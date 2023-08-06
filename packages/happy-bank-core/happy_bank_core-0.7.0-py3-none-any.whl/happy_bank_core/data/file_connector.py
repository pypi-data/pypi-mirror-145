"""Python module that contains FileConnector class"""
import os
import json
import logging

from happy_bank_core.data.connector import Connector
from happy_bank_core.logic.account import Account

logger = logging.getLogger(__name__)


class FileConnector(Connector):
    """FileConnector class that inherits from parent Connector class"""

    def __init__(self):
        self.abs_path = os.path.abspath("data/customers.json")

    def read(self, account_id: str) -> Account:
        """Returns account with specified account id"""
        try:
            with open(self.abs_path, encoding="utf-8") as customers:
                data = json.load(customers)
                logger.debug(
                    f"Read with id parameter: {account_id} returns: {data[account_id]}",
                )
                return Account(
                    data[account_id]["id"],
                    data[account_id]["name"],
                    data[account_id]["deposit"],
                )
        except FileNotFoundError as err:
            logger.info(f"File: {self.abs_path} not found. Creating it...")
            try:
                with open(self.abs_path, "w", encoding="utf-8") as customers:
                    json.dump({}, customers)
                raise KeyError(f"Account with id: {account_id} not found.") from err
            except PermissionError as err:
                logger.error(err)
                raise err
        except KeyError as err:
            logger.error(f"Account with id: {account_id} not found.")
            raise err
        except PermissionError as err:
            logger.error(err)
            raise err

    def update(self, account: Account):
        """Updates a given account"""
        try:
            with open(self.abs_path, "r+", encoding="utf-8") as customers:
                data = json.load(customers)
                logger.debug(f"File: {self.abs_path} before update contains: {data}")
                data[account.id] = account.__dict__
                logger.debug(f"File: {self.abs_path} after update contains: {data}")
            with open(self.abs_path, "w", encoding="utf-8") as customers:
                json.dump(data, customers, indent=2)
        except FileNotFoundError:
            logger.info(f"File: {self.abs_path} not found. Creating it...")
            try:
                with open(self.abs_path, "w", encoding="utf-8") as customers:
                    json.dump({account.id: account.__dict__}, customers)
            except PermissionError as err:
                logger.error(err)
                raise err
        except KeyError as err:
            logger.error(f"Account with id: {account.id} not found.")
            raise err
        except PermissionError as err:
            logger.error(err)
            raise err
