"""
 harvest.py

 Author: Jonathan Hosmer
 (forked from https://github.com/lionheart/python-harvest.git)
 Date: Sat Jan 31 12:17:16 2015
"""
import logging

from statsbiblioteket.harvest.clients import Clients
from statsbiblioteket.harvest.contacts import Contacts
from statsbiblioteket.harvest.expense_categories import ExpenseCategories
from statsbiblioteket.harvest.expenses import Expenses
from statsbiblioteket.harvest.invoices import Invoices
from statsbiblioteket.harvest.projects import Projects
from statsbiblioteket.harvest.task_assignments import TaskAssignments
from statsbiblioteket.harvest.tasks import Tasks
from statsbiblioteket.harvest.timetracking import Timetracking
from statsbiblioteket.harvest.users import Users

logger = logging.getLogger(__name__)


class Harvest(Clients, Contacts, ExpenseCategories, Invoices, Users, Projects,
              Tasks, Timetracking, TaskAssignments, Expenses):
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

        ::

            {
              'company': {
                'active': True,
                'base_uri': 'https://statsbiblioteket.harvestapp.com',
                'clock': '24h',
                'color_scheme': 'red',
                'decimal_symbol': ',',
                'full_domain': 'statsbiblioteket.harvestapp.com',
                'modules': {
                  'approval': False,
                  'estimates': False,
                  'expenses': False,
                  'invoices': False
                },
                'name': 'State and University Library',
                'plan_type': 'business-v3',
                'thousands_separator': '.',
                'time_format': 'hours_minutes',
                'week_start_day': 'Monday'
              },
              'user': {
                'admin': True,
                'avatar_url': '/assets/profile_images/abraj_albait_towers.png?1456217395',
                'email': 'abr@statsbiblioteket.dk',
                'first_name': 'Asger',
                'id': 1221014,
                'last_name': 'Askov-Blekinge',
                'project_manager': {
                  'can_create_invoices': True,
                  'can_create_projects': True,
                  'can_see_rates': True,
                  'is_project_manager': False
                },
                'timestamp_timers': False,
                'timezone': 'Berlin',
                'timezone_identifier': 'Europe/Berlin',
                'timezone_utc_offset': 7200
              }
            }
        """
        return self._get('/account/who_am_i')


