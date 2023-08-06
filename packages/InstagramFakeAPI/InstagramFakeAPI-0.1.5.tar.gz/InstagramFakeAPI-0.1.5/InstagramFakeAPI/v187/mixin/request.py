import logging
import requests
import json
from urllib.parse import urlencode

from InstagramFakeAPI.lib.mixin.request import Request
from ..utils.header import Header

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RequestCustom(Request, Header):

    def __init__(self, logger:logging, proxy, salt):

        self.log.debug('RequestCustom')
        Request.__init__(self, logger, proxy)
        Header.__init__(self, logger, salt)

        self.__key_id = None
        self.__pub_key = None
        self.__csrf = None

    def contact_point_prefill(self):
        self.proxy_str = self.account.get('proxy', None)
        self.log.debug('Start contact_point_prefill')
        body = {'signed_body': 'SIGNATURE.{"phone_id":"' + self.phone_id(self.username) + '","usage":"prefill"}'}
        self.post('/accounts/contact_point_prefill/', self.default(), body)
        self.log.debug(self.last_json)
        self.log.debug(self.cookies)
        pass

    def launcher_sync(self):
        self.log.debug('Start __launcher_sync')
        self.proxy_str = self.account.get('proxy', None)
        self.mid = self.last_header.get('ig-set-x-mid', self.mid)
        header = self.default()
        body = {'signed_body': 'SIGNATURE.{' + '"id":"{}","server_config_retrieval":"1"'.format(
            self.guid_id(self.username)) + '}'}
        self.post('/launcher/sync/', header, body)
        self.log.debug(self.last_json)
        self.log.debug(self.cookies)
        pass

    def qe_sync(self):
        self.log.debug('Start __qe_sync')
        self.proxy_str = self.account.get('proxy', None)
        self.mid = self.last_header.get('ig-set-x-mid', self.mid)
        header = {**self.default(), **{'X-DEVICE-ID': self.guid_id(self.username)}}
        body = {'signed_body': 'SIGNATURE.{' + '"id":"{}","server_config_retrieval":"1","experiments":"{}"'.format(
            header['X-IG-Device-ID'], self.EXPERIMENTS) + '}'}
        self.post('/qe/sync/', header, body)
        self.__key_id = self.last_header.get('ig-set-password-encryption-key-id', self.__key_id)
        self.__pub_key = self.last_header.get('ig-set-password-encryption-pub-key', self.__pub_key)
        pass

    def get_prefill_candidates(self):
        self.log.debug('Start __get_prefill_candidates')
        self.proxy_str = self.account.get('proxy', None)
        self.mid = self.last_header.get('ig-set-x-mid', self.mid)
        header = {**self.default(), **{'IG-U-DS-USER-ID': ''}}
        array = {
            'android_device_id': self.android_id(self.username),
            'phone_id': self.phone_id(self.username),
            'usages': json.dumps(["account_recovery_omnibox"]),
            'device_id': self.guid_id(self.username)
        }
        body = {'signed_body': 'SIGNATURE.' + json.dumps(array)}
        self.post('/accounts/get_prefill_candidates/', header, body)
        self.__csrf = self.extract_cookie('csrftoken')

    def launcher_sync_after_login(self, user_id):
        self.log.debug('Start __launcher_sync')
        self.proxy_str = self.account.get('proxy', None)
        self.user_id = user_id
        header = self.authorized()
        body = {'signed_body': 'SIGNATURE.{' + '"id":"{}", "_uid":"{}","server_config_retrieval":"1"'.format(
            user_id, user_id) + '}'}
        self.post('/launcher/sync/', header, body, True)
        self.log.debug(self.last_json)
        self.log.debug(self.cookies)
        pass

    def request_chalenge_step_1(self, path: str):
        self.log.debug('Start Challenge 1')
        self.get(path, self.default(), None)

    def request_chalenge_step_2(self, path: str, header, body):
        self.log.debug('Start Challenge 2')
        self.__send_challenge_post(path, header, body)

    def request_chalenge_step_3(self, path: str, header, body):
        self.log.debug('Start Challenge 3')
        self.__send_challenge_post(path, header, body)

    def __send_challenge_post(self, path, header, body):
        self.log.debug('Start __get_prefill_candidates')
        self.proxy_str = self.account.get('proxy', None)
        self.mid = self.last_header.get('ig-set-x-mid', self.mid)
        self.post(path, header, body)

    def logout(self):

        body = {
            'phone_id': self.phone_id(self.username),
            '_csrftoken': self.csrf,
            'guid': self.guid_id(self.username),
            'device_id': self.android_id(self.username),
            '_uuid': self.guid_id(self.username),
            'one_tap_app_login': 'true'
        }

        header = {**self.default(), **{'IG-U-DS-USER-ID': str(self.user_id)}}

        self.post('/accounts/logout/', header, urlencode(body))

        self.log.debug(self.last_json)

    def check_proxy(self, proxy):
        self.get('https://www.instagram.com/', None, None)


    @property
    def key_id(self):
        return self.__key_id

    @property
    def pub_key(self):
        return self.__pub_key

    @property
    def csrf(self):
        return self.__csrf