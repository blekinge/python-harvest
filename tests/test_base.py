import json
import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from statsbiblioteket.harvest import Harvest
from statsbiblioteket.harvest import HarvestDBType

curdir = os.path.dirname(os.path.realpath(__file__))


class TestBase(object):

    @pytest.fixture()
    def harvest(self):
        creds_file = os.path.join(curdir, 'test_creds.json')
        try:
            testCreds = json.load(open(creds_file))
            harvest = Harvest.basic(testCreds['url'], testCreds['user'],
                testCreds['password'])
            return harvest
        except IOError as ioe:
            creds_format = """
{
    "url": "https://YOUR_HARVEST_SITE.harvestapp.com",
    "user": "YOUR_HARVEST_EMAIL_ACCOUNT",
    "password": "YOUR_HARVEST_PASSWORD"
}"""

            message = "Failed to read '{creds_file}'\n" \
            "Please create a file called 'test_creds.json' in {curdir}, " \
            "with this content \n{format}\n".format(creds_file=creds_file,
                curdir=curdir, format=creds_format)
            raise RuntimeError(message) from ioe

    @pytest.fixture()
    def session(self):
        engine = create_engine('sqlite://')
        HarvestDBType.metadata.create_all(engine)
        sessionMaker = sessionmaker(bind=engine)
        session = sessionMaker()  # type: Session
        return session


