import sqlite3
import configparser

def get_db_connection(db_name=None):
    """Gets a database connection."""
    if not db_name:
        config = configparser.ConfigParser()
        config.read('config/config.ini')
        db_name = config['database']['db_name']
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables(conn=None):
    """Creates the necessary tables in the database."""
    close_conn_after = False
    if conn is None:
        conn = get_db_connection()
        close_conn_after = True

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mint_address TEXT UNIQUE NOT NULL,
        name TEXT,
        symbol TEXT,
        description TEXT,
        image_uri TEXT,
        created_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_updated_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        market_cap REAL,
        liquidity REAL,
        price_usd REAL,
        txns_h24_buys INTEGER,
        txns_h24_sells INTEGER,
        source TEXT,
        rug_pull BOOLEAN DEFAULT FALSE,
        pump BOOLEAN DEFAULT FALSE,
        tier1 BOOLEAN DEFAULT FALSE,
        cex_listed BOOLEAN DEFAULT FALSE,
        bundled_supply BOOLEAN DEFAULT FALSE
    )
    """)

    conn.commit()

    if close_conn_after:
        conn.close()

if __name__ == '__main__':
    conn = get_db_connection()
    create_tables(conn)
    conn.close()
    print("Database tables created successfully.")
