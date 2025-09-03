import unittest
from unittest.mock import patch, MagicMock
import os
import sqlite3
from src.data.fetcher import fetch_and_store_dexscreener_pairs
from src.data.database import get_db_connection, create_tables

class TestFetcher(unittest.TestCase):

    test_db_name = "test_fetcher.db"

    def setUp(self):
        """Set up a test database and connection."""
        self.conn = get_db_connection(self.test_db_name)
        create_tables(self.conn)

    def tearDown(self):
        """Tear down the database and connection."""
        self.conn.close()
        os.remove(self.test_db_name)

    @patch('requests.get')
    def test_fetch_and_store_dexscreener_pairs(self, mock_get):
        """Test fetching and storing pairs from Dexscreener."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "pairs": [
                {
                    "pairAddress": "pair_address",
                    "baseToken": {"address": "test_token_address", "name": "Test Token", "symbol": "TEST"},
                    "marketCap": 1000000,
                    "liquidity": {"usd": 50000},
                    "priceUsd": "1.23",
                    "txns": {"h24": {"buys": 100, "sells": 50}},
                    "info": {"description": "A test token.", "imageUrl": "http://example.com/image.png"}
                }
            ]
        }
        mock_get.return_value = mock_response

        # Call the function to be tested
        fetch_and_store_dexscreener_pairs("TEST/SOL", self.conn)

        # Assert that requests.get was called correctly
        mock_get.assert_called_once_with("https://api.dexscreener.com/latest/dex/search?q=TEST/SOL")

        # Assert that the data was inserted into the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM coins WHERE mint_address='test_token_address'")
        coin = cursor.fetchone()

        self.assertIsNotNone(coin)
        self.assertEqual(coin['name'], "Test Token")
        self.assertEqual(coin['symbol'], "TEST")
        self.assertEqual(coin['price_usd'], 1.23)
        self.assertEqual(coin['txns_h24_buys'], 100)

if __name__ == '__main__':
    unittest.main()
