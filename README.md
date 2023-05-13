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

## Run CLI
```bash
python cli_layer.py save_account
```

## To Self
- make sure to add Assets and Liabilities category at any initial run, so that adding an account and not finding categories is impossible.
- creating Enum class or declaring sqlite db in cli.py, then importing it to test files will cause a glitch where it produces
such files in the test dir.
## Features Skipped
- `save_account` takes choice via typed input, but I want arrow keys and enter like click.
Consider displaying the hierarchy of the categories to the user when they are selecting a category.