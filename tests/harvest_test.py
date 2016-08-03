import json
import os
import sys

from statsbiblioteket.harvest.harvest_types import Day, json_to_harvest
from statsbiblioteket.harvest.rest import TypeToJSON
from tests.test_base import TestBase

sys.path.insert(0, sys.path[0] + "/..")

curdir = os.path.dirname(os.path.realpath(__file__))


class TestHarvest(TestBase):

    def test_status_up(self, harvest):
        real = harvest.status()['description']
        expected = "All Systems Operational"
        assert real == expected

    def test_status_not_down(self, harvest):
        real = harvest.status()['description']
        isDown = "down"
        assert real != isDown

    def test_get_today(self, harvest):
        today = harvest.today() # type: Day
        assert today.for_day


    def test_get_projects(self, harvest):
        projects = harvest.projects()
        print(projects)
        pass

    def test_get_users(self, harvest):
        users = harvest.users()
        print(users)
        pass

    def test_json_parsing(self):
        # load as pure json
        with open(curdir+'/client.json', 'r') as clientjson:
            pure = json.load(clientjson)
            pure = json.dumps(pure, sort_keys=True) #Sort keys on to be able to assert

        # load as object and decode back to json
        with open(curdir+'/client.json', 'r') as clientjson:
            pythonObjectStructure = json.load(clientjson,
                                              object_hook=json_to_harvest)

            redumped = json.dumps(pythonObjectStructure, cls=TypeToJSON, sort_keys=True)
        assert pure == redumped
