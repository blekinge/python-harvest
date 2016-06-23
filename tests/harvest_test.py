import json
import os
import sys
from time import time

import pytest

from statsbiblioteket.harvest import Harvest
from statsbiblioteket.harvest.harvest_types import json_type_hook, \
    ObjectEncoder

sys.path.insert(0, sys.path[0] + "/..")

curdir = os.path.dirname(os.path.realpath(__file__))


class TestHarvest():
    @pytest.fixture()
    def harvest(self):
        harvest = Harvest.basic(
            "https://goretoytest.harvestapp.com",
            "tester@goretoy.com",
            "tester account")
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

    def test_add(self, harvest):
        today = harvest.today
        start = time()
        project = "%s" % today['projects'][0]['id']
        task = "%s" % today['projects'][0]['tasks'][0]['id']
        assert harvest.add_entry({
            "notes": "%s" % start,
            "hours": "1.5",
            "project_id": project,
            "task_id": task
        }) is not None
        exists = harvest.today
        # test that the entry got added
        assert len(exists['day_entries']) > len(today['day_entries'])

        if len(exists['day_entries']) > len(today['day_entries']):
            for entry in exists['day_entries']:
                if "%s" % entry['notes'] == "%s" % start:
                    assert "1.5" == "%s" % entry['hours']
                    assert project == "%s" % entry['project_id']
                    assert task == "%s" % entry['task_id']

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
