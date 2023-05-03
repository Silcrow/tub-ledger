from tests.test_accounting import TestAccounting, TestDatabase

if __name__ == "__main__":
    # test_accounting = TestAccounting()
    # test_accounting.test_print_balance_sheet()
    test_database = TestDatabase()
    test_database.test_get_category_fields_by_name()

    # TODO provide "disable" bool to both category and account records. Edit all queries or db-read opr accordingly.
    # when a record is disabled, recalculate all category values accordingly.
