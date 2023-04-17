from tests.test_accounting import initialize_SqliteDb

if __name__ == "__main__":
    sqlite_db, assets, liabilities = initialize_SqliteDb()
    print(sqlite_db, assets, liabilities)
    # TODO make print_balance_sheet() work for sql data

    # TODO CLI input form for category, then for account
    # TODO provide "disable" bool to both category and account records. Edit all queries or db-read opr accordingly.
    # when a record is disabled, recalculate all category values accordingly.
