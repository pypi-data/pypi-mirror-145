from .lib.entity import Credential


class CredentialCustom(Credential):
    USER_AGENT = 'Instagram {app_version} Android ({android_version}/{android_release}; {dpi}; {resolution}; {manufacturer}; {device}; {model}; {cpu}; en_US; {version_code})'
    BLOKS = 'c76e70c382311c68b2201f168f946d800bbfcb7b6d9e43edbd9342d9a2048377'
    CAPABILITIES = '3brTvx8='

    def __init__(self, a, b, c):
        self.__log.debug('CredentialCustom')
        Credential.__init__(self, self.USER_AGENT, self.BLOKS, self.CAPABILITIES)

    @property
    def cookies(self):
        self.__log.debug(self.abstract_auth)
        return self.abstract_auth.get('cookie', {}) if self.abstract_auth else {}

    @property
    def user_id(self):
        return self.cookies.get('ds_user_id', 0)