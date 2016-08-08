import datetime
import logging
import typing
from json import JSONEncoder
from pprint import pformat

import inflection
from sqlalchemy import Table, Column, ForeignKeyConstraint, Integer, DateTime
from sqlalchemy import event, util
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapper
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapper, attributes, object_mapper
from sqlalchemy.orm.collections import InstrumentedDict, InstrumentedList, \
    InstrumentedSet
from sqlalchemy.orm.exc import UnmappedColumnError
from sqlalchemy.orm.properties import RelationshipProperty
from sqlalchemy.orm.state import InstanceState

VERSION_COLUMN_NAME = 'version'


VERSION_META = "version_meta"


UNVERSIONED = "unversioned"


def remove_private_fields(fields: typing.Dict) -> typing.Dict:
    """
    Remove fields whose key start with _ (indicating private-ness)
    :param fields: the fields to clean
    :return: a copy of fields, without the private keys
    """
    fields = dict((key, value) for key, value in fields.items() if
                  not key.startswith('_'))  # Strip out private values
    return fields


class TypeToJSON(JSONEncoder):
    """
    Class to encode the harvest type objects as json
    """

    def default(self, object_to_encode):
        key = inflection.underscore(object_to_encode.__class__.__name__)
        values = object_to_encode.__dict__
        values = remove_private_fields(values)
        values = remove_sqlalchemy_fields(values)

        encoded = {key: values}
        return encoded


def remove_sqlalchemy_fields(fields: typing.Dict) -> typing.Dict:
    """
    Remove fields added by SQL Alchemy
    :param fields: the fields to clean
    :return: a copy of fields, without the sql alchemy keys
    """
    fields = dict((key, value) for key, value in fields.items() if
                  not key.startswith('linked_'))  # Strip out sql relationships
    fields = dict((key, value) for key, value in fields.items() if
                  not isinstance(value, (InstrumentedList, InstrumentedSet,
                                         InstrumentedDict)))  # Strip out
    # sql relationships
    return fields


def remove_fields_with_value_none(fields: typing.Dict) -> typing.Dict:
    """
    Remove keys whose value is none
    :param fields: the fields to clean
    :return: a copy of fields, without the none values
    """
    fields = dict((key, value) for key, value in fields.items() if
                  value is not None)  # Strip out none values
    return fields


class HarvestType(object):
    """
    Base class of all the HarvestType objects
    """

    def __eq__(self, other):
        if type(other) is type(self):
            him = self.__dict__
            him = remove_private_fields(him)
            him = remove_sqlalchemy_fields(him)
            him = remove_fields_with_value_none(him)

            her = other.__dict__
            her = remove_private_fields(her)
            her = remove_sqlalchemy_fields(her)
            her = remove_fields_with_value_none(her)

            return him == her
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self, *args, **kwargs):
        return self.id

    def __lt__(self, other):
        if hasattr(other, 'id'):
            return self.id < other.id
        return False

    def __repr__(self, *args, **kwargs):
        name = inflection.underscore(self.__class__.__name__)
        values = self.__dict__
        values = remove_private_fields(values)
        values = remove_sqlalchemy_fields(values)
        return pformat({name: values})

    def __str__(self, *args, **kwargs):
        mytype = self.__class__.__name__
        name_attr = getattr(self, 'name', None)
        if name_attr:
            name = name_attr
        else:
            name = str(self.id)
        return mytype + ': ' + name



def _lenient_constructor(self, **kwargs):
    """A simple constructor that allows initialization from kwargs.

    Sets attributes on the constructed instance using the names and
    values in ``kwargs``.

    If the attribute is not known beforehand, it is set privately

    see _declarative_constructor
    """
    cls_ = type(self)
    for key in kwargs:
        if not hasattr(cls_, key):
            logging.debug("%r is an invalid keyword argument for %s" % (
            key, cls_.__name__))
            setattr(self, '_' + key, kwargs[key])
        else:
            setattr(self, key, kwargs[key])


def mymap(cls, *arg, **kw):
    mp = mapper(cls, *arg, **kw)
    _history_mapper(mp)
    return mp


HarvestDeclarativeType = declarative_base(cls=HarvestType, mapper=mymap,
                                          constructor=_lenient_constructor)


class HarvestDBType(HarvestDeclarativeType):
    __abstract__ = True

    @declared_attr
    def _updated_on(cls):
        """The _updated_on column lists the timestamp for when this row was
        last modified. Changes only to this column does not count as
        a modification of the row"""
        return Column(DateTime, server_default=func.now(), onupdate=func.now(),
                      info=UNVERSIONED,)

def col_references_table(col: Column, table: Table):
    """
    :param col: The column
    :param table: the table
    :return: True if col contains a foreign key from table
    """
    for fk in col.foreign_keys:
        if fk.references(table):
            return True
    return False


def _is_unversioned(col: Column):
    """
    :param col: The column
    :return: True if the column is annotated as unversioned (info field)
    """
    return UNVERSIONED in col.info


def _is_versioning_col(col: Column):
    """
    :param col: The column
    :return: True if the column is annotated as being versioning metadata
    """
    return VERSION_META in col.info


def _history_mapper(local_mapper: Mapper):
    """
    Initialises a history mapper and adds it to the local mapper
    The responsibility of the mapper is to link SQL tables with columns
      with python attributes. So, this is used when generating the tables, and
      not later
    :param local_mapper: The local mapper
    :return: None
    """

    # Get the class of the object to map
    cls = local_mapper.class_

    # set the "active_history" flag
    # on on column-mapped attributes so that the old version
    # of the info is always loaded (currently sets it on all attributes)
    for prop in local_mapper._prop_set:
        prop.active_history = True
        getattr(cls, prop.key).active_history = True

    super_mapper = local_mapper.inherits
    super_history_mapper = getattr(cls, '__history_mapper__', None)

    polymorphic_on = None
    super_fks = []  # type: typing.List[(str,str)]

    def _col_copy(col: Column) -> Column:
        """
        Copy a column

        :param col: The column to copy
        :return: the copied column
        """
        orig = col
        col = col.copy()
        orig.info['history_copy'] = col
        col.unique = False
        col.default = col.server_default = None
        return col

    properties = util.OrderedDict()  # Mapper properties

    if not super_mapper or local_mapper.local_table is not \
            super_mapper.local_table:

        # Columns to version
        cols = []  # type: typing.List[Column]
        # add column.info to identify columns specific to versioning
        version_meta = {VERSION_META: True}

        for column in local_mapper.local_table.c:
            if _is_versioning_col(column):
                continue
            if _is_unversioned(column):
                continue

            col = _col_copy(column)

            if super_mapper and col_references_table(column,
                                                     super_mapper.local_table):
                super_fks.append((col.key, list(
                    super_history_mapper.local_table.primary_key)[0]))

            cols.append(col)

            if column is local_mapper.polymorphic_on:
                polymorphic_on = col

            orig_prop = local_mapper.get_property_by_column(column)
            # carry over column re-mappings
            if len(orig_prop.columns) > 1 or \
                            orig_prop.columns[0].key != orig_prop.key:
                properties[orig_prop.key] = tuple(
                    col.info['history_copy'] for col in orig_prop.columns)

        if super_mapper:
            super_fks.append((VERSION_COLUMN_NAME,
                              super_history_mapper.local_table.c.version))

        # "version" stores the integer version id.  This column is
        # required.
        cols.append(Column(VERSION_COLUMN_NAME, Integer, primary_key=True,
                           autoincrement=False, info=version_meta))

        # "changed" column stores the UTC timestamp of when the
        # history row was created.
        # This column is optional and can be omitted.
        cols.append(
            Column('changed', DateTime, default=datetime.datetime.utcnow,
                info=version_meta))

        if super_fks:
            cols.append(ForeignKeyConstraint(*zip(*super_fks)))

        table = Table(local_mapper.local_table.name + '_history',
            local_mapper.local_table.metadata, *cols,
            schema=local_mapper.local_table.schema)
    else:
        # single table inheritance.  take any additional columns that may have
        # been added and add them to the history table.
        for column in local_mapper.local_table.c:
            if column.key not in super_history_mapper.local_table.c:
                col = _col_copy(column)
                super_history_mapper.local_table.append_column(col)
        table = None

    if super_history_mapper:
        bases = (super_history_mapper.class_,)

        if table is not None:
            properties['changed'] = ((table.c.changed,) + tuple(
                super_history_mapper.attrs.changed.columns))

    else:
        bases = local_mapper.base_mapper.class_.__bases__
    versioned_cls = type.__new__(type, "%sHistory" % cls.__name__, bases, {})

    m = mapper(versioned_cls, table, inherits=super_history_mapper,
        polymorphic_on=polymorphic_on,
        polymorphic_identity=local_mapper.polymorphic_identity,
        properties=properties)
    cls.__history_mapper__ = m

    if not super_history_mapper:
        local_mapper.local_table.append_column(
            Column(VERSION_COLUMN_NAME, Integer, default=1, nullable=False))
        local_mapper.add_property("version",
            local_mapper.local_table.c.version)


def versioned_objects(object_set: typing.Set):
    """
    filters out all objects that do not have a history mapper

    :param object_set: The set of objects to filter
    :return: a generator of the objects with a history mapper
    """
    for obj in object_set:
        if hasattr(obj, '__history_mapper__'):
            yield obj


def create_version(obj, session: Session, deleted=False):
    """
    Create a new version of the object for the session

    :param obj: The object to create a version for
    :param session: The session
    :param deleted: If true, the object have been deleted
    :return:
    """
    obj_mapper = object_mapper(obj)  # type: Mapper
    history_mapper = obj.__history_mapper__ #Get the history mapper from _history_mapper
    history_cls = history_mapper.class_

    obj_state = attributes.instance_state(obj)  # type: InstanceState

    attr = {}  # Attributes for the version object

    obj_changed = False

    for om, hm in zip(obj_mapper.iterate_to_root(),
            history_mapper.iterate_to_root()):
        if hm.single:
            continue

        for hist_col in hm.local_table.c:
            if _is_versioning_col(hist_col):
                continue
            if _is_unversioned(hist_col):
                continue

            obj_col = om.local_table.c[hist_col.key]

            # get the value of the
            # attribute based on the MapperProperty related to the
            # mapped column.  this will allow usage of MapperProperties
            # that have a different keyname than that of the mapped column.
            try:
                prop = obj_mapper.get_property_by_column(obj_col)
            except UnmappedColumnError:
                # in the case of single table inheritance, there may be
                # columns on the mapped table intended for the subclass only.
                # the "unmapped" status of the subclass column on the
                # base class is a feature of the declarative module.
                continue

            # expired object attributes and also deferred cols might not
            # be in the dict.  force it to load no matter what by
            # using getattr().
            if prop.key not in obj_state.dict:
                getattr(obj, prop.key)

            added, unchanged, deleted = attributes.get_history(obj, prop.key)

            if deleted:
                attr[prop.key] = deleted[0]
                obj_changed = True
            elif unchanged:
                attr[prop.key] = unchanged[0]
            elif added:
                # if the attribute had no value.
                attr[prop.key] = added[0]
                obj_changed = True

    if not obj_changed:
        # not changed, but we have relationships.  OK, check those too
        for prop in obj_mapper.iterate_properties:
            if isinstance(prop, RelationshipProperty) and \
                    attributes.get_history(obj, prop.key, passive=attributes.PASSIVE_NO_INITIALIZE).has_changes():
                for p in prop.local_columns:
                    if p.foreign_keys:
                        obj_changed = True
                        break
                if obj_changed is True:
                    break

    if not obj_changed and not deleted:
        return

    attr[VERSION_COLUMN_NAME] = obj.version
    hist = history_cls()  # The version object
    for key, value in attr.items():  # Set the attributes on the version object
        setattr(hist, key, value)
    session.add(hist)
    obj.version += 1


def versioned_session(session):
    """
    Add a versioning listener to the session

    :param session: The session to wrap
    :return: None
    """
    @event.listens_for(session, 'before_flush')
    def before_flush(session, flush_context, instances):
        for obj in versioned_objects(session.dirty):
            create_version(obj, session)
        for obj in versioned_objects(session.deleted):
            create_version(obj, session, deleted=True)
