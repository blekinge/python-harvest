from json import JSONEncoder

import sys

def json_type_hook(d):
    try:
        if len(d.keys()) == 1:
            key = d.keys()[0]
            class_ = getattr(sys.modules[__name__], key.title())
            object_ = class_.__new__(class_)
            object_.__dict__ = d[key]
            return object_
    except:
        pass
    return d

class ObjectEncoder(JSONEncoder):
    def default(self, o):
        return {o.__class__.__name__.lower(): o.__dict__}


class Client(object):
    def __init__(self, name, id=None, active=None, currency=None,
                 highrise_id=None, cache_version=None, updated_at=None,
                 created_at=None, currency_symbol=None, details=None,
                 default_invoice_timeframe=None, last_invoice_kind=None):
        super(Client, self).__init__()
        self.id = id
        self.name = name
        self.active = active
        self.currency = currency
        self.highrise_id = highrise_id
        self.cache_version = cache_version
        self.updated_at = updated_at
        self.created_at = created_at
        self.currency_symbol = currency_symbol
        self.details = details
        self.default_invoice_timeframe = default_invoice_timeframe
        self.last_invoice_kind = last_invoice_kind


class Contact(object):
    def __init__(self, id=None, client_id=None, first_name=None,
                 last_name=None,
                 email=None, phone_office=None, phone_mobile=None, fax=None,
                 title=None, created_at=None, updated_at=None):
        super(Contact, self).__init__()
        self.id = id
        self.client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_office = phone_office
        self.phone_mobile = phone_mobile
        self.fax = fax
        self.title = title
        self.created_at = created_at
        self.updated_at = updated_at


class Invoice(object):
    def __init__(self, client_id=None, period_start=None, period_end=None,
                 number=None, issued_at=None, due_at=None, amount=None,
                 currency=None, state=None, notes=None, purchase_order=None,
                 due_amount=None, due_at_human_format=None, created_at=None,
                 updated_at=None, tax=None, tax_amount=None, subject=None,
                 recurring_invoice_id=None, tax2=None, tax2_amount=None,
                 client_key=None, estimate_id=None, discount=None,
                 discount_amount=None, retainer_id=None, created_by_id=None,
                 csv_line_items=None):
        super(Invoice, self).__init__()
        self.id = id
        self.client_id = client_id
        self.period_start = period_start
        self.period_end = period_end
        self.number = number
        self.issued_at = issued_at
        self.due_at = due_at
        self.amount = amount
        self.currency = currency
        self.state = state
        self.notes = notes
        self.purchase_order = purchase_order
        self.due_amount = due_amount
        self.due_at_human_format = due_at_human_format
        self.created_at = created_at
        self.updated_at = updated_at
        self.tax = tax
        self.tax_amount = tax_amount
        self.subject = subject
        self.recurring_invoice_id = recurring_invoice_id
        self.tax2 = tax2
        self.tax2_amount = tax2_amount
        self.client_key = client_key
        self.estimate_id = estimate_id
        self.discount = discount
        self.discount_amount = discount_amount
        self.retainer_id = retainer_id
        self.created_by_id = created_by_id
        self.csv_line_items = csv_line_items
