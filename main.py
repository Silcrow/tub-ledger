from tests.test_accounting import TestAccounting

if __name__ == "__main__":
    test_accounting = TestAccounting()
    test_accounting.test_print_balance_sheet()

    # TODO CLI input form for category, then for account
    # TODO provide "disable" bool to both category and account records. Edit all queries or db-read opr accordingly.
    # when a record is disabled, recalculate all category values accordingly.
