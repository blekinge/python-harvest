import sys
from json import JSONEncoder

import inflection as inflection
from sqlalchemy.orm.collections import InstrumentedList, InstrumentedSet, \
    InstrumentedDict

from statsbiblioteket.harvest import harvest_types
from statsbiblioteket.harvest.harvest_types import DayEntry, Day


def getOurName(d):
    oneValue = len(d.keys()) == 1
    if oneValue:
        key = list(d.keys())[0]
        className = inflection.camelize(key)
        return className, d[key]

    if 'for_day' in d and 'day_entries' in d:  # Special handling for Day
        day_entries = d['day_entries']
        d['day_entries'] = [wrap(DayEntry.__name__, day_entry) for day_entry in
                            day_entries or []]
        return Day.__name__, d
    return None, d


def json_type_hook(d):
    class_name, values = getOurName(d)

    if class_name:
        return wrap(class_name, values)

    return d


def wrap(className, values):
    name___ = sys.modules[harvest_types.__name__]
    class_ = getattr(name___, className)
    object_ = class_(**values)
    # object_.__dict__ = values
    # object_.__dict__.update((k, v) for k, v in d[key] if v is not None)
    return object_


class HarvestEncoder(JSONEncoder):
    def default(self, o):
        elementName = inflection.underscore(o.__class__.__name__)
        fields = o.__dict__
        fields = dict((key, value) for key, value in fields.items() if not key.startswith('_')) #Strip out private values
        fields = dict((key, value) for key, value in fields.items() if not key.startswith('linked_'))  # Strip out sql relationships
        fields = dict((key, value) for key, value in fields.items() if
                      not isinstance(value,(InstrumentedList,InstrumentedSet,InstrumentedDict)))  # Strip out sql relationships
        # fields = dict((key, value) for key, value in fields.items() if value is not None) #Strip out none values
        encoded = {elementName: fields}
        return encoded