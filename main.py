from tests.test_accounting import test_print_balance_sheet, test_create_ledger
from db_layer.database import SqliteDb

if __name__ == "__main__":
    db = SqliteDb('ledger.db')
    test_create_ledger(db)
    test_print_balance_sheet(db)

    # TODO create delete account in database.py
    # TODO provide "disable" bool to both category and account records. Edit all queries or db-read opr accordingly.

