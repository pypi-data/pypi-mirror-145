"""
Runs happy bank core app.

Represents REST Api layer.
"""
import logging
import json
from flask import Flask, request

from happy_bank_core.logic.transaction import Transaction, TransactionException
from happy_bank_core.logic.registration import Registration
from happy_bank_core.data.file_connector import FileConnector
from happy_bank_core.config.log import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

api = Flask(__name__)


def compose_error_message(msg, status_code: int):
    """Composes general error message"""
    return json.dumps({"message": str(msg)}), status_code


@api.errorhandler(404)
def page_not_found(err):
    """Handles 404 NotFound error"""
    logger.error(err)
    return compose_error_message(err, 404)


@api.errorhandler(ValueError)
def value_error(err):
    """Handles ValueError"""
    logger.error(err)
    return compose_error_message(
        "Received empty string or incorrect data type instead of fullname", 400
    )


@api.errorhandler(KeyError)
def key_error(err):
    """Handles KeyError"""
    logger.error(err)
    return compose_error_message("Invalid customer ID", 400)


@api.errorhandler(PermissionError)
def permission_error(err):
    """Handles PermissionError"""
    logger.error(err)
    return compose_error_message("Internal Server Error", 500)


@api.errorhandler(FileNotFoundError)
def file_not_found(err):
    """Handles FileNotFoundError"""
    logger.error(err)
    return compose_error_message(err, 404)


@api.errorhandler(TransactionException)
def handle_exception(err):
    """Handles TransactionException"""
    logger.error(err)
    return compose_error_message(err, 400)


@api.route("/")
def welcome_page():
    """Returns welcome message"""
    return "Welcome to Happy Bank", 200


@api.route("/health")
def health():
    """Returns health status"""
    return "Happy Bank Core app is up and running.", 200


@api.route("/registration", methods=["POST"])
def registration():
    """Creates new account"""
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json_data = request.json
        account = Registration.register(json_data)
        file_connector = FileConnector()
        file_connector.update(account)
        return (
            "You have successfully registered",
            200,
            {"Content-Type": "application/json"},
        )
    return "Content-Type not supported!", 400


@api.route("/transfer/<sender>/<receiver>/<amount>")
def transfer(sender, receiver, amount: float):
    """Ensures transfer between 2 accounts of given money"""
    file_connector = FileConnector()
    updated_sender, updated_receiver = Transaction.transfer(
        file_connector.read(sender),
        file_connector.read(receiver),
        float(amount),
    )
    file_connector.update(updated_sender)
    file_connector.update(updated_receiver)
    return f"{list((updated_sender, updated_receiver))}", 200


def main():
    """Main method to run code as a module"""
    api.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    main()
