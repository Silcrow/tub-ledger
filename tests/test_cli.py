import pytest

from cli import CategoryEnum, save_account
from database import SqliteDb
from models.accounting import Category, Account


@pytest.fixture(scope="module")
def db():
    db = SqliteDb(filename='test_ledger.db')
    yield db


@pytest.fixture(scope="module")
def test_choices(db):
    category_names = db.get_category_names()
    result = CategoryEnum.from_category_list(category_names)
    yield result


def test_save_account(test_choices):
    for category_enum in test_choices:
        print(f"Testing {category_enum.name}")
        test_account = save_account(name='test account', value=100.0, category=test_choices.ASSETS, remarks='test '
                                                                                                            'remarks')
        # Validate data type
        assert isinstance(test_account['name'], str)
        assert isinstance(test_account['value'], float)
        assert isinstance(test_account['category'], Category)
        assert isinstance(test_account['remarks'], str)
