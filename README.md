# tub-ledger
A ledger system for myself. Run `main.py` to start.

## To use CSV DB
> Note: This option has been deprecated in favor of SQLite. Only the upsert_csv() method is available for the CSV implementation.

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
- run `test_accounting.py`

## To Self
- make sure to add Assets and Liabilities category at any initial run, so that adding an account and not finding categories is impossible.