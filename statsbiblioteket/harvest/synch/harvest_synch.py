import argparse
import logging
import logging.config
from datetime import datetime, date
from os import path
from os.path import expanduser

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import func
from sqlalchemy.orm import Query
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import attributes
from sqlalchemy.orm.base import object_state
from sqlalchemy.sql.ddl import CreateTable

from statsbiblioteket.harvest import Harvest
from statsbiblioteket.harvest.synch import logger
from statsbiblioteket.harvest.typesystem.harvest_types import *
from statsbiblioteket.harvest.typesystem.orm_types import versioned_session

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
                             'file ~/.harvest\nThe format of this file is \n'
                             '"username=value\n'
                             'password=value"', dest='harvestPassword')

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
    parser.add_argument('--logFile', default=curdir + '/default_log.ini',
                        help='the log file (default: %(default)s)',
                        dest='logfile')

    datetime.today()
    return parser


def main():
    parser = create_parser()

    args = parser.parse_args()

    setup_logging(args)

    harvest_pass, harvest_user = get_harvest_credentials(args)

    backup(args, harvest_user, harvest_pass)

    logging.shutdown()


def setup_logging(args):
    logfile = path.expanduser(path.expandvars(args.logfile))
    if path.exists(logfile):
        logging.config.fileConfig(fname=logfile)
    else:
        logging.config.fileConfig(fname=curdir + '/default_log.ini')


def get_harvest_credentials(args):
    """
        specifies a file that contains a username andr password. The format
        of the file is:
        username=value
        password=value

        This is preferred over specifying the username and password on the
        command line

    :param args:
    :return:
    :link https://www.samba.org/samba/docs/man/manpages-3/mount.cifs.8.html

    """

    cred_file = '~/.harvest'
    harvest_user = None
    harvest_pass = None
    if not args.harvestPassword:
        with open(expanduser(cred_file)) as harvestPassFile:
            lines = harvestPassFile.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith("#") or line.isspace():
                    continue

                parts = line.split("=", maxsplit=1)
                if parts[0] == 'username':
                    harvest_user = parts[1]
                if parts[0] == 'password':
                    harvest_pass = parts[1]
    else:
        harvest_user = args.harvestUser
        harvest_pass = args.harvestPassword
    if harvest_user is None or harvest_pass is None:
        logger.warn(
            "Failed to parse harvest credentials from either the command "
            "line or from {cred_file}".format(cred_file=cred_file))
    return harvest_pass, harvest_user


def backup(args, harvest_user, harvest_pass):
    # Initialise sql alchemy
    engine = sqlalchemy.create_engine(args.dbConnectString)

    session_maker = sessionmaker(bind=engine)

    global session
    session = session_maker()  # type: Session
    versioned_session(session)

    global transaction_now
    transaction_now = session.scalar(func.now())

    try:
        # Create the tables that are missing
        HarvestDBType.metadata.create_all(engine)

        # Connect to Harvest
        hrvst = Harvest.basic(uri=args.harvestDomain, email=harvest_user,
                              password=harvest_pass)  # type: Harvest

        # Determine modules, for what not to back up
        who_am_i = hrvst.who_am_i
        # True/false if we have installed this module
        backup_expenses = who_am_i['company']['modules']['expenses'] or False
        backup_invoices = who_am_i['company']['modules']['invoices'] or False

        # printDDL(engine)

        # Backup the User, Task and Client lists. These are usually very short
        upsert(User, hrvst.users())
        archive_untouched_rows(User)

        upsert(Task, hrvst.tasks())
        archive_untouched_rows(Task)

        upsert(Client, hrvst.clients())
        archive_untouched_rows(Client)

        # If the invoice module is enabled, back up invoices
        if backup_invoices:
            upsert(Invoice, hrvst.invoices())
            archive_untouched_rows(Invoice)

        # Backup and store the projects list
        projects = upsert(Project, hrvst.projects())
        archive_untouched_rows(Project)

        from_date = args.fromDate
        to_date = args.toDate
        logger.info('For date inverval {} to {}'.format(from_date, to_date))
        for project in projects:  # For each Project
            logger.info("For Project %s", project.name)
            logger.add()  # Indent the log statements

            # Get Tasks for each project and store them
            task_assignments = hrvst.get_all_tasks_from_project(project.id)
            upsert(TaskAssignment, task_assignments)

            # Get Expenses for each project and store them
            if backup_expenses:  # Only if the expenses module is enabled
                upsert(Expense, hrvst.expenses_for_project(project.id))

            # get Timesheets for each project and store them
            timesheets = hrvst.timesheets_for_project(project.id,
                                                      start_date=from_date,
                                                      end_date=to_date)
            upsert(DayEntry, timesheets)

            logger.sub()  # Remove log indent

        # Flush changes to be sure they are available for the following queries
        session.flush()

        # Each object have a database maintained _updated_at datetime field.
        #  When the object
        # is upsert'ed as above, this field is set to start_timestamp.
        # For all tables (except DayEntry) we can now remove all objects
        # which where the
        # _updated_at field is less than the start_timestamp
        archive_untouched_rows(TaskAssignment)
        archive_untouched_rows(Expense)

        # All DayEntries outside the given range is marked as updated,
        # to prevent
        # them from being archived
        mark_timesheets_as_updated(DayEntry, from_date, to_date)
        # Now, all DayEntries outside the from_date->to_date range are
        # marked as updated, and
        # all which we got from harvest are marked as updated. Any that
        # remains are
        # entries in the given range, which NO LONGER exist in Harvest. These
        # should be archived
        archive_untouched_rows(DayEntry)

        session.commit()
    finally:
        session.close()


def archive_untouched_rows(cls: HarvestDBType):
    """
    'Archives' the untouched rows
    TODO make this save old versions rather than just deleting them
    :param cls:
    :return:
    """
    query = session.query(cls)  # type: Query
    query = query.filter(cls._updated_on < transaction_now)  # Add a filter
    # query.delete() #Bulk delete
    untouched_rows = query.all()  # type: typing.List[HarvestDBType]

    def delete(row: HarvestDBType):
        logger.debug('deleted {row}'.format(row=str(row)))
        session.delete(row)

    map(delete, untouched_rows)


def mark_timesheets_as_updated(cls: DayEntry, from_date, to_date):
    query = session.query(cls)  # type: Query
    query = query.filter((cls._updated_on < transaction_now) & (
        (cls.spent_at < from_date) | (cls.spent_at > to_date)
    ))
    query = query.order_by(cls.project_id)
    # query.update({DayEntry._updated_on : transaction_now}) # Bulk operation
    old_rows = query.all()  # type: typing.List[DayEntry]

    for old_row in old_rows:
        old_row._updated_on = transaction_now
        logger.debug(
            "Updated timestamp on time entry '{id}' from '{project}' at '{date}' "
            "by '{user}'".format(id=old_row.id,
                                 project=old_row.linked_project,
                                 date=old_row.spent_at,
                                 user=old_row.linked_user))
    session.flush()


def get_history(db_object: HarvestDBType):
    state = object_state(db_object)

    changes = {}
    dict_ = state.dict

    for attr in state.manager.attributes:
        (new_value, _, old_value) = attr.impl.get_history(state, dict_,
                                                          passive=attributes.NO_CHANGE)
        if new_value and old_value:
            changes[str(attr.prop)] = (old_value[0], new_value[0])
        else:
            if new_value:
                changes[str(attr.prop)] = (None, new_value[0])
            else:
                if old_value:
                    changes[str(attr.prop)] = (old_value[0], None)

    return changes


def upsert(cls: HarvestDBType, harvest_objects: typing.Set[HarvestDBType]) -> \
        typing.Set[HarvestDBType]:
    """
    Upserts the given objects in the database
    :param cls: The class of the objects (which implicitly denote the sql
    table)
    :param harvest_objects: The objects to create or update in the database
    :return: The updated objects
    """
    class_name = inflection.pluralize(cls.__name__)  # Used for log messages

    logger.info("%s: Merging %d harvest objects with database", class_name,
                len(harvest_objects))
    logger.add()  # Add indent
    db_objects = set()
    for harvest_object in harvest_objects:
        db_object = session.merge(harvest_object)  # type: HarvestDBType
        db_objects.add(db_object)
        # if session.is_modified(db_object):
        history = get_history(db_object)
        if history:
            logger.debug(
                'Object {id} was changed: {row}'.format(id=str(db_object),
                                                        row=history))
        # Mark as updated so it wont get cleaned
        db_object._updated_on = transaction_now

    session.flush()
    logger.sub()  # Reduce indent back
    return db_objects


def print_DDL(engine):
    tables = HarvestDBType.metadata.sorted_tables
    for table in tables:
        print(CreateTable(table).compile(engine))


if __name__ == '__main__':
    main()
