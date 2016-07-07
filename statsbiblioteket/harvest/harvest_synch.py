import argparse
import logging
from datetime import datetime, date
from os.path import expanduser

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.ddl import CreateTable
from sqlalchemy.sql.elements import and_

from statsbiblioteket.harvest import Harvest
from statsbiblioteket.harvest.harvest_types import HarvestDBType, User, Project, \
    Task, Client, TaskAssignment, DayEntry, Expense


def create_parser():
    parser = argparse.ArgumentParser(
            description='Backups all harvest data from your harvest domain to a sqlLite database', )
    parser.add_argument('--domain', action='store', required=True,
                        help='The Harvest domain to backup',
                        dest='harvestDomain')
    parser.add_argument('--user', action='store', required=False,
                        help='The harvest user to connect as',
                        dest='harvestUser')
    parser.add_argument('--password', action='store', required=False,
                        help='The harvest password. If not specified, the username and password is read from the file ~/.harvest, in the format "username=password"',
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
    parser.add_argument('--logFile', default='log.log',
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

    logging.basicConfig(filename=args.logfile,
                        level=getattr(logging, args.loglevel.upper()))
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    backup(args, harvest_user, harvest_pass)

    logging.shutdown()


def backup(args, harvest_user, harvest_pass):
    engine = sqlalchemy.create_engine(args.dbConnectString)
    session_maker = sessionmaker(bind=engine)

    session = session_maker()  # type: Session

    harvest = Harvest.basic(uri=args.harvestDomain, email=harvest_user,
                            password=harvest_pass)

    # Determine modules, for what not to back up
    who_am_i = harvest.who_am_i
    backup_expenses = who_am_i['company']['modules']['expenses']
    backup_invoices = who_am_i['company']['modules']['invoices']

    # printDDL(engine)

    # Create the tables that are missing
    HarvestDBType.metadata.create_all(engine)

    session.query(User).delete()
    users = harvest.users()
    session.add_all(users)
    session.flush()

    session.query(Project).delete()
    projects = harvest.projects()
    session.add_all(projects)
    session.flush()

    session.query(Task).delete()
    tasks = harvest.tasks()
    session.add_all(tasks)
    session.flush()

    session.query(Client).delete()
    clients = harvest.clients()
    session.add_all(clients)
    session.flush()

    for project in projects:
        # Get Tasks for each project
        session.query(TaskAssignment).delete()
        tasks_for_project = harvest.get_all_tasks_from_project(project.id)
        session.add_all(tasks_for_project)
        session.flush()

        # get Timesheets for each project
        timesheets = harvest.timesheets_for_project(project_id=project.id,
                                                    start_date=args.fromDate,
                                                    end_date=args.toDate.replace(
                                                        '-', ''), )
        session.query(DayEntry).filter(and_(DayEntry.spent_at >= args.fromDate,
                                            DayEntry.spent_at <= args.toDate)).delete()
        session.add_all(timesheets)
        session.flush()

        if backup_expenses:
            session.query(Expense).delete()
            expenses = harvest.expenses_for_project(project_id=project.id)
            session.add_all(expenses)
            session.flush()

    if backup_invoices:
        invoices = harvest.invoices()
        session.add_all(invoices)

    session.flush()
    session.commit()
    session.close()


def printDDL(engine):
    tables = HarvestDBType.metadata.sorted_tables
    for table in tables:
        print(CreateTable(table).compile(engine))


if __name__ == '__main__':
    main()
