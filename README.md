# tub-ledger
A ledger system for myself. Run `main.py` to start.

## To use CSV DB
> There's only upsert_csv(). I changed my mind to use sqlite not flat file.

```python
# in main.py
if __name__ == "__main__":
    csv_db = CsvDb('accounts.csv', directory='flat_database')  # initialize CsvDb
    csv_db = CsvDb('categories.csv', directory='flat_database')
    
    assets = Category('Assets')
    csv_db.upsert_csv(assets)
    current_assets = Category('Current Assets', parent=assets)
    csv_db.upsert_csv(current_assets)
    traditional_savings = Category('Traditional Savings', parent=current_assets, description='1M insured')
    csv_db.upsert_csv(traditional_savings)
    
    scb_bank = Account('SCB Bank', 503.97, category=traditional_savings, remarks='has SCB Easy online access')
    csv_db.upsert_csv(scb_bank)
    k_bank = Account('K Bank', 145253, category=traditional_savings)
    csv_db.upsert_csv(k_bank)
    # so on...
```

## To use SQLite DB
```python
if __name__ == "__main__":
    sqlite_db = SqliteDb('ledger.db')  # initialize SqliteDb
    assets = Category('Assets')
    sqlite_db.upsert_category(assets)
    liabilities = Category('Liabilities')
    sqlite_db.upsert_category(liabilities)

    # insert categories
    current_assets = Category('Current Assets', parent=assets)
    sqlite_db.upsert_category(current_assets)
    traditional_savings = Category('Traditional Savings', parent=current_assets, description='1M insured')
    sqlite_db.upsert_category(traditional_savings)
    e_savings = Category('E-Savings', parent=current_assets, description='1M insured')
    sqlite_db.upsert_category(e_savings)
    fixed_assets = Category('Fixed Assets', parent=assets, description='Cannot liquidate in 1y')
    sqlite_db.upsert_category(fixed_assets)

    # insert cash accounts
    scb_bank = Account('SCB Bank', 503.97, category=traditional_savings, remarks='has SCB Easy online access')
    sqlite_db.upsert_account(scb_bank)
    k_bank = Account('K Bank', 145253, category=traditional_savings)
    sqlite_db.upsert_account(k_bank)
    bkk_bank = Account('BKK Bank', 90744, category=traditional_savings)
    sqlite_db.upsert_account(bkk_bank)
    kt_bank = Account('KT Bank', 42287, category=traditional_savings)
    sqlite_db.upsert_account(kt_bank)
    gh_bank = Account('GH Bank (partnered savings)', 19377, category=traditional_savings, remarks='50% of 38,754')
    sqlite_db.upsert_account(gh_bank)
    baac_bank = Account('BAAC Bank (partnered savings)', 9915.5, category=traditional_savings, remarks='50% of 23,231')
    sqlite_db.upsert_account(baac_bank)
    # E-Savings accounts
    g_wallet = Account('G-wallet (paotang)', 0, category=e_savings, remarks='KTBank')
    sqlite_db.upsert_account(g_wallet)
    kpp_dime = Account('KPP Dime (high-yield)', 30000, category=e_savings)
    sqlite_db.upsert_account(kpp_dime)
    lhb_you = Account('LHB You (high-yield)', 10000, category=e_savings)
    sqlite_db.upsert_account(lhb_you)

    # Fixed Assets accounts
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

    # Liabilities accounts
    mortgage = Account('1.7M Mortgage (for the partnership property)', 480465.59, category=liabilities,
                       remarks='50% of 960,931.18')
    sqlite_db.upsert_account(mortgage)

    print_balance_sheet(assets, liabilities)  # python print as balance sheet
```

## To Self
- make sure to add Assets and Liabilities category at any initial run, so that adding an account and not finding categories is impossible.