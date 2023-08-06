from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager, AbstractContextManager
import logging
import requests
import datetime
from money import Money

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
}
logger = logging.getLogger(__name__)


class BaseBank(ABC):
    def __init__(self, login_url, accounts_url, movements_url, logout_url):
        self.login_url = login_url
        self.accounts_url = accounts_url
        self.movements_url = movements_url
        self.logout_url = logout_url


class InvalidCredentialsException(Exception):
    pass


class MovementPageNonAvailable(Exception):
    pass


class ChangePasswordRequired(Exception):
    pass


class BankLogin(ABC):
    pass


class UserPasswordBankLogin(BankLogin):
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Bank(BaseBank):
    def __init__(self, name, baseBank, credentials, session=requests.Session()):

        super().__init__(
            baseBank.login_url,
            baseBank.accounts_url,
            baseBank.movements_url,
            baseBank.logout_url,
        )
        self.name = name
        self.credentials = credentials
        self._session = session
        self.is_logged_in = False

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.logout()

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def fetch_accounts(self):
        pass

    @abstractmethod
    def get_account(self, number):
        pass

    @abstractmethod
    def logout(self):
        pass

    def _fetch(self, url, data=None, headers=None, json=False):
        if headers:
            merged_headers = dict(list(DEFAULT_HEADERS.items()) + list(headers.items()))
        else:
            merged_headers = DEFAULT_HEADERS
        logging.debug("Will make request with this headers: {0}".format(merged_headers))
        if data is None:
            result = self._session.get(url, headers=merged_headers)
            result.raise_for_status()
            if json:
                return result.json()
            return result.content
        else:
            result = self._session.post(url, data=data, headers=merged_headers)
            result.raise_for_status()
            return result.text


class AbstractBankAccount(ABC):
    def __init__(
        self, bank, account_number, alias, type, currency, account_bank_reference=None
    ):
        self.bank = bank
        self.account_number = account_number
        self.alias = alias
        self.type = type
        self.currency = currency
        self.account_bank_reference = account_bank_reference

    def __str__(self):
        return "{0} - {1} - {2} - {3} - {4} - {5}".format(
            self.bank.name,
            self.account_number,
            self.alias,
            self.type,
            self.currency,
            self.account_bank_reference,
        )

    @abstractmethod
    def fetch_movements(self, start_date, end_date):
        pass


class Movement:
    def __init__(
        self,
        account,
        transaction_id,
        date,
        description,
        ammount,
        alternative_transaction_id=None,
    ):
        self.account = account
        self.transaction_id = transaction_id
        self.alternative_transaction_id = alternative_transaction_id
        self.date = date
        self.description = description
        self.ammount = ammount
        self.is_debit = ammount < Money(0, currency="GTQ")
        self.is_credit = ammount > Money(0, currency="GTQ")
        self.is_fund_regulation = ammount == Money(0, currency="GTQ")

    def __str__(self):
        return "{0} - {1} (ID: {5}) - {2} - {3} - {4}".format(
            self.account.account_number,
            self.transaction_id,
            self.date,
            self.description,
            self.ammount,
            self.alternative_transaction_id,
        )
