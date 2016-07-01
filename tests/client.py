import json
import os

import sys
from pprint import pprint

from statsbiblioteket.harvest import Harvest


sys.path.insert(0, sys.path[0] + "/..")

curdir = os.path.dirname(os.path.realpath(__file__))


def harvestApi():
    testCreds = json.load(open(os.path.join(curdir, 'test_creds.json')))
    harvest = Harvest.basic(testCreds['url'], testCreds['user'],
                            testCreds['password'])
    return harvest


def main():

    harvest = harvestApi()

    users = harvest.users()
    pprint(users)

    projects = harvest.projects()
    pprint(projects)
    project_timesheets = {}
    for project in projects:
        timesheet = harvest.timesheets_for_project(project.id,'19700101','20200101')
        project_timesheets[project.id] = timesheet

    pprint(project_timesheets)


    pass





if __name__ == '__main__':
    main()