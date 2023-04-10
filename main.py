
import json


class Category:
    """
    Represents calculated values in financial statements such as assets, current assets, fixed assets, liabilities, etc.
    as well as any custom subcategories.
    When user creates a category, instantiate an object from this class.
    """
    def __init__(self, name, value=0, parent=None):
        self.name = name
        self.value = value
        self.parent = parent
        self.children = []
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


class Account:
    """
    Represents individual listings in a financial statement, such as cash in a bank or the value of a property.
    """
    def __init__(self, name, value, category, remarks=None):
        self.name = name
        self.value = value
        self.category = category
        self.remarks = remarks
        category.add_child(self)


def print_nested_category(data, indent=0):
    print("  " * indent + data['name'] + ": " + "{:,.2f}".format(data['value']))
    if data.get('children'):
        for child in data['children']:
            print_nested_category(child, indent+1)


def print_balance_sheet():
    print('Balance Sheet (as of March 4,2023)')  # will need to timestamp and save each balance sheet.
    assets_copy = assets.to_dict()
    print_nested_category(assets_copy)
    liabilities_copy = liabilities.to_dict()
    print_nested_category(liabilities_copy)
    net_worth_calc = assets_copy['value'] - liabilities_copy['value']
    print('Net Worth:', "{:,.2f}".format(net_worth_calc))


if __name__ == "__main__":

    '''assume user creates categories'''
    assets = Category('Assets')
    current_assets = Category('Current Assets', parent=assets)
    traditional_savings = Category('Traditional Savings', parent=current_assets)
    e_savings = Category('E-Savings', parent=current_assets)
    fixed_assets = Category('Fixed Assets', parent=assets)
    liabilities = Category('Liabilities')

    '''assume user creates accounts'''
    # Traditional Savings accounts
    scb_bank = Account('SCB Bank', 503.97, category=traditional_savings, remarks='has SCB Easy online access')
    k_bank = Account('K Bank', 145253, category=traditional_savings)
    bkk_bank = Account('BKK Bank', 90744, category=traditional_savings)
    kt_bank = Account('KT Bank', 42287, category=traditional_savings)
    gh_bank = Account('GH Bank (partnered savings)', 19377, category=traditional_savings, remarks='50% of 38,754')
    baac_bank = Account('BAAC Bank (partnered savings)', 9915.5, category=traditional_savings, remarks='50% of 23,231')

    # E-Savings accounts
    g_wallet = Account('G-wallet (paotang, krungthai)', 0, category=e_savings)
    kpp_dime = Account('KPP Dime (high-yield)', 30000, category=e_savings)
    lhb_you = Account('LHB You (high-yield)', 10000, category=e_savings)

    # Fixed Assets accounts
    gh_bank_fd = Account('GH Bank 3-year Fixed Deposit (since 23M02)', 300000, category=fixed_assets,
                         remarks='2.25% semiannual')
    real_estate_equity = Account('Real estate partnership equity', 250000, category=fixed_assets,
                                 remarks='50% of the 500,000 down payment of 2.2M Baht house')
    maxvalu_fl3 = Account('MaxValu FL3', 300000, category=fixed_assets)
    midsoi_fl4 = Account('MidSoi FL4 (co-own sis)', 150000, category=fixed_assets, remarks='50% of 300,000')
    midsoi_fl2 = Account('MidSoi FL2 (co-own sis)', 115000, category=fixed_assets, remarks='50% of 230,000')

    # Liabilities accounts
    mortgage = Account('1.7M Mortgage (for the partnership property)', 480465.59, category=liabilities,
                       remarks='50% of 960,931.18')

    '''display each'''
    # print(assets.calculate_value())
    # print(liabilities.calculate_value())

    '''display as json'''
    # assets_dict = assets.to_dict()
    # print(json.dumps(assets_dict, indent=4, sort_keys=False, ensure_ascii=False))

    '''display as balance sheet'''
    print_balance_sheet()

    # TODO each time category or account object is created, save it as record in csv.
    # TODO now create a a function that would read from the csv's and python print a json version of the balance sheet.

