import logging
import json
import time
import os

from ..mixin.request import RequestCustom
from ...lib.util.crypto import Crypto


# from lib.util.solver import ChallengeSolverMessages


class PreLoginAction(RequestCustom):

    def __init__(self, logger: logging):
        super(PreLoginAction, self).__init__(logger, '', '')
        self.log.debug('Start PreLogin Class')

    def start_pre(self):
        self.contact_point_prefill()
        time.sleep(2)
        self.launcher_sync()
        time.sleep(2)
        self.qe_sync()
        time.sleep(2)
        pass


class LoginAction(PreLoginAction, Crypto):
    def __init__(self, logger: logging):
        self.log.debug('Start LoginAction')

        super(LoginAction, self).__init__(logger)
        pass

    def login(self):

        #self.check_proxy(self.proxy_str)

        status = self.login_request()

        if not status:
            return False

        if self.last_json.get('message', '') == 'challenge_required':
            self.log.debug('Challenge required')
            self.challenge_solving(self.last_json)

        elif self.last_json.get('logged_in_user', ''):
            self.log.info('Succesfully loggined')
            self.set_auth(self.last_header, None, self.mid)
            self.log.debug(json.dumps(self.last_json, indent=4))
            self.log.debug(json.dumps(self.last_header, indent=4))
            self.launcher_sync_after_login(self.last_json.get('logged_in_user')['pk'])
        else:
            logging.error('Wrong answer during loggin {}'.format(self.last_json))
            raise ValueError('Wrong answer')

        return True

    def repeat(self):
        return self.login_request(True)

    def challenge_solving(self, response_message):

        path = self.__challenge_step_1(response_message)

        code = self.__challenge_step_2(path)

        self.__challenge_step_3(code, path)

        self.log.debug('Stop')

    def __challenge_step_3(self, code, path):
        code_data = {
            "security_code": code,
            "_uuid": self.guid_id(self.username),
            "_uid": self.guid_id(self.username),
            "_csrftoken": "missing",
        }
        self.request_chalenge_step_3(path, self.default(), code_data)
        if "logged_in_user" in self.last_json:
            self.log.debug(f'Logged In "{self.username}"')
            self.log.debug(json.dumps(self.last_json, indent=4))
            self.log.debug(json.dumps(self.last_header, indent=4))
            self.log.info('Succesfully loggined')
            self.set_auth(self.last_header, None, self.mid)
        else:
            self.log.debug(json.dumps(self.last_json, indent=4))
            self.log.debug(json.dumps(self.last_header, indent=4))
            os.system("cls")
            quit()

    def __challenge_step_1(self, message):

        self.request_chalenge_step_1(message['challenge']['api_path'])

        return message['challenge']['api_path']

    def __challenge_step_2(self, path):

        if "step_data" not in self.last_json:
            self.log.debug(f"{self.last_json}")
            quit()

        self.log.info(self.last_json)
        if (
                "phone_number" in self.last_json["step_data"]
                and "email" in self.last_json["step_data"]
        ):
            self.log.info(
                f'<0> phone_number: {self.last_json["step_data"]["phone_number"]} <1> email: {self.last_json["step_data"]["email"]}'
            )
        elif "phone_number" in self.last_json["step_data"]:
            self.log.info(f'<0> phone_number: {self.last_json["step_data"]["phone_number"]}')
        elif "email" in self.last_json["step_data"]:
            self.log.info(f'<1> email: {self.last_json["step_data"]["email"]}')
        else:
            raise ValueError('<!> unknown verification method')

        choice = input(f"Choice: ")

        secure_data = {
            "choice": choice,
            "_uuid": self.guid_id(self.username),
            "_uid": self.guid_id(self.username),
            "_csrftoken": "missing",
        }

        self.request_chalenge_step_2(path, self.default(), secure_data)

        if "step_data" not in self.last_json:
            self.log.debug(f"<!> {self.last_json}")
            quit()

        self.log.debug(f'Code Sent To: "{self.last_json["step_data"]["contact_point"]}"')

        code = input(f"Enter code from email")

        return code

    def login_request(self, is_repeat=False) -> bool:

        if not self.username:
            raise Exception('Username not exists')

        if not self.password:
            raise Exception('Password not exists')

        if not self.device:
            raise ValueError('Update device json')

        if not self.user_agent:
            raise Exception('User-Agent not exists')

        if self.extract_cookie('sessionid') or self.bearer:
            self.log.debug('Has already Cookie')
            self.is_logged_in = True
            return True

        self.log.debug('Start Login')

        try:
            self.start_pre()
        except:
            return False

        time.sleep(1)

        self.log.debug(' pub {} key {}'.format(self.pub_key, self.key_id))

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

        header = {**self.default(), **{'Cookie': "; ".join([str(x) + "=" + str(y) for x, y in self.cookies.items()])}}

        self.post('/accounts/login/', header, body, True)

        return True
