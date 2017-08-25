import sqlalchemy as sa
from mailmig.models import SqlBase
from sqlalchemy.orm import relationship


class MailMigration(SqlBase):
    __tablename__ = 'migrations'

    id = sa.Column(sa.types.Integer, primary_key=True)
    status = sa.Column(sa.types.String(20), default='Pending', nullable=False)
    source_id = sa.Column(sa.types.Integer, sa.ForeignKey('imap_accounts.id'))
    destination_id = sa.Column(sa.types.Integer, sa.ForeignKey('imap_accounts.id'))
    last_time = sa.Column(sa.types.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.current_timestamp())

    source = relationship('ImapAccount', foreign_keys=[source_id])
    destination = relationship('ImapAccount', foreign_keys=[destination_id])


__all__ = ['MailMigration']
