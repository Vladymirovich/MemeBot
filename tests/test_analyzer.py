import unittest
import configparser
from src.analysis.analyzer import is_coin_blacklisted, is_developer_blacklisted, is_coin_filtered, has_fake_volume_custom, get_rugcheck_data, is_contract_good, has_bundled_supply
from unittest.mock import patch, MagicMock

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        """Set up a mock config object for testing."""
        self.config = configparser.ConfigParser()
        self.config['CoinBlacklist'] = {'tokens': 'addr1,addr2'}
        self.config['DeveloperBlacklist'] = {'developers': 'dev1,dev2'}
        self.config['Filters'] = {'min_market_cap': '1000', 'min_liquidity': '5000'}
        self.config['FakeVolume'] = {'max_volume_to_liquidity_ratio': '3', 'min_txns_24h': '10', 'max_buy_sell_ratio': '10'}

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

    def test_has_fake_volume_custom(self):
        """Test the has_fake_volume_custom function."""
        # Test case 1: Coin should be flagged due to low transaction count
        coin1 = {'txns_h24_buys': 4, 'txns_h24_sells': 5, 'symbol': 'LOWTX', 'liquidity': 10000, 'market_cap': 20000, 'volume_h24': 20000}
        self.assertTrue(has_fake_volume_custom(coin1, self.config))

        # Test case 2: Coin should be flagged due to high buy/sell ratio
        coin2 = {'txns_h24_buys': 100, 'txns_h24_sells': 5, 'symbol': 'HIGHBUY', 'liquidity': 10000, 'market_cap': 20000, 'volume_h24': 20000}
        self.assertTrue(has_fake_volume_custom(coin2, self.config))

        # Test case 3: Coin should be flagged due to high volume-to-liquidity ratio
        coin3 = {'txns_h24_buys': 50, 'txns_h24_sells': 45, 'symbol': 'HIGHVOL', 'liquidity': 5000, 'market_cap': 20000, 'volume_h24': 20000}
        self.assertTrue(has_fake_volume_custom(coin3, self.config))

        # Test case 4: Coin should not be flagged
        coin4 = {'txns_h24_buys': 50, 'txns_h24_sells': 45, 'symbol': 'GOODCOIN', 'liquidity': 10000, 'market_cap': 20000, 'volume_h24': 20000}
        self.assertFalse(has_fake_volume_custom(coin4, self.config))

    @patch('src.analysis.analyzer.perform_rugcheck')
    def test_get_rugcheck_data(self, mock_perform_rugcheck):
        """Test the get_rugcheck_data function."""
        mock_rugcheck_data = MagicMock()
        mock_perform_rugcheck.return_value = mock_rugcheck_data

        result = get_rugcheck_data("test_address")
        self.assertEqual(result, mock_rugcheck_data)
        mock_perform_rugcheck.assert_called_once_with("test_address")

    def test_is_contract_good(self):
        """Test the is_contract_good function."""
        # Test case 1: Good contract
        good_data = MagicMock(rugged=False, result='Success')
        self.assertTrue(is_contract_good(good_data))

        # Test case 2: Rugged contract
        rugged_data = MagicMock(rugged=True, result='Success')
        self.assertFalse(is_contract_good(rugged_data))

        # Test case 3: Danger result
        danger_data = MagicMock(rugged=False, result='Danger')
        self.assertFalse(is_contract_good(danger_data))

    def test_has_bundled_supply(self):
        """Test the has_bundled_supply function."""
        # Test case 1: Bundled supply risk
        risk1 = MagicMock()
        risk1.name = "Top 10 holders high ownership"
        bundled_data = MagicMock(risks=[risk1])
        self.assertTrue(has_bundled_supply(bundled_data))

        # Test case 2: No bundled supply risk
        risk2 = MagicMock()
        risk2.name = "Some other risk"
        not_bundled_data = MagicMock(risks=[risk2])
        self.assertFalse(has_bundled_supply(not_bundled_data))

        # Test case 3: No risks
        no_risks_data = MagicMock(risks=[])
        self.assertFalse(has_bundled_supply(no_risks_data))

if __name__ == '__main__':
    unittest.main()
