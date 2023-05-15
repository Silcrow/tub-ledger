# tub-ledger
A ledger system for myself. Run `main.py` to start.

## To populate DB with starter data
run `test_accounting.py` or `main.py`
```python
# main.py
from tests.test_accounting import test_print_balance_sheet, test_create_ledger
from db_layer.database import SqliteDb

if __name__ == "__main__":
    db = SqliteDb('ledger.db')
    test_create_ledger(db)
    test_print_balance_sheet(db)
```

## Run CLI
At root directory:
```bash
python -m cli_layer.cli --help
```

## To Self
- make sure to add Assets and Liabilities category at any initial run, so that adding an account and not finding categories is impossible.
- creating Enum class or declaring sqlite db in cli.py, then importing it to test files will cause a glitch where it produces
such files in the test dir.
## Features Skipped
- `save_account` takes choice via typed input, but I want arrow keys and enter like click.
Consider displaying the hierarchy of the categories to the user when they are selecting a category.