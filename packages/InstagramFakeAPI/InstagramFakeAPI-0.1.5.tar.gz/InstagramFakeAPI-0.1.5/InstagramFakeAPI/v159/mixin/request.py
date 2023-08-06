import requests
from InstagramFakeAPI.lib import Request
from InstagramFakeAPI.v159.utils.header import Header

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RequestCustom(Request, Header):

    def __init__(self, proxy, salt):
        self.__log.debug('RequestCustom')
        Request.__init__(self, proxy)
        Header.__init__(self, salt)
