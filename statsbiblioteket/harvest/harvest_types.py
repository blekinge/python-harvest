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


class Expense_Category(object):
    """

    ::

        {
            "expense_category": {
                "id": 1338056,
                "name": "Entertainment",
                "unit_name": null,
                "unit_price": null,
                "created_at": "2015-04-17T20:28:12Z",
                "updated_at": "2015-04-17T20:28:12Z",
                "deactivated": false
            }
        }


    """

    def __init__(self, id=None, name=None, unit_name=None, unit_price=None,
                 created_at=None, updated_at=None, deactivated=None):
        super(Expense_Category, self).__init__()
        self.id = id
        self.name = name
        self.unit_name = unit_name
        self.unit_price = unit_price
        self.created_at = created_at
        self.updated_at = updated_at
        self.deactivated = deactivated


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
        super(Project, self).__init__()
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
        super(TaskAssignment, self).__init__()
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


class User(object):
    # TODO
    # {
    #     "user": {
    #         "id": 508343,
    #         "email": "user@example.com",
    #         "created_at": "2013-04-30T20:28:12Z",
    #         "is_admin": true,
    #         "first_name": "Harvest",
    #         "last_name": "User",
    #         "timezone": "Eastern Time (US & Canada)",
    #         "is_contractor": false,
    #         "telephone": "",
    #         "is_active": true,
    #         "has_access_to_all_future_projects": true,
    #         "default_hourly_rate": 0,
    #         "department": "",
    #         "wants_newsletter": true,
    #         "updated_at": "2015-04-29T14:54:19Z",
    #         "cost_rate": null,
    #         "identity_account_id": 302900,
    #         "identity_user_id": 20725
    #     }
    # }
    pass


class TimeSheet(object):
    pass


class Expense(object):
    pass


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
