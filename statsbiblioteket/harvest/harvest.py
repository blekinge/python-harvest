"""
 harvest.py

 Author: Jonathan Hosmer
 (forked from https://github.com/lionheart/python-harvest.git)
 Date: Sat Jan 31 12:17:16 2015
"""

from statsbiblioteket.harvest.clients import Clients
from statsbiblioteket.harvest.contacts import Contacts
from statsbiblioteket.harvest.expense_categories import ExpenseCategories
from statsbiblioteket.harvest.invoices import Invoices
from statsbiblioteket.harvest.people import People
from statsbiblioteket.harvest.projects import Projects
from statsbiblioteket.harvest.task_assignment import TaskAssignment
from statsbiblioteket.harvest.tasks import Tasks
from statsbiblioteket.harvest.timetracking import Timetracking



class Harvest(Clients, Contacts, ExpenseCategories, Invoices, People, Projects,
              Tasks, Timetracking, TaskAssignment):
    """
    Harvest class to implement Harvest API
    """

    @classmethod
    def oath(cls, uri, client_id, token):
        return Harvest(uri=uri, client_id=client_id, token=token)

    @classmethod
    def basic(cls, uri, email, password, put_auth_in_header=True):
        return Harvest(uri=uri, email=email, password=password,
                       put_auth_in_header=put_auth_in_header)

    def __init__(self, uri, email=None, password=None, client_id=None,
                 token=None, put_auth_in_header=True):
        super(Harvest, self).__init__(uri, email, password, client_id, token)

    # Accounts
    @property
    def who_am_i(self):
        """
        who_am_i property
        http://help.getharvest.com/api/introduction/overview/who-am-i/
        """
        return self._get('/account/who_am_i')


