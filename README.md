# tub-ledger
A ledger system for myself. Run `main.py` to start.

## To use SQLite DB
run `test_accounting.py` or
```python
# main.py
from tests.test_accounting import TestAccounting

if __name__ == "__main__":
    test_accounting = TestAccounting()
    test_accounting.test_print_balance_sheet()
```

## To Self
- make sure to add Assets and Liabilities category at any initial run, so that adding an account and not finding categories is impossible.