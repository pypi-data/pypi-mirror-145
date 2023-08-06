# Bank Base Parser for Guatemala Banks

Base models and clases to build parsers for Guatemalan Banks.

This library provides only models and base structure to develop further integrations with each individual bank.

## Supported banks

- [Banrural](https://github.com/gt-banks-parser/banrural-scrapper)
- [BAC - WIP](https://github.com/gt-banks-parser/bac-gt-parser)



## How to use it

### Installation

`pip install bank_base_gt`

Example to get movements of all accounts of Banrural bank, you should install first, banrural library

### Example

```python

credentials = UserPasswordBankLogin(username="", password="")


def test():
    with BanruralBank(credentials) as connection: # Login with bank and make sure that we logout after doing all operations
        accounts = connection.fetch_accounts() # Fetch all accounts
        for a in accounts:
            a.fetch_movements(
                datetime.date.today() - datetime.timedelta(days=20),
                datetime.date.today() + datetime.timedelta(days=1),
            )
            # Fetch all movements 


test()
```