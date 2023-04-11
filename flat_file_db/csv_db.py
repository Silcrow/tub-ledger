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

    def upsert_csv(self, obj):
        """
        :param obj: Account or Category object to upsert
        :return: updated csv
        """
        # maybe prompt the user if row exists: "SCB Bank account exists. Do you want to rewrite this row?"
        if isinstance(obj, Account):
            filename = os.path.join(self.directory, 'accounts.csv')
            with open(filename, 'r', newline='') as file:
                reader = csv.reader(file)
                rows = [row for row in reader]
            for i, row in enumerate(rows):
                if row[0] == obj.name:
                    rows[i] = obj.to_csv_row()
                    break
            else:
                rows.append(obj.to_csv_row())
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
        elif isinstance(obj, Category):
            filename = os.path.join(self.directory, 'categories.csv')
            with open(filename, 'r', newline='') as file:
                reader = csv.reader(file)
                rows = [row for row in reader]
            for i, row in enumerate(rows):
                if row[0] == obj.name:
                    rows[i] = obj.to_csv_row()
                    break
            else:
                rows.append(obj.to_csv_row())
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
        else:
            raise ValueError("Unsupported object type")
