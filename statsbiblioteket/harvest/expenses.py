import typing

from statsbiblioteket.harvest.rest import Rest
from statsbiblioteket.harvest.typesystem.harvest_types import Expense


class Expenses(Rest):
    # Expense Categories

    @property
    def expenses(self) -> typing.List[Expense]:
        """ expense categories property """
        return self._get('/expenses')

    def create_expense(self, new_expense_id, **kwargs):
        # TODO types
        """
        Create an expense 
        """
        url = '/expenses/{0}'.format(new_expense_id)
        return self._post(url, data=kwargs)

    def update_expense(self, expense_id, **kwargs):
        # TODO types
        """
        Update an existing expense 
        """
        url = '/expenses/{0}'.format(expense_id)
        return self._put(url, data=kwargs)

    def get_expense(self, expense_id) -> Expense:
        """
        Get an expense  by expense__id
        """
        url = '/expenses/{0}'.format(expense_id)
        return self._get(url)

    def delete_expense_(self, expense_id):
        """
        Delete an expense 
        """
        url = '/expenses/{0}'.format(expense_id)
        return self._delete(url)

    def toggle_expense__active(self, expense_id):
        """
        Toggle the active flag of an expense 
        """
        url = '/expenses/{0}/toggle'.format(expense_id)
        return self._get(url)
