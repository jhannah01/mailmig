from beautifultable import BeautifulTable


class MailMigError(Exception):
    _values = {}
    def __init__(self, message, base_ex, dump_objs=None):
        super(MailMigError, self).__init__(message)
        self._values = {'message': message, 'base_ex': base_ex, 'dump_objs': dump_objs}

    message = property(fget=lambda self: self._values['message'], doc='Human-friendly message')
    base_ex = property(fget=lambda self: self._values['base_ex'], doc='Base Exception (if any)')
    dump_objs = property(fget=lambda self: self._values['dump_objs'], doc='Dumpable objects (if any)')

    def print_dump_objs(self, show_headers=True):
        if not self.dump_objs:
            return None

        tbl = BeautifulTable()

        if show_headers:
            tbl.column_headers = ['Name', 'Values']

        for name, obj in self.dump_objs.items():
            tbl.append_row(name, obj)

        print table

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


__all__ = ['MailMigError']
