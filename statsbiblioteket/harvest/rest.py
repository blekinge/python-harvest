# Internal methods
import json
import os
import sys
from json import JSONEncoder

import inflection as inflection
import requests
from requests.packages.urllib3.exceptions import HTTPError
from requests_oauthlib import OAuth2Session

from statsbiblioteket.harvest import harvest_types
from statsbiblioteket.harvest.harvest_types import DayEntry, Day, User

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

        url = '{uri}{path}'.format(uri=self.uri, path=path)

        jsonData = json.dumps(data, cls=ObjectEncoder)
        #print(jsonData)
        resp = self._session.request(method=method,
                                     url=url,
                                     data=jsonData,
                                     params=params)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise HarvestError(exc,exc.response.text)

        if resp.status_code == requests.codes.created:
            return os.path.basename(resp.headers['location'])

        if 'DELETE' not in method:
            return resp.json(object_hook=json_type_hook)
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


def isOurs(d):
    oneValue = len(d.keys()) == 1
    isDay = 'for_day' in d and 'day_entries' in d
    return oneValue or isDay


def getOurName(d):
    oneValue = len(d.keys()) == 1
    if oneValue:
        key = list(d.keys())[0]
        className = inflection.camelize(key)
        return className,d[key]

    if 'for_day' in d and 'day_entries' in d: #Special handling for Day
        day_entries = d['day_entries']
        d['day_entries'] = [wrap(Day.__name__, day_entry) for day_entry
                            in day_entries or []]
        return Day.__name__, d
    return None,d

def json_type_hook(d):
    try:
        className,values = getOurName(d)

        if className:
            return wrap(className, values)

    except:
         e = sys.exc_info()[0]
         print(e)
         raise e
    return d


def wrap(className, values):
    name___ = sys.modules[harvest_types.__name__]
    class_ = getattr(name___, className)
    object_ = class_(**values)
    #object_.__dict__ = values
    # object_.__dict__.update((k, v) for k, v in d[key] if v is not None)
    return object_


class ObjectEncoder(JSONEncoder):
    def default(self, o):
        elementName = o.__class__.__name__.lower()
        fields = {}
        fields.update((k, v) for k, v in  o.__dict__.items() if v is not None)
        encoded = {elementName: fields}
        return encoded
