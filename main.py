from financial.accounting import Category, Account, print_balance_sheet
from models import SqliteDb

if __name__ == "__main__":
    sqlite_db = SqliteDb('ledger.db')  # initialize SqliteDb
    assets = Category('Assets')
    sqlite_db.upsert_category(assets)
    liabilities = Category('Liabilities')
    sqlite_db.upsert_category(liabilities)

    current_assets = Category('Current Assets', parent=assets)
    sqlite_db.upsert_category(current_assets)
    traditional_savings = Category('Traditional Savings', parent=current_assets, description='1M insured')
    sqlite_db.upsert_category(traditional_savings)

    # scb_bank = Account('SCB Bank', 503.97, category=traditional_savings, remarks='has SCB Easy online access')
    # sqlite_db.upsert_account(scb_bank)
    # k_bank = Account('K Bank', 145253, category=traditional_savings)
    # sqlite_db.upsert_account(k_bank)

    # TODO change csv to sql, then create a function to read both csv and arrange a balance sheet as dict.
    # TODO CLI input form for category, then for account
    # TODO make sure to add Assets and Liabilities category at any initial run, so that adding an account and not
    #  finding categories is impossible.
