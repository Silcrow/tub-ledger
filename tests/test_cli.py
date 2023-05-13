import pytest
from cli_layer.cli import save_account
from db_layer.database import SqliteDb
from models.accounting import Category
from cli_layer.enums import CategoryEnum


def delete_account_by_name(db, name: str):
    db.cursor.execute("DELETE FROM accounts WHERE name = ?", (name,))
    db.connection.commit()


@pytest.fixture(scope="module")
def db():
    db = SqliteDb('ledger.db', test=True)
    return db
    db.close()


def get_category_enums(db):
    category_names = db.get_category_names()
    result = CategoryEnum.from_category_list(category_names)
    return result


@pytest.mark.depends(on=['test_choices'])
def test_save_account(db):
    category_enums = get_category_enums(db)
    for category_enum in category_enums:
        print(f"\nTesting {category_enum.name}")
        test_account = save_account(use_test_db=True, name='test account', value=100.0, category=category_enum,
                                    remarks='test')
        # Validate data type
        assert isinstance(test_account['name'], str)
        assert isinstance(test_account['value'], float)
        assert isinstance(test_account['category'], Category)
        assert isinstance(test_account['remarks'], str)
        # Clean up test db
        delete_account_by_name(db, 'test account')