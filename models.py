import os
import sqlite3


class SqliteDb:
    """
    Handles reading and writing to a SQLite database file.
    """

    def __init__(self, filename, directory='database'):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)
        self.filename = os.path.join(self.directory, filename)
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()

        # create categories table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                value REAL NOT NULL,
                parent_id INTEGER DEFAULT NULL,
                description TEXT,
                FOREIGN KEY(parent_id) REFERENCES categories(id)
            )
        """)

        # create accounts table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                value REAL NOT NULL,
                category_id INTEGER NOT NULL,
                remarks TEXT,
                FOREIGN KEY(category_id) REFERENCES categories(id)
            )
        """)

        self.connection.commit()

    def upsert_category(self, category):
        """
        Upserts the given Category object to the categories table.
        """
        if category.parent is not None:
            # Check if parent category exists
            parent_query = "SELECT id FROM categories WHERE name = ?"
            self.cursor.execute(parent_query, (category.parent.name,))
            parent_row = self.cursor.fetchone()
            if parent_row:
                parent_id = parent_row[0]
            else:
                raise ValueError("Parent category does not exist in the database")
        else:
            parent_id = None

        # Insert or update category record
        query = """
            INSERT INTO categories (name, value, parent_id, description)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (name) DO UPDATE SET
                value = excluded.value,
                parent_id = excluded.parent_id,
                description = excluded.description
        """
        values = (category.name, category.value, parent_id, category.description)
        self.cursor.execute(query, values)
        self.connection.commit()

    def upsert_account(self, account):
        """
        Upserts the given Account object to the accounts table.
        """
        # Check if category exists
        category_query = "SELECT id FROM categories WHERE name = ?"
        self.cursor.execute(category_query, (account.category.name,))
        category_row = self.cursor.fetchone()
        if category_row:
            category_id = category_row[0]
        else:
            raise ValueError("Category does not exist in the database")

        # Insert or update account record
        query = """
            INSERT INTO accounts (name, value, category_id, remarks)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (name) DO UPDATE SET
                value = excluded.value,
                category_id = excluded.category_id,
                remarks = excluded.remarks
        """
        values = (account.name, account.value, category_id, account.remarks)
        self.cursor.execute(query, values)
        self.connection.commit()

