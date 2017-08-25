import sqlalchemy as sa
from sqlalchemy.orm import relationship
from mailmig.models import SqlBase


class Email(SqlBase):
    __tablename__ = 'emails'

    id = sa.Column(sa.types.Integer, primary_key=True)
    imap_account_id = sa.Column(sa.types.Integer, sa.ForeignKey('imap_accounts.id'))
    email = sa.Column(sa.types.PickleType)
    contents = sa.Column(sa.types.TEXT)

    imap_account = relationship('ImapAccount', backref='emails')

    def _key(self):
        if self.email:
            ids = [k for k in self.email.keys() if k.lower() in ['message-id', 'messageid']]

            if not ids:
                return self.content

            return self.email[ids[0]]
        return self.content

    def __eq__(x, y):
        return (x._key() == y._key())

    def __hash__(self):
        return hash(self._key())


__all__ = ['Email']
