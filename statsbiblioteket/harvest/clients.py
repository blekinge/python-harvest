import typing

from statsbiblioteket.harvest.harvest_types import Client
from statsbiblioteket.harvest.rest import Rest

class Clients(Rest):
    # Clients

    def clients(self, updated_since=None) -> typing.List[Client]:
        """
        Get clients (optionally update since a date)
        http://help.getharvest.com/api/clients-api/clients/using-the-clients-api/#get-all-clients
        """
        url = '/clients'
        params = {}
        if updated_since is not None:
            params['updated_since'] = updated_since
        return self._get(url,params=params)

    def get_client(self, client_id) -> Client:
        """
        Get a single client by client_id
        http://help.getharvest.com/api/clients-api/clients/using-the-clients-api/#get-a-single-client
        """
        return self._get('/clients/{0}'.format(client_id))

    def create_client(self, **kwargs):
        """
        Create a new client
        client.create_client(client={"name":"jo"})
        http://help.getharvest.com/api/clients-api/clients/using-the-clients-api/#create-a-new-client
        """
        url = '/clients/'
        return self._post(url, data=kwargs)

    def update_client(self, client_id, **kwargs):
        """
        Update a client
        http://help.getharvest.com/api/clients-api/clients/using-the-clients-api/#update-a-client
        """
        url = '/clients/{0}'.format(client_id)
        return self._put(url, data=kwargs)

    def toggle_client_active(self, client_id):
        """
        Toggle the active flag of a client
        http://help.getharvest.com/api/clients-api/clients/using-the-clients-api/#activate-or-deactivate-an-existing-client
        """
        url = '/clients/{0}/toggle'.format(client_id)
        return self._post(url)

    def delete_client(self, client_id):
        """
        Delete a client
        http://help.getharvest.com/api/clients-api/clients/using-the-clients-api/#delete-a-client
        """
        url = '/clients/{0}'.format(client_id)
        return self._delete(url)
