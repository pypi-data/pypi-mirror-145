import uuid
import hashlib


class Generations:

    def __init__(self, logger, salt: str):
        self.__log = logger
        self.__log.debug('Start Generator')
        self.__salt = salt

    def phone_id(self, username: str):
        return self.__generator('{}-{}-phone'.format(self.__salt, username))

    def uuid(self, username: str):
        return self.__generator('{}-{}-uuid'.format(self.__salt, username))

    def client_session_id(self, username: str):
        return self.__generator('{}-{}-session'.format(self.__salt, username))

    def pigeon_session_id(self, username: str):
        return self.__generator('{}-{}-pigeon'.format(self.__salt, username))

    def family_guid_id(self, username: str):
        return self.__generator('{}-{}-family'.format(self.__salt, username))

    def guid_id(self, username: str):
        return self.__generator('{}-{}-device'.format(self.__salt, username))

    def android_id(self, username: str):
        m = hashlib.md5()
        m.update(username.encode('utf-8') + self.__salt.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    def advertising_id(self, username):
        return self.__generator('{}-{}-advertising'.format(self.__salt, username))

    @staticmethod
    def __generator(append: str, has_hyphen=True):
        generated_uuid = str(uuid.uuid3(uuid.NAMESPACE_URL, append)) if append else str(uuid.uuid4())
        return generated_uuid if has_hyphen else generated_uuid.replace('-', '')
