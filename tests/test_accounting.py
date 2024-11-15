import pytest
from models.accounting import Category, Account, print_balance_sheet
from db_layer.database import SqliteDb


def insert_categories(db, assets):
    current_assets = Category('Current Assets', parent=assets)
    db.upsert_category(current_assets)
    traditional_savings = Category('Traditional Savings', parent=current_assets, description='1M insured')
    db.upsert_category(traditional_savings)
    e_savings = Category('E-Savings', parent=current_assets, description='1M insured')
    db.upsert_category(e_savings)
    fixed_assets = Category('Fixed Assets', parent=assets, description='Cannot liquidate in 1y')
    db.upsert_category(fixed_assets)
    return current_assets, traditional_savings, e_savings, fixed_assets


def insert_traditional_savings(db, traditional_savings):
    scb_bank = Account('SCB Bank', 503.97, category=traditional_savings, remarks='has SCB Easy online access')
    db.upsert_account(scb_bank)
    k_bank = Account('K Bank', 145253, category=traditional_savings)
    db.upsert_account(k_bank)
    bkk_bank = Account('BKK Bank', 90744, category=traditional_savings)
    db.upsert_account(bkk_bank)
    kt_bank = Account('KT Bank', 42287, category=traditional_savings)
    db.upsert_account(kt_bank)
    gh_bank = Account('GH Bank (partnered savings)', 19377, category=traditional_savings,
                      remarks='50% of 38,754')
    db.upsert_account(gh_bank)
    baac_bank = Account('BAAC Bank (partnered savings)', 9915.5, category=traditional_savings,
                        remarks='50% of 23,231')
    db.upsert_account(baac_bank)


def insert_e_savings(db, e_savings):
    g_wallet = Account('G-wallet (paotang)', 0, category=e_savings, remarks='KTBank')
    db.upsert_account(g_wallet)
    kpp_dime = Account('KPP Dime (high-yield)', 30000, category=e_savings)
    db.upsert_account(kpp_dime)
    lhb_you = Account('LHB You (high-yield)', 10000, category=e_savings)
    db.upsert_account(lhb_you)


def insert_fixed_assets(db, fixed_assets):
    gh_bank_fd = Account('GH Bank 3-year Fixed Deposit (since 23M02)', 300000, category=fixed_assets,
                         remarks='2.25% semiannual')
    db.upsert_account(gh_bank_fd)
    real_estate_equity = Account('Real estate partnership equity', 250000, category=fixed_assets,
                                 remarks='50% of the 500,000 down payment of 2.2M Baht house')
    db.upsert_account(real_estate_equity)
    maxvalu_fl3 = Account('MaxValu FL3', 300000, category=fixed_assets)
    db.upsert_account(maxvalu_fl3)
    midsoi_fl4 = Account('MidSoi FL4 (co-own sis)', 150000, category=fixed_assets, remarks='50% of 300,000')
    db.upsert_account(midsoi_fl4)
    midsoi_fl2 = Account('MidSoi FL2 (co-own sis)', 115000, category=fixed_assets, remarks='50% of 230,000')
    db.upsert_account(midsoi_fl2)


def insert_liabilities(db, liabilities):
    mortgage = Account('1.7M Mortgage (for the partnership property)', 480465.59, category=liabilities,
                       remarks='50% of 960,931.18')
    db.upsert_account(mortgage)


@pytest.fixture(scope='module')
def db():
    db = SqliteDb('ledger.db', test=True)
    return db
    db.close()


def create_default_categories(db):
    assets = Category('Assets')
    db.upsert_category(assets)
    liabilities = Category('Liabilities')
    db.upsert_category(liabilities)
    return assets, liabilities


@pytest.mark.dependency(name='test_create_ledger')
def test_create_ledger(db):
    """
    Integration test for the accounting system.

    This test ensures that the accounting system functions correctly when all components are integrated together.
    It creates a ledger with various categories and accounts, and then prints the balance sheet using the
    `print_balance_sheet` function.

    Note: This is an integration test and may take longer to run than other tests.
    It requires a valid SqliteDb connection.
    """
    assets, liabilities = create_default_categories(db)
    current_assets, traditional_savings, e_savings, fixed_assets = insert_categories(db, assets)

    # insert cash accounts
    insert_traditional_savings(db, traditional_savings)
    insert_e_savings(db, e_savings)

    insert_fixed_assets(db, fixed_assets)
    insert_liabilities(db, liabilities)
    return db, assets, liabilities


@pytest.mark.depends(on=['test_create_ledger'])
def test_print_balance_sheet(db):
    """
    Test the `print_balance_sheet` function with SQLite DB input.
    Note that since print_balance_sheet uses print_composite internally, if this test passes, it implies
    that print_composite is also working correctly.
    """
    print_balance_sheet(db=db)
    # There are no asserts here. Use visual inspection.
