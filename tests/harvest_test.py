import json
import os
import sys
from time import time

import pytest

from statsbiblioteket.harvest import Harvest
from statsbiblioteket.harvest.harvest_types import Project
from statsbiblioteket.harvest.rest import json_type_hook, ObjectEncoder

sys.path.insert(0, sys.path[0] + "/..")

curdir = os.path.dirname(os.path.realpath(__file__))


class TestHarvest():
    @pytest.fixture()
    def harvest(self):
        testCreds = json.load(open(os.path.join(curdir, 'test_creds.json')))
        harvest = Harvest.basic(
            testCreds['url'],testCreds['user'],testCreds['password'])
        return harvest

    def test_status_up(self, harvest):
        real = harvest.status()['description']
        expected = "All Systems Operational"
        assert real == expected

    def test_status_not_down(self, harvest):
        real = harvest.status()['description']
        expected = "down"
        assert real != expected

    def test_get_today(self, harvest):
        today = harvest.today
        assert today.has_key("for_day")


    def test_get_projects(self, harvest):
        projects = harvest.projects()
        print(projects)
        pass

    def test_project_create_remove(self, harvest):

        temp_project_name = 'tempProject'

        clients = harvest.clients()
        if len(clients) == 0:
            #TODO
            harvest.create_client()
            clients = harvest.clients()
        client = clients[0]

        projects = harvest.projects()
        for project in projects:
            if project.name == temp_project_name:
                harvest.delete_project(project.id)

        project=Project(name=temp_project_name,
                        active=True,
                        client_id=client.id,
                        bill_by='project',
                        #billable=False,
                        budget_by="project",
                        )
        returnValue = harvest.create_project(project)
        projects = harvest.projects()
        for project in projects:
            if project.name == temp_project_name:
                harvest.delete_project(project.id)
        print(projects)
        pass


    def test_get_users(self, harvest):
        users = harvest.users()
        print(users)
        pass

    # def test_add(self, harvest):
    #     today = harvest.today
    #     start = time()
    #     project = "%s" % today['projects'][0]['id']
    #     task = "%s" % today['projects'][0]['tasks'][0]['id']
    #     assert harvest.add_entry({
    #         "notes": "%s" % start,
    #         "hours": "1.5",
    #         "project_id": project,
    #         "task_id": task
    #     }) is not None
    #     exists = harvest.today
    #     # test that the entry got added
    #     assert len(exists['day_entries']) > len(today['day_entries'])
    #
    #     if len(exists['day_entries']) > len(today['day_entries']):
    #         for entry in exists['day_entries']:
    #             if "%s" % entry['notes'] == "%s" % start:
    #                 assert "1.5" == "%s" % entry['hours']
    #                 assert project == "%s" % entry['project_id']
    #                 assert task == "%s" % entry['task_id']

    def test_cycle(self):
        # load as pure json
        with open(curdir+'/client.json', 'r') as clientjson:
            pure = json.load(clientjson)
            pure = json.dumps(pure)

        # load as object and decode back to json
        with open(curdir+'/client.json', 'r') as clientjson:
            pythonObjectStructure = json.load(clientjson,
                                              object_hook=json_type_hook)

            redumped = json.dumps(pythonObjectStructure, cls=ObjectEncoder)
        assert pure == redumped
