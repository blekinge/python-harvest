# -*- coding: utf-8 -*-

"""
Harvest Time Tracking API Client
~~~~~~~~~~~~~~~~
"""
import logging

import sys

logger = logging.getLogger(__name__)

module_name = sys.modules[__name__]


# Methods
from statsbiblioteket.harvest.harvest \
    import \
    Harvest

# Types
from statsbiblioteket.harvest.typesystem.harvest_types import \
    Day, \
    Client, \
    Contact, \
    DayEntry, \
    Expense, \
    ExpenseCategory, \
    HarvestType, \
    HarvestDBType, \
    Project, \
    Invoice, \
    Task, \
    TaskAssignment, \
    User

__version__ = "__version__ = '1.1.4rc'"
__author__ = "Asger Askov Blekinge"
__email__ = "abr@statsbiblioteket.dk"
__license__ = "MIT License"

logging.getLogger(__name__).addHandler(logging.NullHandler())
