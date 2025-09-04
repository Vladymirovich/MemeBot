import configparser
import time
from src.data.database import get_db_connection
from rugcheck import rugcheck as perform_rugcheck

def get_config():
    """Reads the configuration file."""
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    return config

def is_coin_blacklisted(mint_address, config):
    """Checks if a coin is in the blacklist."""
    blacklisted_tokens = config['CoinBlacklist']['tokens'].split(',')
    return mint_address in blacklisted_tokens

def is_developer_blacklisted(developer_address, config):
    """Checks if a developer is in the blacklist."""
    # NOTE: Developer address is not available in Dexscreener data yet.
    # This is a placeholder.
    blacklisted_developers = config['DeveloperBlacklist']['developers'].split(',')
    return developer_address in blacklisted_developers

def is_coin_filtered(coin, config):
    """Checks if a coin meets the filter criteria."""
    min_market_cap = float(config['Filters']['min_market_cap'])
    min_liquidity = float(config['Filters']['min_liquidity'])

    if coin['market_cap'] and coin['market_cap'] < min_market_cap:
        return True
    if coin['liquidity'] and coin['liquidity'] < min_liquidity:
        return True

    return False

def get_rugcheck_data(mint_address):
    """
    Gets the rugcheck data for a given mint address.
    """
    try:
        return perform_rugcheck(mint_address)
    except SystemExit:
        print(f"Rugcheck library called exit() for {mint_address}. Treating as an error.")
        return None
    except Exception as e:
        print(f"Error getting rugcheck data for {mint_address}: {e}")
        return None

def is_contract_good(rugcheck_data):
    """
    Checks if a contract is marked as 'Good' based on rugcheck data.
    """
    if not rugcheck_data:
        return False
    if rugcheck_data.rugged:
        print(f"Coin {rugcheck_data.token_address} is rugged.")
        return False
    if rugcheck_data.result == 'Danger':
        print(f"Coin {rugcheck_data.token_address} has a 'Danger' result.")
        return False
    return True

def has_bundled_supply(rugcheck_data):
    """
    Checks for signs of bundled supply from rugcheck data.
    """
    if not rugcheck_data or not rugcheck_data.risks:
        return False

    bundled_supply_risks = [
        "Top 10 holders high ownership",
        "Single holder ownership",
        "High ownership"
    ]

    for risk in rugcheck_data.risks:
        if risk.name in bundled_supply_risks:
            print(f"Coin {rugcheck_data.token_address} has bundled supply risk: {risk.name}")
            return True
    return False

def has_fake_volume_custom(coin, config):
    """
    Checks for signs of fake volume using custom heuristics.
    """
    max_volume_to_liquidity_ratio = float(config['FakeVolume']['max_volume_to_liquidity_ratio'])
    min_txns_24h = int(config['FakeVolume']['min_txns_24h'])
    max_buy_sell_ratio = float(config['FakeVolume']['max_buy_sell_ratio'])

    volume_h24 = coin['volume_h24']
    liquidity = coin['liquidity']
    txns_buys = coin['txns_h24_buys']
    txns_sells = coin['txns_h24_sells']

    if liquidity and volume_h24 and liquidity > 0:
        if (volume_h24 / liquidity) > max_volume_to_liquidity_ratio:
            print(f"Coin {coin['symbol']} has high volume-to-liquidity ratio.")
            return True

    if txns_buys is not None and txns_sells is not None:
        total_txns = txns_buys + txns_sells
        if total_txns < min_txns_24h:
            print(f"Coin {coin['symbol']} has very few transactions in the last 24h.")
            return True

        if txns_sells > 0 and (txns_buys / txns_sells) > max_buy_sell_ratio:
            print(f"Coin {coin['symbol']} has a very high buy/sell ratio.")
            return True

        if txns_buys > 0 and (txns_sells / txns_buys) > max_buy_sell_ratio:
            print(f"Coin {coin['symbol']} has a very high sell/buy ratio.")
            return True

    return False

def is_rug_pull(coin_id):
    """
    Analyzes a coin to determine if it's a rug pull.
    Placeholder function.
    """
    # TODO: Implement rug pull detection logic
    print(f"Analyzing coin {coin_id} for rug pull...")
    return False

def is_pump(coin_id):
    """
    Analyzes a coin to determine if it's a pump.
    Placeholder function.
    """
    # TODO: Implement pump detection logic
    print(f"Analyzing coin {coin_id} for pump...")
    return False

def is_tier1(coin_id):
    """
    Analyzes a coin to determine if it has reached tier 1.
    Placeholder function.
    """
    # TODO: Implement tier 1 detection logic
    print(f"Analyzing coin {coin_id} for tier 1 status...")
    return False

def is_cex_listed(coin_id):
    """
    Analyzes a coin to determine if it's listed on a CEX.
    Placeholder function.
    """
    # TODO: Implement CEX listing detection logic
    print(f"Analyzing coin {coin_id} for CEX listing...")
    return False

def analyze_all_coins():
    """
    Analyzes all coins in the database and updates their status.
    """
    config = get_config()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coins")
    coins = cursor.fetchall()

    for coin in coins:
        rugcheck_data = get_rugcheck_data(coin['mint_address'])
        time.sleep(1) # To avoid rate limiting

        # Check if the contract is good
        if not is_contract_good(rugcheck_data):
            print(f"Contract for coin {coin['symbol']} ({coin['mint_address']}) is not good. Skipping.")
            continue

        # Check for bundled supply
        if has_bundled_supply(rugcheck_data):
            cursor.execute("UPDATE coins SET bundled_supply = TRUE WHERE id = ?", (coin['id'],))
            conn.commit()
            print(f"Coin {coin['symbol']} ({coin['mint_address']}) is blacklisted due to bundled supply.")
            # We might want to skip further analysis for bundled supply coins
            # continue

        # Check blacklists
        if is_coin_blacklisted(coin['mint_address'], config):
            print(f"Coin {coin['symbol']} ({coin['mint_address']}) is blacklisted. Skipping.")
            continue

        # NOTE: Developer address is not available yet.
        # if is_developer_blacklisted(coin['developer_address'], config):
        #     print(f"Developer of coin {coin['symbol']} is blacklisted. Skipping.")
        #     continue

        # Apply filters
        if is_coin_filtered(coin, config):
            print(f"Coin {coin['symbol']} is filtered out. Skipping.")
            continue

        # Check for fake volume
        if has_fake_volume_custom(coin, config):
            print(f"Coin {coin['symbol']} has signs of fake volume. Skipping.")
            continue

        coin_id = coin['id']

        rug_pull = is_rug_pull(coin_id)
        pump = is_pump(coin_id)
        tier1 = is_tier1(coin_id)
        cex_listed = is_cex_listed(coin_id)

        cursor.execute("""
            UPDATE coins
            SET rug_pull = ?, pump = ?, tier1 = ?, cex_listed = ?, last_updated_timestamp = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (rug_pull, pump, tier1, cex_listed, coin_id))
        conn.commit()

    conn.close()

if __name__ == '__main__':
    analyze_all_coins()
    print("Finished analyzing all coins.")
