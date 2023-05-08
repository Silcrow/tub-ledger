import pytest
from database import SqliteDb


@pytest.fixture(scope="module")
def db():
    db = SqliteDb('ledger.db')
    yield db


def test_get_category_names(db):
    category_names = db.get_category_names()
    # print('\n', category_names)
    assert isinstance(category_names, list)
    assert all(isinstance(name, str) for name in category_names)

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
