import requests
import configparser
from src.data.database import get_db_connection

def get_api_url(service):
    """Gets the API URL from the config file."""
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    return config['api'][service]

def fetch_and_store_dexscreener_pairs(search_query, conn=None):
    """Fetches new pairs from Dexscreener and stores them in the database."""
    api_url = get_api_url('dexscreener_api_url')
    search_url = f"{api_url}dex/search?q={search_query}"

    try:
        response = requests.get(search_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        if 'pairs' in data and data['pairs']:
            close_conn_after = False
            if conn is None:
                conn = get_db_connection()
                close_conn_after = True

            cursor = conn.cursor()

            for pair in data['pairs']:
                try:
                    cursor.execute("""
                        INSERT INTO coins (mint_address, name, symbol, description, image_uri, market_cap, liquidity, price_usd, txns_h24_buys, txns_h24_sells, source)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(mint_address) DO UPDATE SET
                            name = excluded.name,
                            symbol = excluded.symbol,
                            description = excluded.description,
                            image_uri = excluded.image_uri,
                            market_cap = excluded.market_cap,
                            liquidity = excluded.liquidity,
                            price_usd = excluded.price_usd,
                            txns_h24_buys = excluded.txns_h24_buys,
                            txns_h24_sells = excluded.txns_h24_sells,
                            last_updated_timestamp = CURRENT_TIMESTAMP
                    """, (
                        pair.get('baseToken', {}).get('address'),
                        pair.get('baseToken', {}).get('name'),
                        pair.get('baseToken', {}).get('symbol'),
                        pair.get('info', {}).get('description', ''), # Dexscreener doesn't provide a top-level description
                        pair.get('info', {}).get('imageUrl', ''),
                        pair.get('marketCap'),
                        pair.get('liquidity', {}).get('usd'),
                        pair.get('priceUsd'),
                        pair.get('txns', {}).get('h24', {}).get('buys'),
                        pair.get('txns', {}).get('h24', {}).get('sells'),
                        'dexscreener'
                    ))
                    print(f"Inserted or updated pair: {pair.get('baseToken', {}).get('symbol')}")
                except Exception as e:
                    print(f"Error inserting pair {pair.get('pairAddress')}: {e}")

            conn.commit()
            if close_conn_after:
                conn.close()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Dexscreener: {e}")

if __name__ == '__main__':
    conn = get_db_connection()
    fetch_and_store_dexscreener_pairs("PEPE/SOL", conn)
    conn.close()
    print("Finished fetching and storing Dexscreener pairs.")
