import re
import email
import datetime
from imaplib2 import IMAP4, IMAP4_SSL

from mailmig.errors import MailMigError


class ImapProvider(object):
    _values = {}

    def __init__(self, hostname, login, password, use_ssl=True, do_login=True):
        self._values = {'hostname': hostname, 'login': login, 'password': password, 'use_ssl': use_ssl, 'imap': None}
        self._check_connection(do_login)

    def _check_connection(self, do_login=True):
        if not self.imap_client or (self.imap_client.state == 'LOGOUT'):
            if self.use_ssl:
                self._values['imap'] = IMAP4_SSL(self.hostname)
            else:
                self._values['imap'] = IMAP4(self.hostname)

        if do_login:
            if self.imap_client.state == 'NONAUTH':
                (typ, data) = self.imap_client.login(self._values['login'], self._values['password'])
                if typ != 'OK':
                    raise MailMigError('Invalid IMAP response from server "%s" when trying to login: %r' % (self.hostname,
                                                                                                             data),
                                        dump_objs={'imap_data': data})


        return self.imap_client.state

    def list_folders(self, directory=None, pattern=None):
        list_re = r'\((?P<flags>.*?)\) "(?P<sep>.*)" "(?P<name>.*)"'

        self._check_connection()
        (typ, folders) = self.imap_client.list(directory, pattern)
        if (typ != 'OK'):
            raise MailMigError('Unable to list folders: %r' % folders, dump_objs={'imap_folders': folders})

        folders = []

        for fld in folders:
            m = re.match(list_re, fld)
            if not m:
                raise MailMigError('Unable to parse folder: %r' % fld, dump_objs={'imap_folders': folders,
                                                                                   'bad_folder': fld})

            folders.append(m.group('name'))

        return folders

    def get_messages(self, folder, criteria='ALL'):
        self._check_connection()

        (typ, data) = self.imap_client.select(folder)
        if (typ != 'OK'):
            raise MailMigError('Unable to enter folder "%s": %r' % (folder, data), dump_objs={'imap_result': data})

        (typ, messages) = self.imap_client.search(None, criteria)
        if (typ != 'OK'):
            raise MailMigError('Unable to find messages in folder "%s": %r' % (folder, messages),
                                dump_objs={'messages': messages})


        found_messages = {}

        for msg_id in messages[0].split(' '):
            (typ, data) = self.imap_client.fetch(msg_id, '(BODY[HEADER.FIELDS (MESSAGE-ID)] RFC822)')
            if (typ != 'OK'):
                raise MailMigError('Unable to fetch message ID %s: %r' % (msg_id, data),
                                    dump_objs={'msg_id': msg_id, 'imap_data': data})

            (req, message_id) = data[0]
            m = re.match(r'Message-ID: <(?P<message_id>.*)>', message_id, re.IGNORECASE)
            if not m:
                raise MailMigError('Unable to determine message ID for message %s from %s' % (msg_id, message_id),
                                    dump_objs={'msg_id': msg_id, 'message_id': message_id, 'imap_data': data})

            (req, contents) = data[1]
            eml = email.message_from_string(contents)
            found_messages[m.group('message_id')] = {'msg_id': msg_id, 'contents': contents, 'email': eml}

        return found_messages

    hostname = property(fget=lambda self: self._values['hostname'], doc='IMAP Hostname')
    use_ssl = property(fget=lambda self: self._values['use_ssl'], doc='Determines if IMAPS is used')
    imap_client = property(fget=lambda self: self._values['imap'], doc='imaplib2.IMAP4/IMAP4_SSL client')


__all__ = ['ImapProvider']
