import json
import time

from InstagramFakeAPI.v159.mixin.request import RequestCustom
from InstagramFakeAPI.lib.util.crypto import Crypto

#from lib.util.solver import ChallengeSolverMessages


class PreLoginAction(RequestCustom):

    def __init__(self):
        super(PreLoginAction, self).__init__('','')
        self.__log.debug('Start PreLogin Class')
        self.__key_id = None
        self.__pub_key = None
        self.__csrf = None

    def start_pre(self):
        self.__sync()
        time.sleep(2)
        # self.__contact_point_prefill()
        # time.sleep(2)
        # self.__qe_sync()
        # time.sleep(2)
        # self.__launcher_sync()
        # time.sleep(2)
        # self.__get_prefill_candidates()
        pass

    def __contact_point_prefill(self):
        self.proxy_str = self.account.get('proxy', None)
        self.__log.debug('Start contact_point_prefill')
        body = {'signed_body': 'SIGNATURE.{"phone_id":"' + self.phone_id(self.username) + '","usage":"prefill"}'}
        self.post('/accounts/contact_point_prefill/', self.default(), body)
        self.__log.debug(self.last_json)
        self.__log.debug(self.cookies)
        pass

    def __qe_sync(self):
        self.__log.debug('Start __qe_sync')
        self.proxy_str = self.account.get('proxy', None)
        header = {**self.default(), **{'X-DEVICE-ID': self.guid_id(self.username)}}
        body = {'signed_body': 'SIGNATURE.{' + '"id":"{}","server_config_retrieval":"1","experiments":"{}"'.format(
            header['X-IG-Device-ID'], self.EXPERIMENTS) + '}'}
        self.post('/qe/sync/', header, body)
        self.__key_id = self.headers.get('ig-set-password-encryption-key-id')
        self.__pub_key = self.headers.get('ig-set-password-encryption-pub-key')
        pass

    def __sync(self):
        self.__log.debug('Start __sync')
        self.proxy_str = self.account.get('proxy', None)
        header = {**self.default(), **{'X-DEVICE-ID': self.guid_id(self.username)}}
        body = {'signed_body': 'SIGNATURE.{' + '"id":"{}","server_config_retrieval":"1","experiments":"{}"'.format(
            header['X-IG-Device-ID'], self.EXPERIMENTS) + '}'}
        self.post('/qe/sync/', header, body)
        self.__key_id = self.headers.get('ig-set-password-encryption-key-id')
        self.__pub_key = self.headers.get('ig-set-password-encryption-pub-key')
        pass

    def __launcher_sync(self):
        self.__log.debug('Start __launcher_sync')
        self.proxy_str = self.account.get('proxy', None)
        header = self.default()
        body = {'signed_body': 'SIGNATURE.{' + '"id":"{}","server_config_retrieval":"1"'.format(
            self.guid_id(self.username)) + '}'}
        self.post('/launcher/sync/', header, body)

    def __get_prefill_candidates(self):
        self.__log.debug('Start __get_prefill_candidates')
        self.proxy_str = self.account.get('proxy', None)
        header = {**self.default(), **{'IG-U-DS-USER-ID': ''}}
        array = {
            'android_device_id': self.android_id(self.username),
            'client_contact_points': json.dumps(
                [{"type": "omnistring", "value": "endemio", "source": "last_login_attempt"}]),
            'phone_id': self.phone_id(self.username),
            'usages': json.dumps(["account_recovery_omnibox"]),
            'device_id': self.guid_id(self.username)
        }
        body = {'signed_body': 'SIGNATURE.' + json.dumps(array)}
        self.post('/accounts/get_prefill_candidates/', header, body)
        self.__csrf = self.extract_cookie('csrftoken')

    @property
    def key_id(self):
        return self.__key_id

    @property
    def pub_key(self):
        return self.__pub_key

    @property
    def csrf(self):
        return self.__csrf


class LoginAction(PreLoginAction, Crypto):
    def __init__(self):
        self.__log.debug('Start LoginAction')
        super(LoginAction, self).__init__()
        pass

    def login(self):
        return self.__login()

    def repeat(self):
        self.__login(True)

    def challenge_solving(self, response_message):

        self.__log.debug(self.device)

        header = {**self.default(), **{'X-Tigon-Is-Retry': "True", 'IG-INTENDED-USER-ID': "0"}}
        header.pop('Content-Type')
        try:
            header.pop('IG-U-DS-USER-ID')
        except:
            pass


        self.__log.debug('Stop')

    def __login(self, is_repeat=False) -> dict:

        self.__log.debug(self.device)

        if not self.username:
            raise Exception('Username not exists')

        if not self.password:
            raise Exception('Password not exists')

        if not self.device:
            raise ValueError('Update device json')

        if not self.user_agent:
            raise Exception('User-Agent not exists')

        if self.extract_cookie('sessionid') or self.bearer:
            self.__log.debug('Has already Cookie')
            self.is_logged_in = True
            return {}

        self.__log.debug('Start Login')
        self.start_pre()

        time.sleep(1)

        # Create login signed body
        array = {
            'jazoest': self.jazoest(self.phone_id(self.username)),
            'country_codes': json.dumps([{"country_code": "1", "source": ["default"]}]),
            'phone_id': self.phone_id(self.username),
            'enc_password': self.encrypt_password(self.password, self.pub_key, self.key_id, int(time.time())),
            "username": self.username,
            "guid": self.guid_id(self.username),
            "_csrftoken": self.csrf,
            "device_id": self.android_id(self.username),
            "adid": "",  # not set on pre-login
            "google_tokens": "[]",
            "login_attempt_count": 0,  # TODO maybe cache this somewhere?
        }

        body = {'signed_body': 'SIGNATURE.' + json.dumps(array)}

        header = {**self.default(),**{'Cookie': "; ".join([str(x)+"="+str(y) for x,y in self.cookies.items()])}}

        self.post('/accounts/login/', header, body, True)

        return self.last_json

