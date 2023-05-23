import os
import sqlite3
from rich import print


class SqliteDb:
    """
    Handles reading and writing to a SQLite database file.
    """

    def __init__(self, filename=None, test=False):
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
        self.filename = filename
        if test:
            directory = 'database'
            self.filename = f"test_{filename}"
        os.makedirs(directory, exist_ok=True)
        db_path = os.path.join(directory, self.filename)
        self.connection = sqlite3.connect(db_path)
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
                is_disabled INTEGER DEFAULT 0,
                FOREIGN KEY(category_id) REFERENCES categories(id)
            )
        """)

        # create enabled_accounts view if it doesn't exist
        self.cursor.execute("""
            CREATE VIEW IF NOT EXISTS enabled_accounts AS
            SELECT * FROM accounts WHERE is_disabled = 0
        """)

        self.connection.commit()

    # did not grok
    def close(self):
        self.cursor.close()
        self.connection.close()

    def calculate_category_value(self, category_id):
        """
        Calculate category value based on values of all its child categories and enabled accounts.
        NOTE: This was created so to create calculate_every_category().
        :param category_id: id of category
        :return: updated database
        """
        # fetch current value
        self.cursor.execute("SELECT value FROM categories WHERE id=?", (category_id,))
        category_value = self.cursor.fetchone()[0]

        # sum values from all child accounts and categories
        self.cursor.execute("SELECT value FROM enabled_accounts WHERE category_id=?", (category_id,))
        child_account_values = [row[0] for row in self.cursor.fetchall()]
        total_value = category_value + sum(child_account_values)
        self.cursor.execute("SELECT value FROM categories WHERE parent_id=? AND parent_id IS NOT NULL", (category_id,))
        child_category_values = [row[0] for row in self.cursor.fetchall()]
        total_value += sum(child_category_values)

        self.cursor.execute("UPDATE categories SET value=? WHERE id=?", (total_value, category_id))
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
        self.connection.commit()
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
            INSERT INTO accounts (name, value, category_id, remarks, is_disabled)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT (name) DO UPDATE SET
                value = excluded.value,
                category_id = excluded.category_id,
                remarks = excluded.remarks
        """
        values = (account.name, account.value, category_id, account.remarks, account.is_disabled)
        self.cursor.execute(query, values)
        self.connection.commit()
        self.calculate_every_category()

    def disable_account(self, name):
        query = "UPDATE accounts SET is_disabled = 1 WHERE name = ?"
        self.cursor.execute(query, (name,))
        self.cursor.execute("SELECT * FROM accounts WHERE name = ?", (name,))
        disabled_account = self.cursor.fetchone()
        self.connection.commit()
        print(f'\nDisabled account: {disabled_account}')
        return disabled_account

    def disable_many_accounts(self, list_account_names):
        for account in list_account_names:
            self.disable_account(account)

    def enable_account(self, name):
        query = "UPDATE accounts SET is_disabled = 0 WHERE name = ?"
        self.cursor.execute(query, (name,))
        self.cursor.execute("SELECT * FROM accounts WHERE name = ?", (name,))
        enabled_account = self.cursor.fetchone()
        self.connection.commit()
        print(f'\nEnabled account: {enabled_account}')
        return enabled_account

    def enable_many_accounts(self, list_account_names):
        for account in list_account_names:
            self.enable_account(account)

    # did not grok
    def get_category_tree(self, name=None):
        """
        Returns a nested dict from categories and enabled accounts databases.
        :param name: name of category i.e. Assets, Liabilities, etc.
        :return: nested dict
        """
        self.calculate_every_category()
        categories_query = "SELECT id, name, value FROM categories WHERE name=?"
        accounts_query = "SELECT id, name, value, remarks FROM enabled_accounts WHERE category_id=?"

        result = {'name': None, 'value': 0.0, 'children': []}

        # Select the category with the given name
        self.cursor.execute(categories_query, (name,))
        category = self.cursor.fetchone()
        if category is None:
            raise ValueError("No category found with name {}".format(name))
        result['name'] = category[1]
        result['value'] = category[2]

        # Select child categories
        self.cursor.execute("SELECT id, name, value FROM categories WHERE parent_id=?", (category[0],))
        child_categories = self.cursor.fetchall()

        # Recursively call get_category_tree for each child category and add resulting nested dict to children array
        for child_category in child_categories:
            result['children'].append(self.get_category_tree(name=child_category[1]))

        # Select child accounts
        self.cursor.execute(accounts_query, (category[0],))
        child_accounts = self.cursor.fetchall()
        self.connection.commit()

        # Add a nested dict to children array for each child account
        for child_account in child_accounts:
            result['children'].append({
                'name': child_account[1],
                'value': child_account[2],
                'remarks': child_account[3]
            })

        return result

    def get_category_names(self):
        """
        Returns a list of unique category names.
        :return: list of category names.
        """
        self.cursor.execute("SELECT DISTINCT name FROM categories")
        rows = self.cursor.fetchall()  # fetch all the results
        category_names = [row[0] for row in rows]  # extract the first column of each row
        return category_names

    # did not grok
    def get_subcategories(self, category_name):
        query = """
            SELECT c.name
            FROM categories AS c
            JOIN categories AS parent ON c.parent_id = parent.id
            WHERE parent.name = ?
        """

        self.cursor.execute(query, (category_name,))
        results = self.cursor.fetchall()

        subcategories = [row[0] for row in results]
        return subcategories

    # did not grok
    def get_leaf_categories(self, category_name):
        query = """
            WITH RECURSIVE subcategories AS (
                SELECT id, name, parent_id
                FROM categories
                WHERE name = ?
                UNION ALL
                SELECT c.id, c.name, c.parent_id
                FROM categories AS c
                INNER JOIN subcategories AS sub ON c.parent_id = sub.id
            )
            SELECT subcategories.name
            FROM subcategories
            LEFT JOIN categories AS child ON subcategories.id = child.parent_id
            WHERE child.id IS NULL
        """

        self.cursor.execute(query, (category_name,))
        results = self.cursor.fetchall()
        leaf_categories = [result[0] for result in results]
        if category_name in leaf_categories:
            leaf_categories.remove(category_name)
        return leaf_categories

    def get_account_by_name(self, name):
        """
        Returns account row given name parameter.
        :param name: str
        :return: dict
        """
        self.cursor.execute("SELECT * FROM accounts WHERE name=?", (name,))
        row = self.cursor.fetchone()
        if row is not None:
            columns = [desc[0] for desc in self.cursor.description]
            account_dict = dict(zip(columns, row))
            return account_dict
        else:
            return None

    def get_accounts(self, enabled=True):
        """
        Returns the names of either from enabled_accounts view or disabled accounts from the accounts table
        :param enabled: toggle mode
        :return: list of tuples
        """
        if enabled:
            self.cursor.execute("SELECT * FROM enabled_accounts")
        else:
            self.cursor.execute("SELECT * FROM accounts WHERE is_disabled = 1")

        rows = self.cursor.fetchall()
        account_names = [row[1] for row in rows]
        return account_names

    def get_all_account_names_in_category(self, name):
        query = """
            SELECT name FROM accounts
            WHERE category_id = (
                SELECT id
                FROM categories
                WHERE name = ?
            )
        """

        self.cursor.execute(query, (name,))
        results = self.cursor.fetchall()
        account_names = [row[0] for row in results]

        return account_names

