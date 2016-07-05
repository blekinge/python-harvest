import json
import os
from pprint import pprint

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.ddl import CreateTable

from statsbiblioteket.harvest.harvest_types import Project, HarvestDBType, User, DayEntry
from statsbiblioteket.harvest import Harvest


def harvestClient() -> Harvest:
    harvest = Harvest.basic(uri=harvestDomain, email=harvestUser, password=harvestPassword)
    return harvest


def main():


    engine = sqlalchemy.create_engine(dbConnectString, echo=True)
    session_maker = sessionmaker(bind=engine)


    session = session_maker()  # type: Session

    harvest = harvestClient()

    # Determine modules, for what not to back up
    who_am_i = harvest.who_am_i
    backup_expenses = who_am_i['company']['modules']['expenses']
    backup_invoices = who_am_i['company']['modules']['invoices']

    # Print the DDL
    tables = HarvestDBType.metadata.sorted_tables
    for table in tables:
        print(CreateTable(table).compile(engine))

    #Create the tables that are missing
    HarvestDBType.metadata.create_all(engine)

    users = harvest.users()
    session.add_all(users)
    session.flush()

    projects = harvest.projects()
    session.add_all(projects)
    session.flush()

    tasks = harvest.tasks()
    session.add_all(tasks)
    session.flush()


    clients = harvest.clients()
    session.add_all(clients)
    session.flush()


    for project in projects:
        # Get Tasks for each project
        tasks_for_project = harvest.get_all_tasks_from_project(project.id)
        session.add_all(tasks_for_project)
        session.flush()


        # get Timesheets for each project
        timesheet = harvest.timesheets_for_project(project_id=project.id,
                                                   start_date=timesheetsFrom,
                                                   end_date=timesheetsTo)
        session.add_all(timesheet)
        session.flush()

        if backup_expenses:
            expenses = harvest.expenses_for_project(project_id=project.id,
                                                       start_date=timesheetsFrom,
                                                       end_date=timesheetsTo)
            session.add_all(expenses)
            session.flush()


    if backup_invoices:
        invoices = harvest.invoices()
        session.add_all(invoices)

    session.flush()
    session.commit()


dbConnectString = 'sqlite:///data.db'
harvestDomain = 'https://statsbiblioteket.harvestapp.com'
harvestUser = 'abr@statsbiblioteket.dk'
harvestPassword = 'DtNCROAHic5h'
timesheetsFrom='19700101'
timesheetsTo='20200101'
dumpSQL=True

if __name__ == '__main__':
    main()
