import logging
import poplib
import os
import datetime

from datetime import timezone
from email.parser import Parser
from email.utils import parsedate_tz


class Pop:

    def __init__(self, logger: logging, pop3_host, pop3_port, debug=False):
        self.logging = logger
        self.pop3_server_domain = pop3_host
        self.pop3_server_port = pop3_port
        self.pop3_conn = None
        self.debug = debug

    def connect_pop3_server(self, user_email, user_password):

        # if pop3 server connection object is null then create it.
        if (self.pop3_conn is None):
            self.logging.debug('---- start connect_pop3_server ----')
            # create pop3 server connection object.
            self.pop3_conn = poplib.POP3_SSL(self.pop3_server_domain, port=self.pop3_server_port)
            if self.debug: self.pop3_conn.set_debuglevel(1)

            # get pop3 server welcome message and print on console.
            welcome_message = self.pop3_conn.getwelcome()
            self.logging.debug('Below is pop3 server welcome messages : ')
            self.logging.debug(welcome_message)

            # send user email and password to pop3 server.
            self.pop3_conn.user(user_email)
            self.pop3_conn.pass_(user_password)

    '''
    Close the pop3 server connection and release the connection object.
    '''

    def close_pop3_server_connection(self):
        if not self.pop3_conn:
            self.pop3_conn.quit()

    '''
    Get email messages status of the given user.
    '''

    def get_user_email_status(self, user_email, user_password):

        # connect to pop3 server with the user account.
        self.connect_pop3_server(user_email, user_password)
        self.logging.debug('---- start get_user_email_status ----')

        # get user total email message count and email file size.
        (messageCount, totalMessageSize) = self.pop3_conn.stat()
        self.logging.debug('Email message numbers : ' + str(messageCount))
        self.logging.debug('Total message size : ' + str(totalMessageSize) + ' bytes.')

    '''
    Get user email index info
    '''

    def get_user_email_index(self, user_email, user_password):

        result = dict()

        self.connect_pop3_server(user_email, user_password)
        self.logging.debug('---- start get_user_email_index ----')

        # get all user email list info from pop3 server.
        (resp_message, mails_list, octets) = self.pop3_conn.list()
        result['resp'] = resp_message
        result['mails'] = mails_list
        result['octets'] = octets
        # print server response message.
        self.logging.debug('Server response message : ' + str(resp_message))
        # loop in the mail list.
        for mail in mails_list:
            # print each mail object info.
            self.logging.debug('Mail : ' + str(mail))

        self.logging.debug('Octets number : ' + str(octets))
        return result

    '''
    Get user account email by the provided email account and email index number.
    '''

    def get_email_by_index(self, user_email, user_password, email_index):

        self.connect_pop3_server(user_email, user_password)
        self.logging.debug('---- start get_email_by_index ----')
        # retrieve user email by email index.
        (resp_message, lines, octets) = self.pop3_conn.retr(email_index)
        self.logging.debug('Server response message : ' + str(resp_message))
        self.logging.debug('Octets number : ' + str(octets))

        # join each line of email message content to create the email content and decode the data with utf-8 charset encoding.
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        # print out the email content string.
        # self.logging.debug('Mail content : ' + msg_content)

        # parse the email string to a MIMEMessage object.
        msg = Parser().parsestr(msg_content)
        return self.parse_email_msg(msg)

    # Parse email message.
    def parse_email_msg(self, msg):

        self.logging.debug('---- start parse_email_msg ----')

        header = self.parse_email_header(msg)

        body = self.parse_email_body(msg)

        return {'header': header, 'body': body}

        # Delete user email by index.

    def delete_email_from_pop3_server(self, user_email, user_password, email_index):
        self.connect_pop3_server(user_email, user_password)
        self.logging.debug(
            '---- start delete_email_from_pop3_server ----')

        self.pop3_conn.dele(email_index)
        self.logging.debug('Delete email at index : ' + email_index)

    # Parse email header data.
    def parse_email_header(self, msg):
        self.logging.debug('---- start parse_email_header ----')
        # just parse from, to, subject header value.
        header_list = ('From', 'To', 'Subject', 'Date')

        result = []

        # loop in the header list
        for header in header_list:
            # get each header value.
            header_value = msg.get(header, '')
            if header == 'Date':
                header_value = parsedate_tz(header_value)
                tz = datetime.timezone(datetime.timedelta(seconds=header_value[-1]))
                header_value = datetime.datetime(*header_value[0:6], tzinfo=tz).replace(tzinfo=tz).astimezone(
                    tz=timezone.utc)

            result.append({header: header_value})
            self.logging.debug(str(header) + ' : ' + str(header_value))

            # Parse email body data.
        return result

    def parse_email_body(self, msg):
        self.logging.debug('---- start parse_email_body ----')

        result = []

        # if the email contains multiple part.
        if (msg.is_multipart()):
            # get all email message parts.
            parts = msg.get_payload()
            # loop in above parts.
            for n, part in enumerate(parts):
                # get part content type.
                content_type = part.get_content_type()
                self.logging.debug('----Part ' + str(n) + ' content type : ' + content_type + '----------------')
                result.append(self.parse_email_content(msg))
        else:
            result.append(self.parse_email_content(msg))
            # Parse email message part data.
        return result

    def parse_email_content(self, msg):
        # get message content type.
        content_type = msg.get_content_type().lower()

        content = ''
        attach_file_path = ''
        attach_file_name = ''

        self.logging.debug('---------- Content type ' + content_type + '-------------------')
        # if the message part is text part.
        if content_type == 'text/plain' or content_type == 'text/html':
            # get text content.
            content = msg.get_payload(decode=True)
            # get text charset.
            charset = msg.get_charset()
            # if can not get charset.
            if charset is None:
                # get message 'Content-Type' header value.
                content_type = msg.get('Content-Type', '').lower()
                # parse the charset value from 'Content-Type' header value.
                pos = content_type.find('charset=')
                if pos >= 0:
                    charset = content_type[pos + 8:].strip()
                    pos = charset.find(';')
                    if pos >= 0:
                        charset = charset[0:pos]
            else:
                content = content.decode(charset)

            # self.logging.debug(content)
        # if this message part is still multipart such as 'multipart/mixed','multipart/alternative','multipart/related'
        elif content_type.startswith('multipart'):
            # get multiple part list.
            body_msg_list = msg.get_payload()
            # loop in the multiple part list.
            for body_msg in body_msg_list:
                # parse each message part.
                self.parse_email_content(body_msg)
        # if this message part is an attachment part that means it is a attached file.
        elif content_type.startswith('image') or content_type.startswith('application'):
            # get message header 'Content-Disposition''s value and parse out attached file name.
            attach_file_info_string = msg.get('Content-Disposition')
            prefix = 'filename="'
            pos = attach_file_info_string.find(prefix)
            attach_file_name = attach_file_info_string[pos + len(prefix): len(attach_file_info_string) - 1]

            # get attached file content.
            attach_file_data = msg.get_payload(decode=True)
            # get current script execution directory path.
            current_path = os.path.dirname(os.path.abspath(__file__))
            # get the attached file full path.
            attach_file_path = current_path + '/' + attach_file_name
            # write attached file content to the file.
            with open(attach_file_path, 'wb') as f:
                f.write(attach_file_data)

            self.logging.debug('attached file is saved in path ' + attach_file_path)

        else:
            content = msg.as_string()
            self.logging.debug(content)

        return {'content': content, 'attach': {'file_path': attach_file_path, 'file_name': attach_file_name}}
