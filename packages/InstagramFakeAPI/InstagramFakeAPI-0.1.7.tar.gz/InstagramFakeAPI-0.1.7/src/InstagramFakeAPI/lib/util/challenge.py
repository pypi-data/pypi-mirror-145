import re
import logging
from ...lib.email.pop import Pop


class ExtractCode:

    def __init__(self, logger: logging,email: Pop):
        self.__log = logger
        self.__email = email
        pass

    def extract_code(self, email: str, password: str, timestamp: int):
        info = self.__email.get_user_email_index(email, password)

        self.__log.info('Messages in mail = ' + str(len(info['mails'])))

        message = self.__email.get_email_by_index(email, password, len(info['mails']))
        message_timestamp = message['header'][3]['Date']

        self.__log.info('Message time received ' + str(message_timestamp))
        self.__log.info('Start time ' + str(timestamp))

        self.__email.close_pop3_server_connection()
        if message_timestamp > timestamp:
            match = re.search('\d\d\d\d\d\d', str(message['body'][0]['content']))
            if match.group(0):
                return '{:06d}'.format(int(match.group(0)))
            else:
                return 0
        else:
            return 0
