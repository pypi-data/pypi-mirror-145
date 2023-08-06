"""Python module that contains MemoryConnector class"""
import logging

from happy_bank_core.data.connector import Connector
from happy_bank_core.logic.account import Account

logger = logging.getLogger(__name__)


class MemoryConnector(Connector):
    """MemoryConnector class that inherits from parent Connector class"""

    def __init__(self):
        self.accounts = {
            "id321": Account("id321", "Johan Doe", 1000),
            "id123": Account("id123", "John Doe", 1000),
            "id456": Account("id456", "Johanna Doe", 1000),
        }

    def read(self, account_id: str) -> Account:
        """Returns account with specific account id"""
        try:
            logger.info(self.accounts[account_id])
            return self.accounts[account_id]
        except KeyError as err:
            logger.error(f"Account with id: {account_id} not found.")
            raise err

    def update(self, account: Account):
        """Updates an existing account"""
        try:
            self.accounts[account.id] = account
            logger.info(self.accounts[account.id])
        except KeyError as err:
            logger.error(f"Account with id: {account.id} not found.")
            raise err
