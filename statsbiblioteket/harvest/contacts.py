from statsbiblioteket.harvest.rest import Rest

class Contacts(Rest):
    # Client Contacts

    def contacts(self, updated_since=None):
        """
        Get list of all contacts (optionally since a given date)
        http://help.getharvest.com/api/clients-api/clients/using-the-client-contacts-api/
        """
        url = '/contacts'
        params = {}
        if updated_since is not None:
            params['updated_since'] = updated_since
        return self._get(url,params=params)

    def get_contact(self, contact_id):
        """
        Get a single contact by contact_id
        http://help.getharvest.com/api/clients-api/clients/using-the-client-contacts-api/#get-a-client-contact
        """
        url = '/contacts/{0}'.format(contact_id)
        return self._get(url)

    def create_contact(self, new_contact_id, fname, lname, **kwargs):
        """
        Create a new contact
        http://help.getharvest.com/api/clients-api/clients/using-the-client-contacts-api/#create-a-new-client-contact
        """
        url = '/contacts/{0}'.format(new_contact_id)
        kwargs.update({'first-name': fname, 'last-name': lname})
        return self._post(url, data=kwargs)

    def client_contacts(self, client_id, updated_since=None):
        """
        Get all contacts for a client by client_id (optionally specifing anupdated_since data)
        http://help.getharvest.com/api/clients-api/clients/using-the-client-contacts-api/#get-all-contacts-for-a-client
        """
        url = '/clients/{0}/contacts'.format(client_id)
        params = {}
        if updated_since is not None:
            params['updated_since'] = updated_since
        return self._get(url,params=params)

    def update_contact(self, contact_id, **kwargs):
        """
        Update a contact
        http://help.getharvest.com/api/clients-api/clients/using-the-client-contacts-api/#update-a-client-contact
        """
        url = '/contacts/{0}'.format(contact_id)
        return self._put(url, data=kwargs)

    def delete_contact(self, contact_id):
        """
        Delete a contact
        http://help.getharvest.com/api/clients-api/clients/using-the-client-contacts-api/#delete-a-client-contact
        """
        url = '/contacts/{0}'.format(contact_id)
        return self._delete(url)
