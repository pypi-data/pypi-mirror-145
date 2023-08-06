class Credential:

    def __init__(self, logger, ua: str, bloks: str, cap: str):
        self.__log = logger
        self.__log.debug('Start Creds')
        self.__account = {}

        self.__language = ''
        self.__username = ''
        self.__password = ''
        self.__last_login = {}
        self.__auth = {}

        self.__device = None
        self.__connection_type_header = None
        self.__capabilities = cap
        self.__bloks_version_id = bloks
        self.__user_agent = ua

        self.__mid = ''

    @property
    def settings(self):
        return {
            'account': self.__account,
            'device': self.__device,
            'auth': self.__auth
        }

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, account: dict):
        self.__account = account if account else {}

    @property
    def abstract_auth(self) -> dict:
        return self.__auth

    @abstract_auth.setter
    def abstract_auth(self, value: dict):
        print('add')
        self.__auth = value

    @property
    def last_login(self):
        return self.__last_login

    @last_login.setter
    def last_login(self, last_login: dict):

        print(last_login)

        self.__last_login = last_login

        self.__device = self.__last_login.get('device')
        self.__account = self.__last_login.get('account')
        self.__auth = self.__last_login.get('auth')

    @property
    def language(self):
        return self.account.get('language', 'en_US')

    @property
    def device(self):
        return self.__device

    @device.setter
    def device(self, device: dict):
        self.__device = device
        self.__log.debug(self.__device)
        if self.__device:
            self.__user_agent = self.__user_agent.format(**device)

    @property
    def username(self) -> str:
        return self.__account.get('username')

    @property
    def password(self) -> str:
        return self.__account.get('password')

    @property
    def email(self) -> str:
        return self.__account.get('email_login')

    @property
    def email_password(self) -> str:
        return self.__account.get('email_pass')

    @property
    def email_host(self) -> str:
        return self.__account.get('email_host')

    @property
    def email_port(self) -> int:
        return int(self.__account.get('email_port'))

    @property
    def bloks_version_id(self) -> str:
        return self.__bloks_version_id

    @property
    def claim(self) -> str:
        return self.__auth.get('x-ig-set-www-claim') if self.__auth.get('x-ig-set-www-claim') != '0' else ''

    @property
    def bearer(self) -> str:
        return self.__auth.get('ig-set-authorization', '')

    @property
    def u_rur(self) -> str:
        return self.__auth.get('ig-set-ig-u-rur', '')

    @property
    def mid(self) -> str:
        return self.__auth.get('mid', self.__mid)

    @mid.setter
    def mid(self, value: str):
        self.__mid = value

    @property
    def connection_type_header(self):
        return self.__connection_type_header

    @property
    def user_agent(self):
        return self.__user_agent.format(**self.__device)

    @property
    def capabilities(self):
        return self.__capabilities
