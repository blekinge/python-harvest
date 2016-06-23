# Internal methods
import json
from urlparse import urlparse

import requests
from requests_oauthlib import OAuth2Session



HARVEST_STATUS_URL = 'http://www.harveststatus.com/api/v2/status.json'

class HarvestError(Exception):
    """ Custom class for Harvest exceptions """
    pass


class Rest(object):
    def __init__(self, uri, email=None, password=None, client_id=None,
                 token=None):
        """ Init method """
        self.uri = uri.rstrip('/')
        parsed = urlparse(uri)
        if not (parsed.scheme and parsed.netloc):
            raise HarvestError('Invalid harvest uri "{0}".'.format(uri))

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
            'User-Agent': 'Mozilla/5.0',  # 'TimeTracker for Linux' -- ++ << >>
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

        try:
            url = '{uri}{path}'.format(uri=self.uri, path=path)

            resp = self._session.request(method=method,
                                         url=url,
                                         data=json.dumps(data),
                                         params=params)
            resp.raise_for_status()
            if 'DELETE' not in method:
                return resp.json()
            return resp
        except Exception as exc:
            raise HarvestError(exc)


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