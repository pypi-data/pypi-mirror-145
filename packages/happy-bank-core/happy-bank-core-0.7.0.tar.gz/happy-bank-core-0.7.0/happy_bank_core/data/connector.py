"""Python module that contains parent class Connector"""
from abc import ABC, abstractmethod

from happy_bank_core.logic.account import Account


class Connector(ABC):
    """Parent class for data source connectors"""

    @abstractmethod
    def read(self, account_id: str) -> Account:
        """Returns account with specific account id"""

    @abstractmethod
    def update(self, account: Account):
        """Updates a given account"""
