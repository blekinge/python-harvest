# Internal methods
import json
import os

import requests
from requests_oauthlib import OAuth2Session

from statsbiblioteket.harvest.harvest_types import json_to_harvest
from statsbiblioteket.harvest.orm_types import TypeToJSON

HARVEST_STATUS_URL = 'http://www.harveststatus.com/api/v2/status.json'


class HarvestError(Exception):
    """ Custom class for Harvest exceptions """
    pass


class Rest(object):
    def __init__(self, uri, email=None, password=None, client_id=None,
                 token=None):
        """ Init method """
        self.uri = uri.rstrip('/')

        if email and password:
            self._session = requests.Session()
            self.auth = 'Basic'
            self.email = email.strip()
            self.password = password
            self._session.auth = (self.email, self.password)
        elif client_id and token:
            self.auth = 'OAuth2'
            self.client_id = client_id
            self.token = token
            self._session = OAuth2Session(client_id=self.client_id,
                                          token=self.token)
        else:
            raise ValueError()

        self._session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0',
            # 'TimeTracker for Linux' -- ++ << >>
        })

    def _get(self, path='/', data=None, params=None):
        """
        Internal method to GET from a url
        """
        return self._request('GET', path, data, params)

    def _post(self, path='/', data=None, params=None):
        """
        Internal method to POST to a url
        """
        return self._request('POST', path, data, params)

    def _put(self, path='/', data=None, params=None):
        """
        Internal method to PUT to a url
        """
        return self._request('PUT', path, data, params)

    def _delete(self, path='/', data=None, params=None):
        """
        Internal method to DELETE a url
        """
        return self._request('DELETE', path, data, params)

    def _request(self, method='GET', path='/', data=None, params=None):
        """
        Internal method to use requests library
        """

        url = '{uri}{path}'.format(uri=self.uri, path=path)

        json_data = json.dumps(data, cls=TypeToJSON)

        resp = self._session.request(method=method, url=url, data=json_data,
                                     params=params)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise HarvestError(exc, exc.response.text)

        if resp.status_code == requests.codes.created:
            return os.path.basename(resp.headers['location'])

        if 'DELETE' not in method:
            return resp.json(object_hook=json_to_harvest)
        else:
            return resp.text

    @classmethod
    def status(cls):
        """
        Global scope status function
        """
        try:
            resp = requests.get(HARVEST_STATUS_URL)
            resp.raise_for_status()
            get = resp.json().get('status', {})
            return get
        except:
            return {}


