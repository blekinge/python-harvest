from statsbiblioteket.harvest.rest import Rest


class People(Rest):
    # People

    def people(self):
        """
        Get all the people
        http://help.getharvest.com/api/users-api/users/managing-users/
        """
        url = '/people'
        return self._get(url)

    def get_person(self, person_id):
        """
        Get a particular person by person_id
        """
        url = '/people/{0}'.format(person_id)
        return self._get(url)

    def toggle_person_active(self, person_id):
        """
        Toggle the active flag of a person
        http://help.getharvest.com/api/users-api/users/managing-users/#toggle-an-existing-user
        """
        url = '/people/{0}/toggle'.format(person_id)
        return self._get(url)

    def delete_person(self, person_id):
        """
        Delete a person
        http://help.getharvest.com/api/users-api/users/managing-users/#delete-a-user
        """
        url = '/people/{0}'.format(person_id)
        return self._delete(url)
