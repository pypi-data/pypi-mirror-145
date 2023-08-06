"""Python module that contains Registration class"""
import random
import logging

from happy_bank_core.logic.account import Account

logger = logging.getLogger(__name__)


class Registration:
    """Registration class that contains register method"""

    @staticmethod
    def register(data: dict) -> Account:
        """register method that gets dict and returns Account obj"""
        try:
            if not data["fullname"] or not isinstance(data["fullname"], str):
                logger.error("Received empty string or incorrect data type instead of fullname")
                raise ValueError
            account_id = random.randint(100, 1000)
            return Account(str(account_id), data["fullname"], 0)
        except KeyError as err:
            logger.error("Fullname key not found")
            raise err
