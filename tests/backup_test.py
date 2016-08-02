import json
import os
import sys
from pprint import pprint

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from statsbiblioteket.harvest import Harvest
from statsbiblioteket.harvest.harvest_types import User, HarvestDBType, Project, Client, Task, Expense, Invoice, \
    DayEntry, TaskAssignment

sys.path.insert(0, sys.path[0] + "/..")

curdir = os.path.dirname(os.path.realpath(__file__))


class TestBackup:
    @pytest.fixture()
    def harvest(self):
        testCreds = json.load(open(os.path.join(curdir, 'test_creds.json')))
        harvest = Harvest.basic(
                testCreds['url'], testCreds['user'], testCreds['password'])
        return harvest

    @pytest.fixture()
    def session(self):
        engine = create_engine('sqlite://')
        HarvestDBType.metadata.create_all(engine)
        sessionMaker = sessionmaker(bind=engine)
        session = sessionMaker() #type: Session
        return session

    def test_backup_users(self, harvest, session):
        users = harvest.users()
        session.add_all(users)
        session.commit()
        savedUsers = session.query(User).all()
        assert sorted(users) == sorted(savedUsers)

    def test_backup_projects(self, harvest, session):
        projects = harvest.projects()
        session.add_all(projects)
        session.commit()
        savedprojects = session.query(Project).all()
        assert sorted(projects) == sorted(savedprojects)

    def test_backup_tasks(self, harvest, session):
        tasks = harvest.tasks()
        session.add_all(tasks)
        session.commit()
        savedtasks = session.query(Task).all()
        assert sorted(tasks) == sorted(savedtasks)

    def test_backup_clients(self, harvest, session):
        clients = harvest.clients()
        session.add_all(clients)
        session.commit()
        savedclients = session.query(Client).all()
        assert sorted(clients) == sorted(savedclients)

    @pytest.mark.skipif(True, reason='no invoices for the test project')
    def test_backup_invoices(self, harvest, session):
        invoices = harvest.invoices()
        session.add_all(invoices)
        session.commit()
        savedinvoices = session.query(Invoice).all()
        assert sorted(invoices) == sorted(savedinvoices)

    @pytest.mark.skipif(True, reason='no expenses for the test project')
    def test_backup_expenses(self, harvest, session):
        expenses = harvest.expenses()
        session.add_all(expenses)
        session.commit()
        savedexpenses = session.query(Expense).all()
        assert sorted(expenses) == sorted(savedexpenses)

    @pytest.mark.skipif(True, reason='Slow test')
    def test_backup_all(self, harvest: Harvest):
        me = harvest.who_am_i
        pprint(me)

        engine = create_engine('sqlite://')
        HarvestDBType.metadata.create_all(engine)
        sessionMaker = sessionmaker(bind=engine)
        session = sessionMaker() # type: Session

        if session.query(User).count() == 0:
            users = harvest.users()
            session.add_all(users)

        if session.query(Project).count() == 0:
            projects = harvest.projects()
            session.add_all(projects)
        else:
            projects = session.query(Project).all()

        if session.query(Task).count() == 0:
            tasks = harvest.tasks()
            session.add_all(tasks)

        if session.query(Client).count() == 0:
            clients = harvest.clients()
            session.add_all(clients)

        #get Tasks assigned to each project
        if session.query(TaskAssignment).count() == 0:
            for project in projects:
                tasks_for_project = harvest.get_all_tasks_from_project(project.id)
                session.add_all(tasks_for_project)

        if session.query(DayEntry).count() == 0:
            # get Timesheets for each project
            for project in projects:
                timesheet = harvest.timesheets_for_project(project_id=project.id,
                                                           start_date='2016-03-01',
                                                           end_date='2016-05-01')
                session.add_all(timesheet)

        session.commit()

        my_id = me['user']['id']
        me_as_user = session.query(User).filter_by(id=my_id).first() # type: User

        assert me_as_user.email == me['user']['email']


pass
