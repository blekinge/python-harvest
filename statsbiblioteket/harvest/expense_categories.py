from statsbiblioteket.harvest.rest import Rest


class ExpenseCategories(Rest):
    # Expense Categories

    @property
    def expense_categories(self):
        """ expense categories property """
        return self._get('/expense_categories')

    def create_expense_category(self, new_expense_category_id, **kwargs):
        """
        Create an expense category
        """
        url = '/expense_categories/{0}'.format(new_expense_category_id)
        return self._post(url, data=kwargs)

    def update_expense_category(self, expense_category_id, **kwargs):
        """
        Update an existing expense category
        """
        url = '/expense_categories/{0}'.format(expense_category_id)
        return self._put(url, data=kwargs)

    def get_expense_category(self, expense_category_id):
        """
        Get an expense category by expense_category_id
        """
        url = '/expense_categories/{0}'.format(expense_category_id)
        return self._get(url)

    def delete_expense_category(self, expense_category_id):
        """
        Delete an expense category
        """
        url = '/expense_categories/{0}'.format(expense_category_id)
        return self._delete(url)

    def toggle_expense_category_active(self, expense_category_id):
        """
        Toggle the active flag of an expense category
        """
        url = '/expense_categories/{0}/toggle'.format(expense_category_id)
        return self._get(url)
