from enum import Enum

from db_layer.database import SqliteDb


class CategoryEnum(str, Enum):
    """
    Class for prompting the user to select from a list of choices.
    """
    @classmethod
    def from_category_list(cls, list_data):
        enum_values = [(name.upper(), name) for name in list_data]  # enum class attributes
        return cls("CategoryEnum", enum_values)


def load_category_enum():
    """
    Reads the database for list of category names and convert that into a CategoryEnum object.
    :return: CategoryEnum object instance
    """
    db = SqliteDb('ledger.db')
    category_names = db.get_category_names()
    db.close()
    if not category_names:
        result = CategoryEnum.from_category_list(['Assets', 'Liabilities'])
    else:
        result = CategoryEnum.from_category_list(category_names)
    return result


CategoryChoice = load_category_enum()

