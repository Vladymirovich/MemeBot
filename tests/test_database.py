import unittest
import sqlite3
import os
from src.data.database import get_db_connection, create_tables

class TestDatabase(unittest.TestCase):

    test_db_name = "test_coins.db"

    def setUp(self):
        """Set up a test database before each test."""
        self.conn = get_db_connection(self.test_db_name)
        create_tables(self.conn)

    def tearDown(self):
        """Tear down the test database after each test."""
        self.conn.close()
        os.remove(self.test_db_name)

    def test_db_connection(self):
        """Test that a database connection can be established."""
        self.assertIsNotNone(self.conn)
        self.assertIsInstance(self.conn, sqlite3.Connection)

    def test_create_tables(self):
        """Test that the coins table is created."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='coins'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)

if __name__ == '__main__':
    unittest.main()
