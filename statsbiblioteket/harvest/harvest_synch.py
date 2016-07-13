import argparse
import logging
import logging.config
from datetime import datetime, date
from os.path import expanduser
from pprint import pformat

import sqlalchemy
import sqlalchemy.orm
import typing

from os import path
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.ddl import CreateTable
from sqlalchemy.sql.elements import and_

from statsbiblioteket.harvest import Harvest
from statsbiblioteket.harvest import logger
from statsbiblioteket.harvest.harvest_types import DayEntry, Project, Task, \
    User, Expense, HarvestDBType, Client, TaskAssignment, HarvestType, Invoice




def create_parser():
    parser = argparse.ArgumentParser(
            description='Backups all harvest data from your harvest domain to a SQL database', )
    parser.add_argument('--domain', action='store', required=True,
                        help='The Harvest domain to backup',
                        dest='harvestDomain')
    parser.add_argument('--user', action='store', required=False,
                        help='The harvest user to connect as',
                        dest='harvestUser')
    parser.add_argument('--password', action='store', required=False,
                        help='The harvest password.\n If not specified, the username and password is read from the file ~/.harvest, in the format "username=password"',
                        dest='harvestPassword')

    parser.add_argument('--sql', action='store', default='sqlite:///data.db',
                        help='The sql connect string (default: %(default)s)\n' + 'The string form of the URL is dialect[+driver]://user:password@host/dbname[?key=value..], where dialect is a database name such as mysql, oracle, postgresql, etc., and driver the name of a DBAPI, such as psycopg2, pyodbc, cx_oracle, etc. ',
                        dest='dbConnectString')

    parser.add_argument('--from', action='store', default='1970-01-01',
                        dest='fromDate',
                        help='Get timesheets starting from this date, format YYYY-MM-DD (default: %(default)s)')
    parser.add_argument('--to', action='store',
                        default="{:%Y-%d-%m}".format(date.today()),
                        dest='toDate',
                        help='Get timesheets until this date, format YYYY-MM-DD (default: %(default)s)')

    parser.add_argument('--logLevel', default='DEBUG',
                        help='the log level (default: %(default)s)',
                        dest='loglevel')
    parser.add_argument('--logFile', default='log.ini',
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
        curdir = path.dirname(path.realpath(__file__))
        logging.config.fileConfig(fname=curdir+'/default_log.ini')

    backup(args, harvest_user, harvest_pass)

    logging.shutdown()


def backup(args, harvest_user, harvest_pass):
    engine = sqlalchemy.create_engine(args.dbConnectString)
    session_maker = sessionmaker(bind=engine)

    session = session_maker()  # type: Session

    harvest_client = Harvest.basic(uri=args.harvestDomain, email=harvest_user,
                                   password=harvest_pass)  # type: Harvest

    # Determine modules, for what not to back up
    who_am_i = harvest_client.who_am_i
    # True/false if we have installed this module
    backup_expenses = who_am_i['company']['modules']['expenses'] or False
    backup_invoices = who_am_i['company']['modules']['invoices'] or False

    # printDDL(engine)

    # Create the tables that are missing
    HarvestDBType.metadata.create_all(engine)

    recreate(session, User, harvest_client.users())
    projects = recreate(session, Project, harvest_client.projects())
    recreate(session, Task, harvest_client.tasks())
    recreate(session, Client, harvest_client.clients())

    for project in projects:
        # Get Tasks for each project
        logger.info("For Project %s", project.name)
        task_assignments = recreate(session,
                                    TaskAssignment,
                                    harvest_client.get_all_tasks_from_project(project.id),
            project.id)

        # get Timesheets for each project
        timesheets = harvest_client.timesheets_for_project(
            project_id=project.id,
                start_date=args.fromDate,
            end_date=args.toDate, )
        update_timesheets(session,
                          timesheets,
                          fromDate=args.fromDate,
                          toDate=args.toDate,
                          project_id=project.id)

        if backup_expenses:
            logger.info("Getting expenses for project %s", project.name)
            recreate(session, Expense,
                     harvest_client.expenses_for_project(project_id=project.id))


    if backup_invoices:
        recreate(session, Invoice, harvest_client.invoices())

    session.flush()
    session.commit()
    session.close()


def update_timesheets(session: Session, objects, project_id, fromDate, toDate):
    cls = DayEntry
    num_deleted = session.query(cls).filter(and_(cls.project_id == project_id,
             cls.spent_at >= fromDate,
                                        cls.spent_at <= toDate)).delete()
    logger.info("%ss: Removed %d objects", cls.__name__,num_deleted,)
    logger.debug("Adding new objects: \n%s", pformat(objects))
    session.add_all(objects)
    logger.info("%ss: Added %d objects", cls.__name__, len(objects), )

    session.flush()


def recreate(session: Session, cls: HarvestType, objects: typing.List, project_id = None) -> typing.List:
    query = session.query(cls)
    if project_id is not None:
        query = query.filter(cls.project_id == project_id)
    num_deleted = query.delete()
    logger.info("%ss: Removed %d objects", cls.__name__,num_deleted,)
    logger.debug("Adding new objects: \n%s", pformat(objects))
    session.add_all(objects)
    logger.info("%ss: Added %d objects", cls.__name__, len(objects), )

    session.flush()
    return objects


def printDDL(engine):
    tables = HarvestDBType.metadata.sorted_tables
    for table in tables:
        print(CreateTable(table).compile(engine))


if __name__ == '__main__':
    main()
