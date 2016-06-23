import sys
import unittest
from time import time

sys.path.insert(0, sys.path[0] + "/..")

import statsbiblioteket.harvest as harvest


class TestHarvest(unittest.TestCase):
    def setUp(self):
        self.harvest = harvest.Harvest.basic(
            "https://goretoytest.harvestapp.com",
            "tester@goretoy.com",
            "tester account")

    def tearDown(self):
        pass

    def test_status_up(self):
        real = harvest.status()['description']
        expected = "All Systems Operational"
        assert real == expected

    def test_status_not_down(self):
        real = harvest.status()['description']
        expected = "down"
        assert real != expected

    def test_get_today(self):
        today = self.harvest.today
        assert today.has_key("for_day")

    def test_add(self):
        today = self.harvest.today
        start = time()
        project = "%s" % today['projects'][0]['id']
        task = "%s" % today['projects'][0]['tasks'][0]['id']
        self.assertTrue(self.harvest.add({
            "notes": "%s" % start,
            "hours": "1.5",
            "project_id": project,
            "task_id": task
        }))
        exists = self.harvest.today
        # test that the entry got added
        self.assertTrue(len(exists['day_entries']) > len(today['day_entries']))

        if len(exists['day_entries']) > len(today['day_entries']):
            for entry in exists['day_entries']:
                if "%s" % entry['notes'] == "%s" % start:
                    self.assertEqual("1.5", "%s" % entry['hours'],
                                     "Hours are not equal")
                    self.assertEqual(project, "%s" % entry['project_id'],
                                     "Project Id not equal")
                    self.assertEqual(task, "%s" % entry['task_id'],
                                     "Task Id not equal")


if __name__ == '__main__':
    unittest.main()
