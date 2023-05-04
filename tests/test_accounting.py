import logging
import unittest
from typing import Dict, Type
from models.accounting import Category, Account, print_balance_sheet
from database import SqliteDb


def initialize_SqliteDb():
    sqlite_db = SqliteDb('ledger.db')
    assets = Category('Assets')
    sqlite_db.upsert_category(assets)
    liabilities = Category('Liabilities')
    sqlite_db.upsert_category(liabilities)
    return sqlite_db, assets, liabilities


def insert_categories(sqlite_db, assets):
    current_assets = Category('Current Assets', parent=assets)
    sqlite_db.upsert_category(current_assets)
    traditional_savings = Category('Traditional Savings', parent=current_assets, description='1M insured')
    sqlite_db.upsert_category(traditional_savings)
    e_savings = Category('E-Savings', parent=current_assets, description='1M insured')
    sqlite_db.upsert_category(e_savings)
    fixed_assets = Category('Fixed Assets', parent=assets, description='Cannot liquidate in 1y')
    sqlite_db.upsert_category(fixed_assets)
    return current_assets, traditional_savings, e_savings, fixed_assets


def insert_traditional_savings(sqlite_db, traditional_savings):
    scb_bank = Account('SCB Bank', 503.97, category=traditional_savings, remarks='has SCB Easy online access')
    sqlite_db.upsert_account(scb_bank)
    k_bank = Account('K Bank', 145253, category=traditional_savings)
    sqlite_db.upsert_account(k_bank)
    bkk_bank = Account('BKK Bank', 90744, category=traditional_savings)
    sqlite_db.upsert_account(bkk_bank)
    kt_bank = Account('KT Bank', 42287, category=traditional_savings)
    sqlite_db.upsert_account(kt_bank)
    gh_bank = Account('GH Bank (partnered savings)', 19377, category=traditional_savings,
                      remarks='50% of 38,754')
    sqlite_db.upsert_account(gh_bank)
    baac_bank = Account('BAAC Bank (partnered savings)', 9915.5, category=traditional_savings,
                        remarks='50% of 23,231')
    sqlite_db.upsert_account(baac_bank)


def insert_e_savings(sqlite_db, e_savings):
    g_wallet = Account('G-wallet (paotang)', 0, category=e_savings, remarks='KTBank')
    sqlite_db.upsert_account(g_wallet)
    kpp_dime = Account('KPP Dime (high-yield)', 30000, category=e_savings)
    sqlite_db.upsert_account(kpp_dime)
    lhb_you = Account('LHB You (high-yield)', 10000, category=e_savings)
    sqlite_db.upsert_account(lhb_you)


def insert_fixed_assets(sqlite_db, fixed_assets):
    gh_bank_fd = Account('GH Bank 3-year Fixed Deposit (since 23M02)', 300000, category=fixed_assets,
                         remarks='2.25% semiannual')
    sqlite_db.upsert_account(gh_bank_fd)
    real_estate_equity = Account('Real estate partnership equity', 250000, category=fixed_assets,
                                 remarks='50% of the 500,000 down payment of 2.2M Baht house')
    sqlite_db.upsert_account(real_estate_equity)
    maxvalu_fl3 = Account('MaxValu FL3', 300000, category=fixed_assets)
    sqlite_db.upsert_account(maxvalu_fl3)
    midsoi_fl4 = Account('MidSoi FL4 (co-own sis)', 150000, category=fixed_assets, remarks='50% of 300,000')
    sqlite_db.upsert_account(midsoi_fl4)
    midsoi_fl2 = Account('MidSoi FL2 (co-own sis)', 115000, category=fixed_assets, remarks='50% of 230,000')
    sqlite_db.upsert_account(midsoi_fl2)


def insert_liabilities(sqlite_db, liabilities):
    mortgage = Account('1.7M Mortgage (for the partnership property)', 480465.59, category=liabilities,
                       remarks='50% of 960,931.18')
    sqlite_db.upsert_account(mortgage)


class TestAccounting(unittest.TestCase):

    def setUp(self) -> None:
        print("\033[34mTesting:\033[0m", self._testMethodName)

    def tearDown(self) -> None:
        print(self._testMethodName, "\033[32mPassed.\033[0m")

    def test_create_ledger(self):
        """
        Integration test for the accounting system.

        This test ensures that the accounting system functions correctly when all components are integrated together.
        It creates a ledger with various categories and accounts, and then prints the balance sheet using the
        `print_balance_sheet` function.

        Note: This is an integration test and may take longer to run than other tests.
        It requires a valid SqliteDb connection.
        """
        sqlite_db, assets, liabilities = initialize_SqliteDb()
        current_assets, traditional_savings, e_savings, fixed_assets = insert_categories(sqlite_db, assets)

        # insert cash accounts
        insert_traditional_savings(sqlite_db, traditional_savings)
        insert_e_savings(sqlite_db, e_savings)

        insert_fixed_assets(sqlite_db, fixed_assets)
        insert_liabilities(sqlite_db, liabilities)
        return sqlite_db, assets, liabilities

    def test_print_balance_sheet(self):
        print("\nTest with object input.")
        sqlite_db, assets, liabilities = self.test_create_ledger()
        print_balance_sheet(assets=assets, liabilities=liabilities)
        print("\nTest with SQLite DB input.")
        print_balance_sheet(sqlite_db=sqlite_db)


class TestDatabase(unittest.TestCase):

    def setUp(self) -> None:
        self.db = SqliteDb('ledger.db')
        print("\033[34mTesting:\033[0m", self._testMethodName)

    def tearDown(self) -> None:
        print(self._testMethodName, "\033[32mPassed.\033[0m")

    def test_get_category_names(self):
        category_names = self.db.get_category_names()
        # print(category_names)
        assert isinstance(category_names, list)
        assert all(isinstance(name, str) for name in category_names)

    def test_get_category_fields_by_name(self):
        category_names = self.db.get_category_names()
        for category_name in category_names:
            category_fields = self.db.get_category_fields_by_name(category_name)
            # print(category_fields)
            assert isinstance(category_fields, dict)
            assert isinstance(category_fields.get('name'), str)\
                   and category_fields.get('name') is not None
            assert isinstance(category_fields.get('value'), float)
            assert category_fields.get('parent_id') is None or isinstance(category_fields.get('parent_id'), int)
            assert isinstance(category_fields.get('description'), str)
            print(f"{category_name} passed")


if __name__ == '__main__':
    unittest.main()
