import configparser
from src.data.database import get_db_connection

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
    conn.close()

    for coin in coins:
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

        coin_id = coin['id']

        rug_pull = is_rug_pull(coin_id)
        pump = is_pump(coin_id)
        tier1 = is_tier1(coin_id)
        cex_listed = is_cex_listed(coin_id)

        conn = get_db_connection()
        cursor = conn.cursor()
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
