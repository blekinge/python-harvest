import typing


class Client(object):
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

    def __init__(self, name, id=None, active=None, currency=None,
                 highrise_id=None, cache_version=None, updated_at=None,
                 created_at=None, currency_symbol=None, details=None,
                 default_invoice_timeframe=None, last_invoice_kind=None):
        """

        :param name: New client name.
        :param id:
        :param active: Determines if the client is active, or archived. Options: true, false.
        :param currency: The currency you’d like to use for the client.
        :param highrise_id: Optional Highrise ID for our legacy integration
        :param cache_version:
        :param updated_at:
        :param created_at:
        :param currency_symbol: The symbol that correlates to the selected currency.
        :param details: Additional details, normally used for address information.
        :param default_invoice_timeframe:
        :param last_invoice_kind:
        """
        super().__init__()
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

    def __init__(self, id=None, client_id=None, first_name=None,
                 last_name=None,
                 email=None, phone_office=None, phone_mobile=None, fax=None,
                 title=None, created_at=None, updated_at=None):
        super().__init__()
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
    """

    def __init__(self, client_id=None, period_start=None, period_end=None,
                 number=None, issued_at=None, due_at=None, amount=None,
                 currency=None, state=None, notes=None, purchase_order=None,
                 due_amount=None, due_at_human_format=None, created_at=None,
                 updated_at=None, tax=None, tax_amount=None, subject=None,
                 recurring_invoice_id=None, tax2=None, tax2_amount=None,
                 client_key=None, estimate_id=None, discount=None,
                 discount_amount=None, retainer_id=None, created_by_id=None,
                 csv_line_items=None, kind=None, projects_to_invoice=None,
                 import_hours=None, import_expense=None,
                 expense_period_start=None, expense_period_end=None,
                 expense_summary_kind=None):
        """
        User Editable Parameters
            :param client_id: A valid client-id
            :param period_start: Date for included project hours. (Example: 2015-04-22)
            :param period_end: End date for included project hours. (Example: 2015-05-22)
            :param number: Optional invoice number. If no value is set, the number will be automatically generated.
            :param issued_at: Invoice creation date. (Example: 2015-04-22)
            :param due_at:
            :param amount:
            :param currency: A valid currency format (Example: United States Dollar - USD). Optional, and will default to the client currency if no value is passed. Click here for a list of supported currencies
            :param notes: Optional invoice notes.
            :param purchase_order: Optional purchase order number.
            :param due_amount:
            :param due_at_human_format: Invoice due date. Acceptable formats are NET N where N is the number of days until the invoice is due.
            :param tax: First tax rate for created invoice. Optional. Account default used otherwise.
            :param tax_amount:
            :param subject: Optional invoice subject.
            :param tax2: Second tax rate for created invoice. Optional. Account default used otherwise.
            :param tax2_amount:
            :param discount: Optional value to discount invoice total.
            :param discount_amount:
            :param csv_line_items: Used to create line items in free-form invoices. Entries should have their entries enclosed in quotes when they contain extra commas. This is especially important if you are using a number format which uses commas as the decimal separator.
            :param kind: Invoice type. Options: free-form, project, task, people, detailed. (See Invoice Types)
            :param projects_to_invoice: Comma separated project IDs to gather data from, unused for free-form invoices.
            :param import_hours: Hours to import into invoices. Options: all(import all hours), yes (import hours using period-start, period-end), no (do not import hours).
            :param import_expense: Expenses to import into invoices. Options: all(import all expenses), yes (import expenses using expense-period-start, expense-period-end), no (do not import expenses).
            :param expense_period_start: Date for included project expenses. (Example: 2015-04-22)
            :param expense_period_end: End date for included project expenses. (Example: 2015-05-22)
            :param expense_summary_kind: Summary type for expenses in an invoice. Options: project, people, category, detailed.

        Parameters Generated By Harvest
            :param client_key:	Value to generate URL to client dashboard. (Example: https://YOURACCOUNT.harvestapp.com/clients/invoices/{CLIENTKEY})
            :param estimate_id:	This value will exist if an estimate was converted into an invoice.
            :param retainer_id: This value will exist if the invoice was created from a retainer.
            :param recurring_invoice_id:	This value will exist if the invoice is recurring, and automatically generated.
            :param created_by_id:   User ID of the invoice creator.
            :param updated_at:	    Date invoice was last updated. (Example: 2015-04-09T12:07:56Z)
            :param created_at:      Date invoice was created. (Example: 2015-04-09T12:07:56Z)
            :param state:           Updated when invoice is created, sent, paid, late, or written off. Options: draft, paid, late, sent, written-off.


        Invoice Types
            Type	    Description
            free-form   Creates free form invoice. Line items added with csv-line-items
            project     Gathers hours & expenses from Harvest grouped by projects.
            task        Gathers hours & expenses from Harvest grouped by task.
            people      Gathers hours & expenses from Harvest grouped by person.
            detailed    Uses a line item for each hour & expense entry, including detailed notes.

        """
        super().__init__()
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
        self.expense_summary_kind = expense_summary_kind
        self.kind = kind
        self.projects_to_invoice = projects_to_invoice
        self.import_hours = import_hours
        self.import_expense = import_expense
        self.period_start = period_start
        self.period_end = period_end
        self.expense_period_start = expense_period_start
        self.expense_period_end = expense_period_end


class ExpenseCategory(object):
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

    def __init__(self, id=None, name=None, unit_name=None, unit_price=None,
                 created_at=None, updated_at=None, deactivated=None):
        super().__init__()
        self.id = id
        self.name = name
        self.unit_name = unit_name
        self.unit_price = unit_price
        self.created_at = created_at
        self.updated_at = updated_at
        self.deactivated = deactivated


class Expense(object):
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

    def __init__(self, id=None, notes: str = None, total_cost: int = None,
                 project_id=None, expense_category_id=None,
                 billable: bool = None, spent_at=None, units: int = None,
                 created_at=None, updated_at=None, user_id=None,
                 is_closed=None, invoice_id=None, company_id=None,
                 has_receipt=None, receipt_url=None, is_locked=None,
                 locked_reason=None):
        """
        :param id:
        :param notes: Expense entry notes
        :param total_cost: integer value for the expense entry
        :param project_id: Valid and existing project ID
        :param expense_category_id: Valid and existing expense category ID
        :param billable: Options: true, false. Note: Only expenses that are billable can be invoiced.
        :param spent_at: Date for expense entry
        :param units: integer value for use with an expense calculated by unit price (Example: Mileage)
        :param created_at:
        :param updated_at:
        :param user_id:
        :param is_closed:
        :param invoice_id:
        :param company_id:
        :param has_receipt:
        :param receipt_url:
        :param is_locked:
        :param locked_reason:
        """
        super().__init__()
        self.id = id
        self.total_cost = total_cost
        self.units = units
        self.created_at = created_at
        self.updated_at = updated_at
        self.project_id = project_id
        self.expense_category_id = expense_category_id
        self.user_id = user_id
        self.spent_at = spent_at
        self.is_closed = is_closed
        self.notes = notes
        self.invoice_id = invoice_id
        self.billable = billable
        self.company_id = company_id
        self.has_receipt = has_receipt
        self.receipt_url = receipt_url
        self.is_locked = is_locked
        self.locked_reason = locked_reason
        # TODO http://help.getharvest.com/api/expenses-api/expenses/add-update-expenses/#attach-receipt-image


class Project(object):
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

    def __init__(self, client_id, name, id=None, code=None,
                 active: bool = True, billable: bool = False, bill_by="project",
                 hourly_rate=None, budget=None, budget_by="project",
                 notify_when_over_budget: bool = None,
                 over_budget_notification_percentage=None,
                 over_budget_notified_at=None, show_budget_to_all: bool = None,
                 created_at=None, updated_at=None, starts_on=None,
                 ends_on=None, estimate=None, estimate_by=None,
                 hint_earliest_record_at=None, hint_latest_record_at=None,
                 notes: str = None, cost_budget=None,
                 cost_budget_include_expenses: bool = None):
        """


        :param id: Project ID
        :param client_id: Client ID for project
        :param name: Project name
        :param code: Project code
        :param active: Whether the project is active or archived. Options: true, false.
        :param billable: Whether the project is billable or not billable. Options: true, false.
        :param bill_by: The method by which the project is invoiced. Options: "project", "tasks", "people", or "none".
        :param hourly_rate: Rate for projects billed by Project Hourly Rate
        :param budget: Budget value for the project.
        :param budget_by: The method by which the project is budgeted. Options: "project" (Hours Per Project), "project_cost" (Total Project Fees), "task" (Hours Per Task), "person" (Hours Per Person), "none" (No Budget).
        :param notify_when_over_budget: Option to send notification emails when a project reaches the budget threshold set in Over-Budget-Notification-Percentage Options: true, false.
        :param over_budget_notification_percentage: Percentage value to trigger over budget email alerts.
        :param over_budget_notified_at: Date of last over budget notification. If none have been sent, this will be nil.
        :param show_budget_to_all: Option to show project budget to all employees. Does not apply to Total Project Fee projects. Options: true, false.
        :param created_at: Date of earliest record for this project. Updated every 24 hours.
        :param updated_at: Date of most recent record for this project. Updated every 24 hours.
        :param starts_on:
        :param ends_on:
        :param estimate:
        :param estimate_by:
        :param hint_earliest_record_at:
        :param hint_latest_record_at:
        :param notes:
        :param cost_budget: Budget value for Total Project Fees projects.
        :param cost_budget_include_expenses: Option for budget of Total Project Fees projects to include tracked expenses.
        """
        super().__init__()
        self.id = id
        self.client_id = client_id
        self.name = name
        self.code = code
        self.active = active
        self.billable = billable
        self.bill_by = bill_by
        self.hourly_rate = hourly_rate
        self.budget = budget
        self.budget_by = budget_by
        self.notify_when_over_budget = notify_when_over_budget
        self.over_budget_notification_percentage = over_budget_notification_percentage
        self.over_budget_notified_at = over_budget_notified_at
        self.show_budget_to_all = show_budget_to_all
        self.created_at = created_at
        self.updated_at = updated_at
        self.starts_on = starts_on
        self.ends_on = ends_on
        self.estimate = estimate
        self.estimate_by = estimate_by
        self.hint_earliest_record_at = hint_earliest_record_at
        self.hint_latest_record_at = hint_latest_record_at
        self.notes = notes
        self.cost_budget = cost_budget
        self.cost_budget_include_expenses = cost_budget_include_expenses


class DayEntry(object):
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
    """

    def __init__(self, id=None, notes=None, spent_at=None, hours=None,
                 user_id=None, project_id=None, task_id=None, created_at=None,
                 updated_at=None, adjustment_record=None,
                 timer_started_at=None, is_closed=None, is_billed=None,
                 hours_with_timer=None):
        """

        Started-At	Start timestamp of timer (if timestamps are enabled)
        Ended-At	End timestamp of timer (if timestamps are enabled)

        :param id: Time Entry ID
        :param notes: Time entry notes
        :param spent_at: Date of the time entry
        :param hours: Number of (decimal time) hours tracked in this time entry
        :param user_id: User ID that tracked this time entry
        :param project_id: Project ID that the time entry is associated with
        :param task_id:
        :param created_at: Time (UTC) and date that entry was created
        :param updated_at: Time (UTC) and date that entry was last updated
        :param adjustment_record:
        :param timer_started_at: Time (UTC) and date that timer was started (if tracking by duration)
        :param is_closed: true if the time entry has been approved via Timesheet Approval (no API support), false if un-approved
        :param is_billed: true if the time entry has been marked as invoiced, false if uninvoiced
        :param hours_with_timer: Running timers will return the currently tracked value in decimal time
        """
        super().__init__()
        self.id = id
        self.notes = notes
        self.spent_at = spent_at
        self.hours = hours
        self.user_id = user_id
        self.project_id = project_id
        self.task_id = task_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.adjustment_record = adjustment_record
        self.timer_started_at = timer_started_at
        self.is_closed = is_closed
        self.is_billed = is_billed
        self.hours_with_timer = hours_with_timer


class TaskAssignment(object):
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

    def __init__(self, id=None, project_id=None, task_id=None, billable=None,
                 deactivated=None, hourly_rate=None, budget=None,
                 created_at=None, updated_at=None, estimate=None):
        super().__init__()
        self.project_id = project_id
        self.task_id = task_id
        self.billable = billable
        self.deactivated = deactivated
        self.hourly_rate = hourly_rate
        self.budget = budget
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.estimate = estimate


class Task(object):
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

    def __init__(self, id=None, name=None, billable_by_default=None,
                 created_at=None, updated_at=None, is_default=None,
                 default_hourly_rate=None, deactivated=None):
        super(Task, self).__init__()
        self.id = id
        self.name = name
        self.billable_by_default = billable_by_default
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_default = is_default
        self.default_hourly_rate = default_hourly_rate
        self.deactivated = deactivated


class Day(object):
    """

    ::

        {
            'day_entries': [],
            'for_day': '2016-06-28',
        }
    """

    def __init__(self, day_entries: typing.List[DayEntry] = None,
                 for_day: str = None):
        super().__init__()
        self.day_entries = day_entries
        self.for_day = for_day



class User(object):
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

    def __init__(self, id=None, email=None, created_at=None, is_admin=None,
                 first_name=None, last_name=None, timezone=None,
                 is_contractor=None, telephone=None, is_active=None,
                 has_access_to_all_future_projects=None,
                 default_hourly_rate=None, department=None,
                 wants_newsletter=None, updated_at=None, cost_rate=None,
                 identity_account_id=None, identity_user_id=None):
        """


        :param id:
        :param email:
        :param created_at:
        :param is_admin: Optional: To create a new admin user.
        :param first_name:
        :param last_name:
        :param timezone: Optional: To set a timezone other than the account default.
        :param is_contractor: Optional: To create a new contractor user.
        :param telephone: Optional: Telephone number for user.
        :param is_active: Optional: If the user is active, or archived (true, false)
        :param has_access_to_all_future_projects: Optional: If true this user will automatically be assigned to all new projects.
        :param default_hourly_rate: Optional: Default rate for the user in new projects, if no rate is specified.
        :param department: Optional: Department for user.
        :param wants_newsletter:
        :param updated_at:
        :param cost_rate: Optional: Cost (internal) rate for user.
        :param identity_account_id:
        :param identity_user_id:
        """

        super().__init__()
        self.id = id
        self.email = email
        self.created_at = created_at
        self.is_admin = is_admin
        self.first_name = first_name
        self.last_name = last_name
        self.timezone = timezone
        self.is_contractor = is_contractor
        self.telephone = telephone
        self.is_active = is_active
        self.has_access_to_all_future_projects = has_access_to_all_future_projects
        self.default_hourly_rate = default_hourly_rate
        self.department = department
        self.wants_newsletter = wants_newsletter
        self.updated_at = updated_at
        self.cost_rate = cost_rate
        self.identity_account_id = identity_account_id
        self.identity_user_id = identity_user_id


