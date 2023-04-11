import csv
import os

from financial.accounting import Account, Category


class CsvDb:
    """
    Handles reading and writing to a CSV file.
    """
    def __init__(self, filename, directory='flat_database'):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)
        self.filename = os.path.join(self.directory, filename)
        with open(self.filename, 'a', newline='') as file:
            pass  # create file if it doesn't exist

    def write_csv(self, obj):
        """
        :param obj: Account or Category object
        :return: updated csv
        """
        if isinstance(obj, Account):
            filename = os.path.join(self.directory, 'accounts.csv')
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(obj.to_csv_row())
        elif isinstance(obj, Category):
            filename = os.path.join(self.directory, 'categories.csv')
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(obj.to_csv_row())
        else:
            raise ValueError("Unsupported object type")

        # TODO it writes, but if you run code twice, it'll write scb_bank twice. Redo so that, if an account exists,
        # then update instead of create. Make write_csv() into update_csv().
