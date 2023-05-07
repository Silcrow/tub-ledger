
class Category:
    """
    Represents calculated values in models statements such as assets, current assets, fixed assets, liabilities, etc.
    as well as any custom subcategories.
    When user creates a category, instantiate an object from this class.
    """
    def __init__(self, name, value=0, parent=None, description=''):
        self.name = name
        self.value = value
        self.parent = parent
        self.children = []
        self.description = description
        if parent is not None:
            parent.add_child(self)

    def add_child(self, child):
        self.children.append(child)

    def calculate_value(self):
        """
        Recursively calculates the summation of the children's values.
        e.g. traditional_savings.calculate_value() will sum the children accounts once. However,
        current_savings.calculate_value() will notice that traditional_savings is a category, so it'll
        trigger the subcategory's calculate_value() and perform that twice. If you assets.calculate_value(), the
        recursion will perform calculate_value() trice.
        :return: the total summation value of accounts and subcategories of the category.
        :rtype: float
        """
        value = 0
        for child in self.children:
            if isinstance(child, Category):
                value += child.calculate_value()
            else:
                value += child.value
        return value

    def to_dict(self):
        """
        Recursively prints the name and value of each account and subcategory in the category, in a tree-like format.
        For example, if called on the "assets" category, it would print out the names and values of all accounts and
        subcategories contained within, as well as any subcategories contained within those subcategories, and so on.
        """
        result = {'name': self.name, 'value': self.calculate_value(), 'children': []}
        for child in self.children:
            if isinstance(child, Category):
                result['children'].append(child.to_dict())
            else:
                result['children'].append({'name': child.name, 'value': child.value})
        return result

    @classmethod
    def from_enum(cls, category_enum):
        return cls(
            name=category_enum.value,
            value=0,
            parent=None,
            description=''
        )

    # TODO create a method that takes dict and instantiates itself as obj


class Account:
    """
    Represents individual listings in a models statement, such as cash in a bank or the value of a property.
    """
    def __init__(self, name, value, category, remarks=None):
        self.name = name
        self.value = value
        self.category = category
        self.remarks = remarks
        category.add_child(self)

    def to_csv_row(self):
        return [self.name, self.value, self.category.name, self.remarks]

    # TODO create a method that takes dict and instantiates itself as obj from data in db


def print_composite(data, indent=0):
    """
    A composite can be broken down into its individual components, but the individual components cannot exist
    independently of the composite.
    e.g. Assets are composite because they are made up of various individual assets that are added together to form a
    total value.
    :param data: composite in dict format.
    :param indent: how much to indent.
    :return: none.
    """
    print("  " * indent + data['name'] + ": " + "{:,.2f}".format(data['value']))
    if data.get('children'):
        for child in data['children']:
            print_composite(child, indent+1)


def print_balance_sheet(assets=None, liabilities=None, sqlite_db=None):
    if not sqlite_db and (not assets or not liabilities):
        raise ValueError("Either 'sqlite_db' or both 'assets' and 'liabilities' must be provided")

    if sqlite_db:
        assets_dict = sqlite_db.get_category_tree(name='Assets')
        liabilities_dict = sqlite_db.get_category_tree(name='Liabilities')
    else:
        # Use the assets and liabilities objects to create the balance sheet dict
        assets_dict = assets.to_dict()
        liabilities_dict = liabilities.to_dict()

    balance_sheet_dict = {
        'assets': assets_dict,
        'liabilities': liabilities_dict,
        'net_worth': assets_dict['value'] - liabilities_dict['value']
    }

    # Print the balance sheet from the balance_sheet_dict
    print('Balance Sheet (as of March 4, 2023)')  # will need to timestamp and save each balance sheet.
    print_composite(balance_sheet_dict['assets'])
    print_composite(balance_sheet_dict['liabilities'])
    print('Net Worth:', "{:,.2f}".format(balance_sheet_dict['net_worth']))
