import typing

from statsbiblioteket.harvest.rest import Rest
from statsbiblioteket.harvest.typesystem.harvest_types import User


class Users(Rest):
    # People

    def users(self) -> typing.List[User]:
        """
        Get all the people
        http://help.getharvest.com/api/users-api/users/managing-users/
        """
        url = '/people'
        return self._get(url)

    def get_user(self, user_id) -> User:
        """
        Get a particular person by person_id
        """
        url = '/people/{0}'.format(user_id)
        return self._get(url)

    def toggle_user_active(self, user_id):
        """
        Toggle the active flag of a person
        http://help.getharvest.com/api/users-api/users/managing-users/#toggle-an-existing-user
        """
        url = '/people/{0}/toggle'.format(user_id)
        return self._get(url)

    def delete_user(self, user_id):
        """
        Delete a person
        http://help.getharvest.com/api/users-api/users/managing-users/#delete-a-user
        """
        url = '/people/{0}'.format(user_id)
        return self._delete(url)
