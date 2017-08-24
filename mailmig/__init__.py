'''mailmig - A Python mail migration and syncing solution

See more about this project on the GitHub page at
https://github.com/jhannah01/mailmig

Author: Jon Hannah <jon@commtest99.org>

'''


__version__ = '1.0.0'

from mailmig.errors import MailMigError
from mailmig.providers import ImapProvider
from mailmig.logger import get_logger
from mailmig.models import ImapAccount, MailMigration, Email, setup_sa
