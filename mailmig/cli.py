#!/usr/bin/env python2.7

import argparse
import sys
import os
import getpass

from mailmig.errors import CliError


class CLITool(object):
    _migration = None
    _is_verbose = False
    _values = {'source_hostname': None, 'destination_hostname': None,
               'source_login': None, 'destination_login': None, 'use_ssl': True,
               'is_verbose': True}

    def __init__(self, args=None, run_app=False):
        if not args:
            args = self._parse_arguments()

        if isinstance(args, argparse.Namespace):
            self._values = {'source_hostname': args.source_hostname,
                            'destination_hostname': args.destination_hostname,
                            'source_login': args.source_login}
                            'destination_login': args.destination_login,
                            'use_ssl': args.use_ssl,e
                            'is_verbose': args.is_verbose}
        elif isinstance(args, dict):
            self._values.update(dict([(k,v) from k, v in args.items() if k in self._values]))
        else:
            raise CLIError('Unknown arguments object provided: "%r"' % args)

        # TODO: Replace this
        '''
        opts = {}

        server = options.get('server', os.environ.get('SMAPI_HOST', None))
        username = options.get('username', os.environ.get('SMAPI_USER', None))
        password = options.get('password', os.environ.get('SMAPI_PASSWD', None))

        opts['source_hostname'] = self._get_setting(self._values['source_hostname'],
                                           prompt='Source Server Hostname: ',
                                           error_message='Missing server hostname')
        opts['username'] = self._get_setting(username, prompt='Admin Username: ',
                                            error_message='Missing admin username')
        opts['password'] = self._get_setting(password, prompt='Admin Password: ',
                                            error_message='Missing admin password',
                                            is_password=True)
        opts['port'] = options.get('port', None)
        opts['use_ssl'] = options.get('use_ssl', False)

        self._options = opts
        self._is_verbose = options.get('is_verbose', False)
        self._smapi = SMAPI(**opts)
        '''

        self._migration = None

    def _parse_arguments(self):
        parser = argparse.ArgumentParser(description='Simple CLI tool for working with SmarterMail')
        # TODO: Update all of this
        '''
        parser.add_argument('-s', '--server', dest='server',
                            help='Server Hostname (otherwise use SMAPI_HOST or prompt')
        parser.add_argument('-u', '--user', dest='username',
                            help='Admin Username (otherwise use SMAPI_USER or prompt')
        parser.add_argument('-x', '--password', dest='password',
                            help='Admin Password (otherwise use SMAPI_PASSWD or prompt')
        parser.add_argument('-v', '--verbose', dest='is_verbose', action='store_true',
                            help='Be more verbose')
        parser.add_argument('-e', '--ssl', dest='use_ssl', action='store_true',
                            help='Force using HTTPS to connect')
        parser.add_argument('-p', '--port', dest='port', type=int, default=None)
        '''
        return parser.parse_args()

    def _get_setting(self, value, prompt=None, error_message=None, is_password=False):
        # TODO: Rework this redundant logic
        if value:
            return value

        if prompt:
            prompt = prompt.rstrip(' ') + ' '

            try:
                value = getpass.getpass(prompt) if is_password else raw_input(prompt)
            except EOFError,ex:
                if error_message is not None:
                    raise CLIError('Unable to read input value: %s' % error_message, ex)
                return None

        if value:
            return value

        if error_message is not None:
            raise CLIError(error_message)

        return None

    def run(self):
        if self._is_verbose:
            print '[--] SMAPI Tool - Using %s (User: %s)' % (self._smapi.server, self._smapi.username)

def run_clitool():
    try:
        cli_app = CLITool()
        exit_code = cli_app.run()
        sys.exit(exit_code)
    except CLIError,ex:
        print >>sys.stderr,str(ex)
        sys.exit(1)

if __name__ == '__main__':
    run_clitool()

__all__ = ['CLITool', 'CLIError', 'run_clitool']
