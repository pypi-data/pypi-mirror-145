import logging
import requests
import time
import random
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from functools import wraps

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def decorator_request():
    def wrapper(f):
        @wraps(f)
        def wrapped(self, endpoint, header, data=None, is_login=False, params=None, *args, **kwargs):

            if header:
                self.s.headers.update(header)

            if self.proxy_str:
                self.s.proxies.update({'http': self.proxy_str, 'https': self.proxy_str})

            counter_429 = 0
            counter_proxy = 0

            while True:

                response = None
                self.log.debug('*' * 80)
                self.log.debug('Send request to {}'.format(self.API_URL + endpoint))
                self.log.debug('-' * 80)
                self.log.debug('Proxy to {}'.format(self.proxy_str))
                self.log.debug('-' * 80)
                self.log.debug('Data to {}'.format(json.dumps(data, indent=4)))
                self.log.debug('-' * 80)
                self.log.debug('Header to {}'.format(json.dumps(header, indent=4)))

                try:
                    response = f(self, endpoint, header, data, is_login, params, *args, **kwargs)

                    self.log.debug('.' * 80)
                    self.log.debug('Response code {}, answer {}'.format(response.status_code, response.text))

                    if response.status_code in [200, 400, 403, 404, 429]:
                        break

                    if response.status_code == 429 and is_login:
                        counter_429 += 1
                        time.sleep(10)

                    if counter_429 > 3:
                        break

                    time.sleep(5)
                except requests.exceptions.ProxyError as err:
                    self.log.warning('ProxyError, repeating {}'.format(err))
                    counter_proxy+=1
                except Exception as e:
                    self.log.error('Except on SendRequest (wait 60 sec and resend): {}'.format(e))
                    self.delay_long()

                if counter_proxy > 4:
                    raise requests.exceptions.ProxyError('Proxy error for {}'.format(self.proxy_str))

                time.sleep(4)

                self.log.debug('-' * 80)
                self.log.debug('Response Cookies to {}'.format(self.s.cookies.get_dict()))
                self.log.debug('-' * 80)
                if response:
                    self.log.debug('Response Header to {}'.format(response.headers, indent=4))
                    self.log.debug('*' * 80)

            self.last_header = dict(response.headers)
            self.cookies = self.s.cookies.get_dict()

            if response.status_code == 200:
                if 'ig-set-x-mid' in self.headers:
                    self.mid = self.headers['ig-set-x-mid']
                if is_login:
                    self.is_logged_in = True
            elif response.status_code == 400:
                if not is_login:
                    raise ValueError('Response 400 with message {}'.format(response.text))
            elif response.status_code == 404:
                raise PageNotFound('Response 404 for {}'.format(self.API_URL + endpoint))
            elif response.status_code == 403:
                self.log.warning(response.content)
                raise NonAuthorizedRequest('Not logging in')
            elif response.status_code == 500:
                self.log.warning(response.content)
                raise BaseException('Wrong answer')
            else:
                self.log.debug(
                    "Request return " + str(response.status_code) + " error!, answer {}".format(response.text))

            # logging.debug('Header is {}'.format(json.dumps(dict(response.request.headers), indent=4)))

            try:
                self.log.debug('Set json')
                self.last_json = json.loads(response.text)
            except json.JSONDecodeError:
                self.log.debug(response.text)
                raise

        return wrapped

    return wrapper


class Request:
    VERIFY = False
    API_URL = 'https://i.instagram.com/api/v1'

    def __init__(self, logger: logging, proxy):
        self.logger = logger

        self.log.debug('Abstarct Request')
        self.s = requests.Session()
        self.__proxy = proxy
        self.__json = None
        self.__headers = None
        self.__raw = None
        self.__is_logged_in = True
        self.__last_connection_unixtime = 0
        self.__cookies = {}
        pass

    SUPPORTED_CAPABILITIES_NEW = [
        {
            "name": "SUPPORTED_SDK_VERSIONS",
            "value": "108.0,109.0,110.0,111.0,112.0,113.0,114.0,115.0,116.0,117.0,118.0,119.0,120.0,121.0,122.0,123.0,124.0,125.0,126.0,127.0"
        },
        {"name": "FACE_TRACKER_VERSION", "value": "14"},
        {"name": "segmentation", "value": "segmentation_enabled"},
        {"name": "COMPRESSION", "value": "ETC2_COMPRESSION"},
        {"name": "world_tracker", "value": "world_tracker_enabled"},
        {"name": "gyroscope", "value": "gyroscope_enabled"}
    ]

    SUPPORTED_CAPABILITIES = [
        {
            "name": "SUPPORTED_SDK_VERSIONS",
            "value": "66.0,67.0,68.0,69.0,70.0,71.0,72.0,73.0,74.0,75.0,76.0,77.0,78.0,79.0,80.0,81.0,82.0,83.0,84.0,85.0,86.0,87.0,88.0,89.0,90.0,91.0,92.0,93.0,94.0,95.0,96.0,97.0"
        },
        {"name": "FACE_TRACKER_VERSION", "value": "14"},
        {"name": "COMPRESSION", "value": "ETC2_COMPRESSION"},
        {"name": "world_tracker", "value": "world_tracker_enabled"}]

    @decorator_request()
    def post(self, endpoint: str, header=None, data=None, is_login=False, params=None):

        if self.cookies:
            response = self.s.post(self.API_URL + endpoint, data=data, cookies=self.cookies, verify=self.VERIFY,
                                   timeout=10)
        else:
            response = self.s.post(self.API_URL + endpoint, data=data, verify=self.VERIFY, timeout=10)
        return response

    @decorator_request()
    def get(self, endpoint: str, header=None, data=None, is_login=False, params=None):
        self.log.debug(params)
        if self.cookies:
            response = self.s.get(self.API_URL + endpoint, cookies=self.cookies, verify=self.VERIFY,
                                  params=params, timeout=10)
        else:
            response = self.s.get(self.API_URL + endpoint, verify=self.VERIFY, params=params, timeout=10)

        self.log.debug(response.request.url)
        return response

    def extract_cookie(self, field):
        if self.cookies:
            return self.cookies.get(field, '')
        return ''

    def extract_header(self, field):
        if self.headers:
            return self.headers.get(field)
        return ''

    @property
    def log(self) -> logging:
        return self.logger

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, headers: dict):
        self.__headers = {k.lower(): v for (k, v) in headers.items()}

    @property
    def cookies(self):
        return self.__cookies

    @cookies.setter
    def cookies(self, value):
        self.__cookies = value

    @property
    def proxy_str(self):
        return self.__proxy

    @proxy_str.setter
    def proxy_str(self, value: str):
        self.__proxy = value

    @staticmethod
    def delay_short():
        time.sleep(random.uniform(0.75, 3.75))

    @staticmethod
    def delay_long():
        time.sleep(60)

    @property
    def raw(self):
        return self.__raw

    @property
    def last_json(self):
        return self.__json

    @last_json.setter
    def last_json(self, value):
        self.log.debug('Added data')
        self.__json = value

    @property
    def last_header(self):
        return self.__headers

    @last_header.setter
    def last_header(self, value: dict):
        self.log.debug('Added data for headers')
        self.__headers = value

    @property
    def is_logged_in(self):
        return self.__is_logged_in

    @is_logged_in.setter
    def is_logged_in(self, status: bool):
        self.__is_logged_in = status

    def last_connection_unixtime(self) -> int:
        return self.__last_connection_unixtime
