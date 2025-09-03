import unittest
import configparser
from src.analysis.analyzer import is_coin_blacklisted, is_developer_blacklisted, is_coin_filtered

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        """Set up a mock config object for testing."""
        self.config = configparser.ConfigParser()
        self.config['CoinBlacklist'] = {'tokens': 'addr1,addr2'}
        self.config['DeveloperBlacklist'] = {'developers': 'dev1,dev2'}
        self.config['Filters'] = {'min_market_cap': '1000', 'min_liquidity': '5000'}

    def test_is_coin_blacklisted(self):
        """Test the is_coin_blacklisted function."""
        self.assertTrue(is_coin_blacklisted('addr1', self.config))
        self.assertFalse(is_coin_blacklisted('addr3', self.config))

    def test_is_developer_blacklisted(self):
        """Test the is_developer_blacklisted function."""
        self.assertTrue(is_developer_blacklisted('dev1', self.config))
        self.assertFalse(is_developer_blacklisted('dev3', self.config))

    def test_is_coin_filtered(self):
        """Test the is_coin_filtered function."""
        # Test case 1: Coin should be filtered due to low market cap
        coin1 = {'market_cap': 500, 'liquidity': 6000}
        self.assertTrue(is_coin_filtered(coin1, self.config))

        # Test case 2: Coin should be filtered due to low liquidity
        coin2 = {'market_cap': 1500, 'liquidity': 4000}
        self.assertTrue(is_coin_filtered(coin2, self.config))

        # Test case 3: Coin should not be filtered
        coin3 = {'market_cap': 1500, 'liquidity': 6000}
        self.assertFalse(is_coin_filtered(coin3, self.config))

        # Test case 4: Coin with no market cap or liquidity should not be filtered
        coin4 = {'market_cap': None, 'liquidity': None}
        self.assertFalse(is_coin_filtered(coin4, self.config))

if __name__ == '__main__':
    unittest.main()
