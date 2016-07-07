import json
import os
import sys
from time import time

import pytest

from statsbiblioteket.harvest import Harvest
from statsbiblioteket.harvest.harvest_types import Day
from statsbiblioteket.harvest.harvest_types import Project
from statsbiblioteket.harvest.rest import HarvestEncoder
from statsbiblioteket.harvest.encoding import json_type_hook, HarvestEncoder

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
                                              object_hook=json_type_hook)

            redumped = json.dumps(pythonObjectStructure, cls=HarvestEncoder, sort_keys=True)
        assert pure == redumped
