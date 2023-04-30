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

    def calculate_category_value(self, category_id):
        """
        Calculate category value based on values of all its child categories and accounts.
        :param category_id: id of category
        :return: updated database
        """
        # fetch current value
        cursor = self.connection.cursor()
        cursor.execute("SELECT value FROM categories WHERE id=?", (category_id,))
        category_value = cursor.fetchone()[0]

        # sum values from all child accounts and categories
        cursor.execute("SELECT value FROM accounts WHERE category_id=?", (category_id,))
        child_account_values = [row[0] for row in cursor.fetchall()]
        total_value = category_value + sum(child_account_values)
        cursor.execute("SELECT value FROM categories WHERE parent_id=? AND parent_id IS NOT NULL", (category_id,))
        child_category_values = [row[0] for row in cursor.fetchall()]
        total_value += sum(child_category_values)

        cursor.execute("UPDATE categories SET value=? WHERE id=?", (total_value, category_id))
        self.connection.commit()

    def calculate_every_category(self):
        """
        Get all category IDs, ordered by hierarchy depth, then calculate_category_value() to each.
        """
        # Reset all category values to 0 before calculating
        self.cursor.execute("UPDATE categories SET value = 0")
        self.connection.commit()

        # Calculate category values in order of depth in the hierarchy tree
        query = """
            WITH RECURSIVE category_tree(id, name, value, parent_id, depth) AS (
                SELECT id, name, value, parent_id, 0
                FROM categories
                WHERE parent_id IS NULL
                UNION ALL
                SELECT c.id, c.name, c.value, c.parent_id, ct.depth + 1
                FROM categories c
                JOIN category_tree ct ON c.parent_id = ct.id
            )
            SELECT id FROM category_tree ORDER BY depth DESC;
        """
        category_ids = [row[0] for row in self.cursor.execute(query)]
        for category_id in category_ids:
            self.calculate_category_value(category_id)

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
        self.calculate_every_category()

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
        self.calculate_every_category()

    # did not grok
    def read_categories(self, name=None):
        """
        Returns a nested dict from categories and accounts databases.
        :param name: name of category i.e. Assets, Liabilities, etc.
        :return: nested dict
        """
        self.calculate_every_category()
        categories_query = "SELECT id, name, value FROM categories WHERE name=?"
        accounts_query = "SELECT id, name, value, remarks FROM accounts WHERE category_id=?"
        cursor = self.connection.cursor()

        result = {'name': None, 'value': 0.0, 'children': []}

        # Select the category with the given name
        cursor.execute(categories_query, (name,))
        category = cursor.fetchone()
        if category is None:
            raise ValueError("No category found with name {}".format(name))
        result['name'] = category[1]
        result['value'] = category[2]

        # Select child categories
        cursor.execute("SELECT id, name, value FROM categories WHERE parent_id=?", (category[0],))
        child_categories = cursor.fetchall()

        # Recursively call read_categories for each child category and add resulting nested dict to children array
        for child_category in child_categories:
            result['children'].append(self.read_categories(name=child_category[1]))

        # Select child accounts
        cursor.execute(accounts_query, (category[0],))
        child_accounts = cursor.fetchall()

        # Add a nested dict to children array for each child account
        for child_account in child_accounts:
            result['children'].append({
                'name': child_account[1],
                'value': child_account[2],
                'remarks': child_account[3]
            })

        return result
