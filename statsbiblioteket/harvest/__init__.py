# -*- coding: utf-8 -*-

"""
Harvest Time Tracking API Client
~~~~~~~~~~~~~~~~
"""

# Methods
from statsbiblioteket.harvest.harvest \
    import \
    Harvest

from statsbiblioteket.harvest.harvest_synch \
    import \
    create_parser # This import is important for the sphinx-argparse docs

# Types
from statsbiblioteket.harvest.harvest_types import \
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




# Set default logging handler to avoid "No handler found" warnings.
import logging


__version__ = "1.0.4"
__author__ = "Alex Goretoy"
__copyright__ = "Copyright 2012, Alex Goretoy"
__maintainer__ = "Alex Goretoy"
__email__ = "alex@goretoy.com"
__license__ = "MIT License"


logging.getLogger(__name__).addHandler(logging.NullHandler())



