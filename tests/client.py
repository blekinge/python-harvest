import json
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from statsbiblioteket.harvest.harvest_types import User, Project, HarvestDBType

sys.path.insert(0, sys.path[0] + "/..")

curdir = os.path.dirname(os.path.realpath(__file__))


def harvestApi():
    testCreds = json.load(open(os.path.join(curdir, 'test_creds.json')))
    from statsbiblioteket.harvest import Harvest
    harvest = Harvest.basic(testCreds['url'], testCreds['user'],
                            testCreds['password'])
    return harvest


def readDB():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from statsbiblioteket.harvest.harvest_types import Project

    engine = create_engine('sqlite:///data.db', echo=True)

    sessionMaker = sessionmaker(bind=engine)
    session = sessionMaker()

    project = session.query(Project).first() # type: Project

    tasks = project.task_assignments

    for task in tasks:
        print(task.project)
        print(task.task)


def loadDayEntries():
    harvest = harvestApi()

    engine = create_engine('sqlite:///data.db', echo=True)
    HarvestDBType.metadata.create_all(engine)
    sessionMaker = sessionmaker(bind=engine)
    session = sessionMaker()

    projects = session.query(Project).all()

    # get Timesheets for each project
    for project in projects:
        timesheet = harvest.timesheets_for_project(project.id, '19700101',
                                                   '20200101')
        session.add_all(timesheet)
    session.commit()
    pass


def loadBasics():

    harvest = harvestApi()

    engine = create_engine('sqlite:///data.db', echo=True)
    HarvestDBType.metadata.create_all(engine)
    sessionMaker = sessionmaker(bind=engine)
    session = sessionMaker()

    users = harvest.users()
    session.add_all(users)
    print(session.query(User).first())

    projects = harvest.projects()
    session.add_all(projects)

    #get Tasks
    tasks = harvest.tasks()
    session.add_all(tasks)

    #get Tasks assigned to each project
    for project in projects:
        tasks_for_project = harvest.get_all_tasks_from_project(project.id)
        session.add_all(tasks_for_project)
    session.commit()

    pass


if __name__ == '__main__':
    #loadDayEntries()
    readDB()