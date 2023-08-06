import json
import platform
import requests
import six

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

from . import VERSION
from .error import APIError

DEFAULT_BASE_URL = 'https://www.ovex.io/api/v2'
DEFAULT_TIMEOUT = 10
PYTHON_VERSION = platform.python_version()
SYSTEM = platform.system()
ARCH = platform.machine()


class BaseClient:
    def __init__(self, api_key_id='', base_url='', timeout=0):
        """
        :type base_url: str
        :type timeout: float
        :type api_key_id: str
        """
        self.set_auth(api_key_id)
        self.set_base_url(base_url)
        self.set_timeout(timeout)

        self.session = requests.Session()

    def set_auth(self, api_key_id):
        """Provides the client with an API key and secret.

        :type api_key_id: str
        """
        self.api_key_id = api_key_id

    def set_base_url(self, base_url):
        """Overrides the default base URL. For internal use.

        :type base_url: str
        """
        if base_url == '':
            base_url = DEFAULT_BASE_URL
        self.base_url = base_url.rstrip('/')

    def set_timeout(self, timeout):
        """Sets the timeout, in seconds, for requests made by the client.

        :type timeout: float
        """
        if timeout == 0:
            timeout = DEFAULT_TIMEOUT
        self.timeout = timeout

    def do(self, method, path, req=None, auth=False, timeout_override=None):
        """Performs an API request and returns the response.

        TODO: Handle 429s

        :type method: str
        :type path: str
        :type req: object
        :type auth: bool
        """
        try:
            params = json.loads(json.dumps(req))
        except Exception:
            params = None
        headers = {}
        headers['User-Agent'] = self.make_user_agent()
        if auth:
            headers['Authorization'] = f'Bearer {self.api_key_id}'
        args = dict(timeout=self.timeout if timeout_override==None else timeout_override, params=params, headers=headers)
        url = self.make_url(path, params)
        res = self.session.request(method, url, **args)
        try:
            e = res.json()
            if 'error' in e and 'error_code' in e:
                raise APIError(e['error_code'], e['error'])
            return e
        except JSONDecodeError:
            raise Exception('ovex: unknown API error (%s)' % res.status_code)

    def make_url(self, path, params):
        """
        :type path: str
        :rtype: str
        """
        if params:
            for k, v in six.iteritems(params):
                path = path.replace('{' + k + '}', str(v))
        return self.base_url + '/' + path.lstrip('/')

    def make_user_agent(self):
        """
        :rtype: str
        """
        return "OVEXpy/%s python/%s %s %s" % \
            (VERSION, PYTHON_VERSION, SYSTEM, ARCH)