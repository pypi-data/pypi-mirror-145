# log.py

import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class CfEmailLog:
    def __init__(self):
        """Log structure"""
        self.connection_ok: Optional[bool] = None
        self.host: Optional[str] = None
        self.port: Optional[int] = None
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.use_tls: Optional[bool] = None
        self.header_tags: Optional[dict] = None
        self.local_hostname: Optional[str] = None
        self.debug: Optional[bool] = None
        self.transfers: List[CfEmailLogTransfer] = []

    @property
    def recipients_list(self) -> List[str]:
        """Return a list of all TO and CC recipients for all transfers.

        Returns:
            List of recipients.
        """
        # Todo: Write test
        recipients = []
        for transfer in self.transfers:
            if isinstance(transfer.recipients, str):
                if transfer.recipients not in recipients:
                    recipients.append(transfer.recipients)
            elif isinstance(transfer.recipients, list):
                for recipient in transfer.recipients:
                    if recipient not in recipients:
                        recipients.append(recipient)

            if isinstance(transfer.cc_recipients, str):
                if transfer.cc_recipients not in recipients:
                    recipients.append(transfer.cc_recipients)
            elif isinstance(transfer.cc_recipients, list):
                for recipient in transfer.cc_recipients:
                    if recipient not in recipients:
                        recipients.append(recipient)

        return recipients

    def as_dict(self) -> dict:
        """Get log contents.

        Returns:
             Log contents.
        """
        return {
            'connection_ok': self.connection_ok,
            'host': self.host,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'use_tls': self.use_tls,
            'header_tags': self.header_tags,
            'local_hostname': self.local_hostname,
            'debug': self.debug,
            'transfers': [transfer.as_dict() for transfer in self.transfers],
        }

    def as_string(self) -> str:
        return str(self.as_dict())

    def __repr__(self):
        return self.as_string()


class CfEmailLogTransfer:
    def __init__(self):
        """Transfer log structure"""

        self.transfer_ok: Optional[bool] = None
        self.sender: Optional[str] = None
        self.recipients: Optional[list, str] = None
        self.cc_recipients: Optional[list, str] = None
        self.subject: Optional[str] = None
        self.body: Optional[str] = None
        self.attachments: Optional[list] = None
        
    def as_dict(self):
        """Get log contents.
        
        Returns:
             Log contents.
        """
        return {
            'transfer_ok': self.transfer_ok,
            'sender': self.sender,
            'recipients': self.recipients,
            'cc_recipients': self.cc_recipients,
            'subject': self.subject,
            'body': self.body,
            'attachments': self.attachments
        }

    def as_string(self) -> str:
        return str(self.as_dict())

    def __repr__(self):
        return self.as_string()
        