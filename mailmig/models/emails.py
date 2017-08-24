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


__all__ = ['Email']
