import argparse
import logging
import logging.config
import typing
from datetime import datetime, date
from os import path
from os.path import expanduser
from pprint import pformat

import inflection
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.ddl import CreateTable

from statsbiblioteket.harvest.synch import logger
from statsbiblioteket.harvest import Harvest
from statsbiblioteket.harvest.harvest_types import DayEntry, Project, Task, \
    User, Expense, HarvestDBType, Client, TaskAssignment, HarvestType, Invoice

curdir = path.dirname(path.realpath(__file__))


def create_parser():
    parser = argparse.ArgumentParser(
        description='Backups all harvest data from your harvest domain '
                    'to a SQL database', )
    parser.add_argument('--domain', action='store', required=True,
                        help='The Harvest domain to backup',
                        dest='harvestDomain')
    parser.add_argument('--user', action='store', required=False,
                        help='The harvest user to connect as',
                        dest='harvestUser')
    parser.add_argument('--password', action='store', required=False,
                        help='The harvest password.\n If not specified, '
                             'the username and password is read from the '
                             'file ~/.harvest, in the format '
                             '"username=password"', dest='harvestPassword')

    parser.add_argument('--sql', action='store', default='sqlite:///data.db',
                        help='The sql connect string (default: %('
                             'default)s)\n' + 'The string form of the URL is '
                                              'dialect['
                                              '+driver]://user:password@host/dbname[?key=value..], where dialect is a database name such as mysql, oracle, postgresql, etc., and driver the name of a DBAPI, such as psycopg2, pyodbc, cx_oracle, etc. ',
                        dest='dbConnectString')

    parser.add_argument('--from', action='store', default='1970-01-01',
                        dest='fromDate',
                        help='Get timesheets starting from this date, '
                             'format YYYY-MM-DD (default: %(default)s)')
    parser.add_argument('--to', action='store',
                        default="{:%Y-%d-%m}".format(date.today()),
                        dest='toDate',
                        help='Get timesheets until this date, format '
                             'YYYY-MM-DD (default: %(default)s)')

    parser.add_argument('--logLevel', default='DEBUG',
                        help='the log level (default: %(default)s)',
                        dest='loglevel')
    parser.add_argument('--logFile', default=curdir+'/default_log.ini',
                        help='the log file (default: %(default)s)',
                        dest='logfile')

    datetime.today()
    return parser


def main():

    parser = create_parser()

    args = parser.parse_args()

    harvest_user = None
    harvest_pass = None
    if not args.harvestPassword:
        with open(expanduser('~/.harvest')) as harvestPassFile:
            lines = harvestPassFile.readlines()
            for line in lines:
                if line.startswith("#") or line.isspace():
                    continue
                parts = line.strip().split("=", maxsplit=1)
                harvest_user = parts[0]
                harvest_pass = parts[1]

    else:
        harvest_user = args.harvestUser
        harvest_pass = args.harvestPassword

    logfile = path.expanduser(path.expandvars(args.logfile))
    if path.exists(logfile):
        logging.config.fileConfig(fname=logfile)
    else:
        logging.config.fileConfig(fname=curdir+'/default_log.ini')

    backup(args, harvest_user, harvest_pass)

    logging.shutdown()


def backup(args, harvest_user, harvest_pass):
    engine = sqlalchemy.create_engine(args.dbConnectString)
    session_maker = sessionmaker(bind=engine)

    session = session_maker()  # type: Session

    hrvst = Harvest.basic(uri=args.harvestDomain, email=harvest_user,
                                   password=harvest_pass)  # type: Harvest

    # Determine modules, for what not to back up
    who_am_i = hrvst.who_am_i
    # True/false if we have installed this module
    backup_expenses = who_am_i['company']['modules']['expenses'] or False
    backup_invoices = who_am_i['company']['modules']['invoices'] or False

    # printDDL(engine)

    # Create the tables that are missing
    HarvestDBType.metadata.create_all(engine)

    recreate(session, User, hrvst.users())
    projects = recreate(session, Project, hrvst.projects())
    recreate(session, Task, hrvst.tasks())
    recreate(session, Client, hrvst.clients())

    for project in projects:
        # Get Tasks for each project
        logger.info("For Project %s", project.name)
        logger.add()

        task_assignments = hrvst.get_all_tasks_from_project(project.id)
        recreate(session, TaskAssignment, task_assignments,
                 TaskAssignment.project_id == project.id)

        # get Timesheets for each project
        timesheets = hrvst.timesheets_for_project(project.id,
                                                  start_date=args.fromDate,
                                                  end_date=args.toDate, )
        recreate(session, DayEntry, timesheets,
                 DayEntry.project_id == project.id,
                 DayEntry.spent_at >= args.fromDate,
                 DayEntry.spent_at <= args.toDate)

        if backup_expenses:
            recreate(session, Expense, hrvst.expenses_for_project(project.id),
                     Expense.project_id == project.id)
        logger.sub()

    if backup_invoices:
        recreate(session, Invoice, hrvst.invoices())

    session.flush()
    session.commit()
    session.close()


def recreate(session: Session, cls: HarvestType, objects: typing.Set,
             project_id=None, *criterion) -> typing.Set:
    """
    Upserts the given objects in the database and removes any objects not given.
    To elaborate, all objects of the same type, matching the project_id, if given
    and any other criterion will be deleted, if they are not present in
    :param session: The database session
    :param cls: The class of the objects (which implicitly denote the sql table)
    :param objects: The objects to create
    :param project_id: The project id
    :param criterion: Other criterion for the delete
    :return: The updated objects
    """
    query = session.query(cls)
    if project_id is not None and hasattr(cls, 'project_id'):
        query = query.filter(cls.project_id == project_id)
    query = query.filter(*criterion)
    existing = set(query.all())

    toDelete = existing.difference(set(objects))
    for dbObj in toDelete:
        session.delete(dbObj)

    classname = inflection.pluralize(cls.__name__)
    logger.info("%s: Removed %d objects", classname, len(toDelete))

    logger.info("%s: Merging %d harvest objects with database", classname, len(objects))
    updates = 0
    for object in objects:
        result = session.merge(object)
        if session.is_modified(result):
            updates += 1
    logger.info("%s: Added/updated %d objects", classname, updates)

    session.flush()
    return objects


def printDDL(engine):
    tables = HarvestDBType.metadata.sorted_tables
    for table in tables:
        print(CreateTable(table).compile(engine))


if __name__ == '__main__':
    main()
