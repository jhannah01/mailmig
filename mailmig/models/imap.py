import sqlalchemy as sa
from mailmig.models import SqlBase
from mailmig.providers import ImapProvider

class ImapAccount(SqlBase):
    __tablename__ = 'imap_accounts'

    _imap_account = None

    id = sa.Column(sa.types.Integer, primary_key=True)
    hostname = sa.Column(sa.types.String(100), nullable=False)
    login = sa.Column(sa.types.String(50), nullable=False)
    password = sa.Column(sa.types.String(50), nullable=False)

    @property
    def imap_account(self):
        if not self._imap_account:
            self._imap_account = ImapProvider(self.hostname, self.login, self.password)

        return self._imap_account

__all__ = ['ImapAccount']
