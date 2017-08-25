'''MailMig related errors

All mailmig Exceptions are defined in this file

'''

from beautifultable import BeautifulTable


class MailMigError(Exception):
    '''Extends the basic :obj:`Exception` object to include more information
    about the error.

    This class is a base Exception class which is inherited by all other mailmig
    related errors.

    Attribues:
        message (str): Human-friendly error message.
        base_ex (Exception or None): Base Exception associated with this error (if any)
        dump_objs (dict or None): A dictionary of dumpable objects. Can be viewed nicely
        with the `print_dump_objs` function.

    '''

    _values = {}

    def __init__(self, message, base_ex, dump_objs=None):
        super(MailMigError, self).__init__(message)
        self._values = {'message': message, 'base_ex': base_ex, 'dump_objs': dump_objs}

    message = property(fget=lambda self: self._values['message'], doc='Human-friendly message')
    base_ex = property(fget=lambda self: self._values['base_ex'], doc='Base Exception')
    dump_objs = property(fget=lambda self: self._values['dump_objs'], doc='Dumpable objects')

    def print_dump_objs(self, show_headers=True):
        '''Print a human-friendly table of the dumpable objects

        Args:
            show_headers (bool, optional): Determines if the table
            will have headers (defaults to True)

        Returns:
            The generated :obj:`beautifultable.BeautifulTable` object.
        '''

        if not self.dump_objs:
            return None

        tbl = BeautifulTable()

        if show_headers:
            tbl.column_headers = ['Name', 'Values']

        for name, obj in self.dump_objs.items():
            tbl.append_row([name, obj])

        print tbl

    def __str__(self):
        res = self.message

        if self.base_ex:
            res = '%s [Base Error: %s]' % (res, str(self.base_ex))

        return res

    def __repr__(self):
        res = '<MailMigError(message="%s"' % self.message

        if self.base_ex:
            res = '%s, base_ex="%s"' % (res, str(self.base_ex))

        if self.dump_objs:
            res = '%s, dump_objs="%s"' % (res, '", "'.join(self.dump_objs.keys()))

        return res


class CLIError(MailMigError):
    '''An exception that occured as part of the CLI
    portion of this application

    '''

    pass


__all__ = ['MailMigError', 'CLIError']
