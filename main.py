from financial.accounting import Category, Account, print_balance_sheet, print_composite
from models import SqliteDb

if __name__ == "__main__":
    sqlite_db = SqliteDb('ledger.db')  # initialize SqliteDb
    category_dict = sqlite_db.read_categories(name='Assets')
    # category_dict = sqlite_db.read_categories(name='Liabilities')
    print(category_dict)
    print_composite(category_dict)

    # TODO each time an account is upserted, recalculate all category values and upsert that in db
    # each time a category is upserted, recalculate all category values and upsert that in db
    # each time read_categories is done, recalculate all category values before creating the dict

    # TODO CLI input form for category, then for account
    # TODO provide "disable" bool to both category and account records. Edit all queries or db-read opr accordingly.
    # when a record is disabled, recalculate all category values accordingly.
