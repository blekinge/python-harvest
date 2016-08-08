import sys
import typing
from typing import List

import inflection
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship

from statsbiblioteket.harvest.typesystem.orm_types import HarvestDBType, HarvestType

_module_name = sys.modules[__name__]


def json_to_harvest(json_dict: typing.Dict):
    # This function should be in orm_types.py, but the explicit reference to
    # DayEntry class will cause a circular dependency
    """
    If possible, convert the json dictionary to a harvest type object
    :param json_dict: The json dict
    :return: A harvest type object, or the json dictionary, if no harvest type
    was found
    """
    if len(json_dict) == 1:  # Just one value
        (first_key, _), = json_dict.items()

        class_name = inflection.camelize(first_key)

        class_ = getattr(_module_name, class_name)

        return class_(**json_dict[first_key])

    if 'for_day' in json_dict and 'day_entries' in json_dict:
        # Special handling for Day

        day_entries_json = json_dict['day_entries']

        day_entries = [DayEntry(**day_entry_fields) for day_entry_fields in
                       day_entries_json or []]

        json_dict['day_entries'] = day_entries

        return Day(**json_dict)

    return json_dict


class User(HarvestDBType):
    """
    ::

        "user": {
            "id": 508343,
            "email": "user@example.com",
            "created_at": "2013-04-30T20:28:12Z",
            "is_admin": true,
            "first_name": "Harvest",
            "last_name": "User",
            "timezone": "Eastern Time (US & Canada)",
            "is_contractor": false,
            "telephone": "",
            "is_active": true,
            "has_access_to_all_future_projects": true,
            "default_hourly_rate": 0,
            "department": "",
            "wants_newsletter": true,
            "updated_at": "2015-04-29T14:54:19Z",
            "cost_rate": null,
            "identity_account_id": 302900,
            "identity_user_id": 20725
        }
   """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    first_name = Column(String)

    last_name = Column(String)

    email = Column(String)

    created_at = Column(String)

    is_admin = Column(Boolean, nullable=True)
    """Optional: To create a new admin user"""

    timezone = Column(String, nullable=True)
    """Optional: To set a timezone other than the account default."""

    is_contractor = Column(Boolean, nullable=True)
    """Optional: To create a new contractor user."""

    telephone = Column(String, nullable=True)
    """Optional: Telephone number for user."""

    is_active = Column(Boolean, nullable=True)
    """Optional: If the user is active, or archived (true, false)"""

    has_access_to_all_future_projects = Column(Boolean, nullable=True)
    """Optional: If true this user will automatically be assigned to all new projects."""

    default_hourly_rate = Column(Integer, nullable=True)
    """Optional: Default rate for the user in new projects, if no rate is specified."""

    department = Column(String, nullable=True)
    """Optional: Department for user."""

    wants_newsletter = Column(Boolean, nullable=True)

    updated_at = Column(String)

    cost_rate = Column(String, nullable=True)
    """Optional: Cost (internal) rate for user."""

    identity_account_id = Column(Integer, nullable=True)

    identity_user_id = Column(Integer, nullable=True)

    signup_redirection_cookie = Column(String, nullable=True)

    linked_day_entries = relationship('DayEntry',
                                      back_populates="linked_user")  # type: List[DayEntry]

    linked_expenses = relationship('Expense', back_populates="linked_user") # type: List[Expense]

    linked_invoices = relationship('Invoice', back_populates='linked_creator') # type: List[Invoice]

    def __str__(self, *args, **kwargs):
        super_str = super(User, self).__str__(args, kwargs)
        local_str = '{firstName} {lastName} <{email}>'.format(
            firstName=self.first_name, lastName=self.last_name,
            email=self.email)
        return super_str + ' ' + local_str


class Project(HarvestDBType):
    """
    ::

        "project": {
            "id": 3554414,
            "client_id": 3398386,
            "name": "Internal",
            "code": "Testing",
            "active": true,
            "billable": true,
            "bill_by": "People",
            "hourly_rate": 100,
            "budget": 100,
            "budget_by": "project",
            "notify_when_over_budget": true,
            "over_budget_notification_percentage": 80,
            "over_budget_notified_at": null,
            "show_budget_to_all": true,
            "created_at": "2013-04-30T20:28:12Z",
            "updated_at": "2015-04-15T15:44:17Z",
            "starts_on": "2013-04-30",
            "ends_on": "2015-06-01",
            "estimate": 100,
            "estimate_by": "project",
            "hint_earliest_record_at": "2013-04-30",
            "hint_latest_record_at": "2014-12-09",
            "notes": "Some project notes go here!",
            "cost_budget": null,
            "cost_budget_include_expenses": false
        }

    .. seealso:: http://help.getharvest.com/api/projects-api/projects/create-and-show-projects/
    """
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    """Project ID"""

    client_id = Column(Integer, ForeignKey('clients.id'), primary_key=False)
    """Client ID for project"""

    name = Column(String)
    """Project name"""

    code = Column(String)
    """Project code"""

    active = Column(Boolean)
    """Whether the project is active or archived. Options: true, false."""

    billable = Column(Boolean, nullable=True)
    """Whether the project is billable or not billable. Options: true, false."""

    bill_by = Column(String)
    """The method by which the project is invoiced. Options: "project", "tasks", "people", or "none"."""

    hourly_rate = Column(Integer, nullable=True)
    """Rate for projects billed by Project Hourly Rate"""

    budget = Column(Integer, nullable=True)
    """Budget value for the project."""

    budget_by = Column(String)
    """The method by which the project is budgeted. Options: "project" (Hours Per Project), "project_cost" (Total Project Fees), "task" (Hours Per Task), "person" (Hours Per Person), "none" (No Budget)."""

    notify_when_over_budget = Column(Boolean)
    """Option to send notification emails when a project reaches the budget threshold set in Over-Budget-Notification-Percentage Options: true, false."""

    over_budget_notification_percentage = Column(Integer)
    """Percentage value to trigger over budget email alerts."""

    over_budget_notified_at = Column(String, nullable=True)
    """Date of last over budget notification. If none have been sent, this will be nil."""

    show_budget_to_all = Column(Boolean)
    """Option to show project budget to all employees. Does not apply to Total Project Fee projects. Options: true, false."""

    created_at = Column(String)
    """Date of earliest record for this project. Updated every 24 hours."""

    updated_at = Column(String)
    """Date of most recent record for this project. Updated every 24 hours."""

    starts_on = Column(String, nullable=True)

    ends_on = Column(String, nullable=True)

    estimate = Column(Integer, nullable=True)

    estimate_by = Column(String)

    hint_earliest_record_at = Column(String)

    hint_latest_record_at = Column(String)

    notes = Column(String)

    cost_budget = Column(String, nullable=True)
    """Budget value for Total Project Fees projects."""

    cost_budget_include_expenses = Column(Boolean, nullable=True)
    """Option for budget of Total Project Fees projects to include tracked expenses."""

    linked_task_assignments = relationship('TaskAssignment',
                                    back_populates="linked_project")  # type: List[TaskAssignment]

    linked_day_entries = relationship('DayEntry',
                               back_populates="linked_project")  # type: List[DayEntry]

    linked_expenses = relationship('Expense', back_populates="linked_project") # type: List[Expense]

    linked_client = relationship('Client',back_populates='linked_projects') # type: Client


class Client(HarvestDBType):
    """
    Data class for Harvest Users.

    Maps to and from this example JSON

    .. code-block:: json

        "client": {
            "id": 3398386,
            "name": "Your Account",
            "active": true,
            "currency": "United States Dollar - USD",
            "highrise_id": null,
            "cache_version": 821859237,
            "updated_at": "2015-04-15T16:25:50Z",
            "created_at": "2015-04-15T16:25:50Z",
            "currency_symbol": "$",
            "details": "123 Main St\\r\\nAnytown, NY 12345",
            "default_invoice_timeframe": null,
            "last_invoice_kind": null
        }

    .. seealso:: http://help.getharvest.com/api/clients-api/clients/using-the-clients-api/ for more details
    """

    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    """Client name"""

    active = Column(Boolean)
    """Determines if the client is active, or archived. Options: true, false."""

    currency = Column(String)
    """The currency you’d like to use for the client."""

    highrise_id = Column(Integer, nullable=True)
    """Optional Highrise ID for our legacy integration"""

    address = Column(String, nullable=True)

    cache_version = Column(Integer)

    updated_at = Column(String)

    created_at = Column(String)

    currency_symbol = Column(String)
    """The symbol that correlates to the selected currency."""

    details = Column(String, nullable=True)
    """Additional details, normally used for address information."""

    default_invoice_timeframe = Column(String, nullable=True)

    default_invoice_kind = Column(String, nullable=True)

    last_invoice_kind = Column(String, nullable=True)

    statement_key = Column(String, nullable=True)

    linked_contacts = relationship('Contact',
                            back_populates="linked_client")  # type: List[Contact]

    linked_invoices = relationship('Invoice', back_populates='linked_client') # type: List[Invoice]

    linked_projects = relationship('Project', back_populates='linked_client') # type: List[Project]


class DayEntry(HarvestDBType):
    """
    ::

        "day_entry": {
                "id": 367231666,
                "notes": "Some notes.",
                "spent_at": "2015-07-01",
                "hours": 0.16,
                "user_id": 508343,
                "project_id": 3554414,
                "task_id": 2086200,
                "created_at": "2015-08-25T14:31:52Z",
                "updated_at": "2015-08-25T14:47:02Z",
                "adjustment_record": false,
                "timer_started_at": "2015-08-25T14:47:02Z",
                "is_closed": false,
                "is_billed": false,
                "hours_with_timer": 0.16
            }

            {
              "task": "Opgave",
              "task_id": "5402830",

              "client": "Statsbiblioteket",

              "project": "Andet",
              "project_id": "9817858",

              "user_id": 1221014,

              "created_at": "2016-07-07T08:18:33Z",
              "id": 484786391,
              "hours_without_timer": 0.37,
              "spent_at": "2016-07-07",
              "notes": "Mails",
              "updated_at": "2016-07-07T08:30:48Z",
              "hours": 0.37
            }
    """

    __tablename__ = 'day_entries'

    id = Column(Integer, primary_key=True)
    """Time Entry ID"""

    notes = Column(String)
    """Time entry notes"""

    spent_at = Column(String)
    """Date of the time entry"""

    hours = Column(Float)
    """Number of (decimal time) hours tracked in this time entry"""

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=False)
    """User ID that tracked this time entry"""

    linked_user = relationship('User', back_populates="linked_day_entries")  # type: User

    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=False)
    """Project ID that the time entry is associated with"""

    linked_project = relationship('Project',
                           back_populates="linked_day_entries")  # type: Project

    task_id = Column(Integer, ForeignKey('tasks.id'), primary_key=False)

    linked_task = relationship('Task', back_populates="linked_day_entries")  # type: Task

    created_at = Column(String)
    """Time (UTC) and date that entry was created"""

    updated_at = Column(String)
    """Time (UTC) and date that entry was last updated"""

    adjustment_record = Column(Boolean)

    timer_started_at = Column(String)
    """Time (UTC) and date that timer was started (if tracking by duration)"""

    is_closed = Column(Boolean)
    """true if the time entry has been approved via Timesheet Approval (no API support), false if un-approved"""

    is_billed = Column(Boolean)
    """true if the time entry has been marked as invoiced, false if uninvoiced"""

    hours_with_timer = Column(Float, nullable=True)
    """Running timers will return the currently tracked value in decimal time"""

    hours_without_timer = Column(Float, nullable=True)


    """

    Started-At	Start timestamp of timer (if timestamps are enabled)
    Ended-At	End timestamp of timer (if timestamps are enabled)


    """

    def __str__(self, *args, **kwargs):
        super_str = super(DayEntry, self).__str__(args, kwargs)
        local_str = "{date} - project_id: {project_id} - time: {hours}".format(
            date=self.spent_at, project_id=self.project_id, hours=self.hours)
        return super_str + ' (' + local_str + ')'


class TaskAssignment(HarvestDBType):
    """

    ::

        "task_assignment": {
            "project_id": 3554414,
            "task_id": 2086199,
            "billable": true,
            "deactivated": true,
            "hourly_rate": 100,
            "budget": null,
            "id": 37453419,
            "created_at": "2013-04-30T20:28:12Z",
            "updated_at": "2013-08-01T22:11:11Z",
            "estimate": null
          }

    .. seealso:: http://help.getharvest.com/api/tasks-api/tasks/task-assignments/
    """
    __tablename__ = 'task_assignments'

    id = Column(Integer, primary_key=True)

    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=False)

    task_id = Column(Integer, ForeignKey('tasks.id'),  primary_key=False)

    linked_task = relationship('Task',
                        back_populates="linked_task_assignments")  # type: Task

    linked_project = relationship('Project',
                           back_populates="linked_task_assignments")  # type: Project

    billable = Column(Boolean)

    deactivated = Column(Boolean)

    hourly_rate = Column(Integer)

    budget = Column(Integer, nullable=True)

    created_at = Column(String)

    updated_at = Column(String)

    estimate = Column(Integer, nullable=True)


class Task(HarvestDBType):
    """
        ::

        "task": {
            "id": 2086199,
            "name": "Admin",
            "billable_by_default": false,
            "created_at": "2013-04-30T20:28:12Z",
            "updated_at": "2013-08-14T22:25:42Z",
            "is_default": true,
            "default_hourly_rate": 0,
            "deactivated": true
        }

    .. seealso:: http://help.getharvest.com/api/tasks-api/tasks/create-show-tasks/
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    billable_by_default = Column(Boolean)

    created_at = Column(String)

    updated_at = Column(String)

    is_default = Column(Boolean)

    default_hourly_rate = Column(Integer)

    deactivated = Column(Boolean)

    linked_task_assignments = relationship('TaskAssignment', back_populates="linked_task") # type: List[TaskAssignment]

    linked_day_entries = relationship('DayEntry',
                               back_populates="linked_task")  # type: List[DayEntry]


class Contact(HarvestDBType):
    """
    Data class for Harvest Contacts.

    Maps to and from this example JSON

    .. code-block:: json

        "contact": {
            "id": 2937808,
            "client_id": 1661738,
            "first_name": "Client",
            "last_name": "Contact",
            "email": "customer@example.com",
            "phone_office": "800-123-4567",
            "phone_mobile": "800-123-4567",
            "fax": "800-123-4567",
            "title": "Mrs",
            "created_at": "2013-08-12T15:30:14Z",
            "updated_at": "2015-04-16T18:07:28Z"
        }

    .. seealso:: http://help.getharvest.com/api/clients-api/clients/using-the-client-contacts-api/
    """
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)

    client_id = Column(Integer, ForeignKey('clients.id'), primary_key=False)

    first_name = Column(String)

    last_name = Column(String)

    email = Column(String)

    phone_office = Column(String)

    phone_mobile = Column(String)

    fax = Column(String)

    title = Column(String)

    created_at = Column(String)

    updated_at = Column(String)

    linked_client = relationship('Client', back_populates="linked_contacts")  # type: Client

    def __str__(self, *args, **kwargs):
        super_str = super(Contact, self).__str__(args, kwargs)
        local_str = '{firstName} {lastName} <{email}>'.format(
            firstName=self.first_name, lastName=self.last_name,
            email=self.email)
        return super_str + ' ' + local_str


class Invoice(HarvestDBType):
    """

    ::

        "invoice": {
            "id": 6763297,
            "client_id": 1929151,
            "period_start": null,
            "period_end": null,
            "number": "1",
            "issued_at": "2015-04-22",
            "due_at": "2015-04-22",
            "amount": 100,
            "currency": "United States Dollar - USD",
            "state": "open",
            "notes": "",
            "purchase_order": "",
            "due_amount": 100,
            "due_at_human_format": "upon receipt",
            "created_at": "2015-04-21T18:41:58Z",
            "updated_at": "2015-04-21T18:42:02Z",
            "tax": null,
            "tax_amount": 0,
            "subject": "",
            "recurring_invoice_id": null,
            "tax2": null,
            "tax2_amount": 0,
            "client_key": "43d9342a017e262c33a395ef3b9dca294f736792",
            "estimate_id": null,
            "discount": null,
            "discount_amount": 0,
            "retainer_id": null,
            "created_by_id": 508343,
            "csv_line_items": "kind,description,quantity,unit_price,amount,taxed,taxed2,project_id\\nProduct,A description,1.00,100.00,100.0,false,false,\\n"
        }



        Invoice Types
            Type	    Description
            free-form   Creates free form invoice. Line items added with csv-line-items
            project     Gathers hours & expenses from Harvest grouped by projects.
            task        Gathers hours & expenses from Harvest grouped by task.
            people      Gathers hours & expenses from Harvest grouped by person.
            detailed    Uses a line item for each hour & expense entry, including detailed notes.
    """

    __tablename__ = 'invoices'

    # Parameters Generated By Harvest
    id = Column(Integer, primary_key=True)

    client_key = Column(String)
    """Value to generate URL to client dashboard. (Example: https://YOURACCOUNT.harvestapp.com/clients/invoices/{CLIENTKEY})"""

    estimate_id = Column(String, nullable=True)
    """This value will exist if an estimate was converted into an invoice."""

    retainer_id = Column(Integer, nullable=True)
    """This value will exist if the invoice was created from a retainer."""

    recurring_invoice_id = Column(String, nullable=True)
    """This value will exist if the invoice is recurring, and automatically generated."""

    created_by_id = Column(Integer, ForeignKey('users.id'), primary_key=False)
    """User ID of the invoice creator."""

    linked_creator = relationship('User', back_populates='linked_invoices') # type: User

    state = Column(String)
    """Updated when invoice is created, sent, paid, late, or written off. Options: draft, paid, late, sent, written-off."""

    created_at = Column(String)
    """Date invoice was created. (Example: 2015-04-09T12:07:56Z)"""

    updated_at = Column(String)
    """Date invoice was last updated. (Example: 2015-04-09T12:07:56Z)"""

    # User Editable Parameters
    client_id = Column(Integer, ForeignKey('clients.id'), primary_key=False)
    """A valid client-id"""

    linked_client = relationship('Client', back_populates='linked_invoices') #type: Client

    period_start = Column(String)
    """Date for included project hours. (Example: 2015-04-22)"""

    period_end = Column(String)
    """End date for included project hours. (Example: 2015-05-22)"""

    number = Column(String, nullable=True)
    """Optional invoice number. If no value is set, the number will be automatically generated."""

    issued_at = Column(String)
    """ Invoice creation date. (Example: 2015-04-22)"""

    due_at = Column(String)

    amount = Column(Integer)

    currency = Column(String)
    """A valid currency format (Example: United States Dollar - USD). Optional, and will default to the client currency if no value is passed. Click here for a list of supported currencies"""

    notes = Column(String, nullable=True)
    """Optional invoice notes."""

    purchase_order = Column(String, nullable=True)
    """Optional purchase order number."""

    due_amount = Column(Integer)

    due_at_human_format = Column(String)
    """Invoice due date. Acceptable formats are NET N where N is the number of days until the invoice is due."""

    tax = Column(String, nullable=True)
    """First tax rate for created invoice. Optional. Account default used otherwise."""

    tax_amount = Column(Integer)

    subject = Column(String)
    """Optional invoice subject."""

    tax2 = Column(String, nullable=True)
    """Second tax rate for created invoice. Optional. Account default used otherwise."""

    tax2_amount = Column(Integer)

    discount = Column(String, nullable=True)
    """Optional value to discount invoice total."""

    discount_amount = Column(Integer)

    csv_line_items = Column(String)
    """Used to create line items in free-form invoices. Entries should have their entries enclosed in quotes when they contain extra commas. This is especially important if you are using a number format which uses commas as the decimal separator."""

    expense_summary_kind = Column(String)
    """Summary type for expenses in an invoice. Options: project, people, category, detailed."""

    kind = Column(String)
    """Invoice type. Options: free-form, project, task, people, detailed. (See Invoice Types)"""

    projects_to_invoice = Column(String)
    """Comma separated project IDs to gather data from, unused for free-form invoices."""

    import_hours = Column(String)
    """Hours to import into invoices. Options: all(import all hours), yes (import hours using period-start, period-end), no (do not import hours)."""

    import_expense = Column(String)
    """Expenses to import into invoices. Options: all(import all expenses), yes (import expenses using expense-period-start, expense-period-end), no (do not import expenses)."""

    expense_period_start = Column(String)
    """Date for included project expenses. (Example: 2015-04-22)"""

    expense_period_end = Column(String)
    """End date for included project expenses. (Example: 2015-05-22)"""

    linked_expense = relationship('Expense', back_populates="linked_invoice") # type:Expense


class ExpenseCategory(HarvestDBType):
    """

    ::

        expense_category": {
                "id": 1338056,
                "name": "Entertainment",
                "unit_name": null,
                "unit_price": null,
                "created_at": "2015-04-17T20:28:12Z",
                "updated_at": "2015-04-17T20:28:12Z",
                "deactivated": false
        }
    """
    __tablename__ = 'expense_categories'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    unit_name = Column(String, nullable=True)

    unit_price = Column(String, nullable=True)

    created_at = Column(String)

    updated_at = Column(String)

    deactivated = Column(Boolean)

    linked_expenses = relationship('Expense', back_populates='linked_expense_category') # type: List[Expense]


class Expense(HarvestDBType):
    """

    ::

        "expense": {
            "id": 7631396,
            "total_cost": 14,
            "units": 14,
            "created_at": "2015-04-21T14:20:34Z",
            "updated_at": "2015-04-21T14:34:27Z",
            "project_id": 3554414,
            "expense_category_id": 1338061,
            "user_id": 508343,
            "spent_at": "2015-04-17",
            "is_closed": false,
            "notes": "Your Updated Expense",
            "invoice_id": 0,
            "billable": false,
            "company_id": 210377,
            "has_receipt": false,
            "receipt_url": "",
            "is_locked": false,
            "locked_reason": null
        }

    """

    __tablename__ = 'expense'

    id = Column(Integer, primary_key=True)

    total_cost = Column(Integer)
    """integer value for the expense entry"""

    units = Column(Integer)
    """integer value for use with an expense calculated by unit price (Example: Mileage)"""

    created_at = Column(String)

    updated_at = Column(String)

    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=False)
    """Valid and existing project ID"""

    linked_project = relationship('Project', back_populates="linked_expenses") # type: Project

    expense_category_id = Column(Integer, ForeignKey('expense_categories.id'), primary_key=False)
    """Valid and existing expense category ID"""

    linked_expense_category = relationship('ExpenseCategory',back_populates='linked_expenses') # type: ExpenseCategory

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=False)

    linked_user = relationship('User', back_populates="linked_expenses") # type: User

    spent_at = Column(String)
    """Date for expense entry"""

    is_closed = Column(Boolean)

    notes = Column(String)
    """Expense entry notes"""

    invoice_id = Column(Integer, ForeignKey('invoices.id'), primary_key=False)

    linked_invoice = relationship('Invoice', back_populates="linked_expense") # type: Invoice

    billable = Column(Boolean)
    """Options: true, false. Note: Only expenses that are billable can be invoiced."""

    company_id = Column(Integer)  # TODO foreign key

    has_receipt = Column(Boolean)

    receipt_url = Column(String)

    is_locked = Column(Boolean)

    locked_reason = Column(String, nullable=True)


class Day(HarvestType):
    """

    ::

        {
            'day_entries': [],
            'for_day': '2016-06-28',
        }
    """

    def __init__(self, day_entries: List[DayEntry] = None,
                 for_day: str = None):
        super().__init__()
        self.day_entries = day_entries
        self.for_day = for_day
