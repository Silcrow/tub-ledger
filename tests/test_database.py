import pytest
import random
from db_layer.database import SqliteDb
from models.accounting import Account, Category


@pytest.fixture(scope="module")
def db():
    db = SqliteDb('ledger.db', test=True)
    return db
    db.close()


@pytest.mark.depends(on=['test_create_ledger'])
def test_get_category_names(db):
    category_names = db.get_category_names()
    print('\n', category_names, '\nfrom db:', db.filename)
    assert isinstance(category_names, list)
    assert all(isinstance(name, str) for name in category_names)


@pytest.mark.depends(on=['test_create_ledger', 'test_get_category_names'])
def test_upsert_account(db):
    test_account = Account(name='Test Account', value=100.0, category=Category(name='Assets'), remarks='Test Remarks')
    category_names = db.get_category_names()
    print('\n')
    for category_name in category_names:
        print(f"Testing {category_name}")
        test_account.category = Category(name=category_name)
        db.upsert_account(test_account)

        # Retrieve the account from the database to check if it was inserted correctly
        query = "SELECT * FROM accounts WHERE name = ?"
        db.cursor.execute(query, (test_account.name,))
        account_row = db.cursor.fetchone()

        # Validate data type and correct values
        assert account_row is not None
        assert isinstance(account_row[0], int)
        assert isinstance(account_row[1], str)
        assert isinstance(account_row[2], float)
        assert isinstance(account_row[3], int)
        assert isinstance(account_row[4], str)
        assert account_row[1] == test_account.name
        assert account_row[2] == test_account.value
        assert account_row[4] == test_account.remarks
        # Check that the category_id in the account row matches the id of the 'Assets' category
        category_query = "SELECT id FROM categories WHERE name = ?"
        db.cursor.execute(category_query, (category_name,))
        category_id = db.cursor.fetchone()[0]
        assert account_row[3] == category_id

        # Delete the test account
        db.cursor.execute("DELETE FROM accounts WHERE name = ?", (test_account.name,))
        db.connection.commit()


@pytest.mark.depends(on=['test_create_ledger'])
def test_enabled_accounts_view(db):
    test_account = Account(name='Test Account', value=0, category=Category(name='Assets'), is_disabled=1)
    db.upsert_account(test_account)
    account_row = db.get_account_by_name('Test Account')
    assert account_row['is_disabled'] == 1
    # Delete the test account
    db.cursor.execute("DELETE FROM accounts WHERE name = ?", (test_account.name,))
    db.connection.commit()


def test_get_enabled_accounts(db):
    enabled_accounts = db.get_accounts(enabled=True)
    assert enabled_accounts is not None
    assert isinstance(enabled_accounts, list)
    assert all(isinstance(account, tuple) for account in enabled_accounts)


def test_get_disabled_accounts(db):
    disabled_accounts = db.get_accounts(enabled=False)
    assert disabled_accounts is not None
    assert isinstance(disabled_accounts, list)
    assert all(isinstance(account, tuple) for account in disabled_accounts)


def test_disable_and_enable_account(db):
    # Retrieve a random account name from the database
    db.cursor.execute("SELECT name FROM accounts")
    account_names = [row[0] for row in db.cursor.fetchall()]
    account_name = random.choice(account_names)
    # test disable_account
    disabled_account = db.disable_account(account_name)
    assert disabled_account is not None
    assert disabled_account[5] == 1
    # test enable_account
    enabled_account = db.enable_account(account_name)
    assert enabled_account is not None
    assert enabled_account[5] == 0


# def test_get_category_fields_by_name(db):
#     category_names = db.get_category_names()
#     for category_name in category_names:
#         category_fields = db.get_category_fields_by_name(category_name)
#         assert isinstance(category_fields, dict)
#         assert isinstance(category_fields.get('name'), str) \
#                and category_fields.get('name') is not None
#         assert isinstance(category_fields.get('value'), float)
#         assert category_fields.get('parent_id') is None or isinstance(category_fields.get('parent_id'), int)
#         assert isinstance(category_fields.get('description'), str)
#         print(f"{category_name} passed")
