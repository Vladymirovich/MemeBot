# Crypto Coin Analyzer Bot

This bot fetches data for new crypto coins from Dexscreener and pump.fun, stores it in a database, and analyzes it to identify patterns in coins that rug, pump, reach tier-1, or get listed on CEXs.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install dependencies:**
    Make sure you have Python 3 installed. Then, run the following command to install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure the bot:**
    The `config/config.ini` file is used for configuration. The default settings should be sufficient to get started.

## Configuration

The `config/config.ini` file allows you to customize the bot's behavior.

*   **[api]**:
    *   `dexscreener_api_url`: The base URL for the Dexscreener API.
    *   `pumpportal_websocket_url`: The WebSocket URL for the pumpportal.fun API.

*   **[database]**:
    *   `db_name`: The name of the SQLite database file.

*   **[Filters]**:
    *   `min_market_cap`: The minimum market cap for a coin to be analyzed.
    *   `min_liquidity`: The minimum liquidity for a coin to be analyzed.

*   **[CoinBlacklist]**:
    *   `tokens`: A comma-separated list of coin mint addresses to be ignored.

*   **[DeveloperBlacklist]**:
    *   `developers`: A comma-separated list of developer addresses to be ignored. (Note: This is a placeholder as developer addresses are not yet available from the current data source).

*   **[FakeVolume]**:
    *   `max_volume_to_liquidity_ratio`: The maximum ratio of 24-hour trading volume to liquidity. A high value can indicate wash trading.
    *   `min_txns_24h`: The minimum number of transactions (buys + sells) in the last 24 hours for a coin to be considered to have real volume.
    *   `max_buy_sell_ratio`: The maximum ratio of buys to sells (or sells to buys) for a coin to be considered to have real volume.

## Analysis Features

The bot performs several checks to identify potentially risky coins:

*   **Rug Check:** Integrates with `rugcheck.xyz` to check if a coin is a known rug pull or has a "Danger" rating.
*   **Bundled Supply Check:** Identifies coins with a high concentration of ownership, which can be a sign of manipulation.
*   **Fake Volume Check:** Uses heuristics based on transaction counts and buy/sell ratios to detect fake trading volume.

## Usage

To run the bot, you can use the following commands from the root directory of the project:

*   **Fetch data from Dexscreener and analyze it:**
    ```bash
    python3 main.py dexscreener "[search_query]"
    ```
    Example: `python3 main.py dexscreener "PEPE/SOL"`

*   **Listen for new coins on pump.fun:**
    ```bash
    python3 main.py pumpfun
    ```
    This will start a long-running process to listen for new token creations in real-time.

*   **Run both flows concurrently:**
    ```bash
    python3 main.py all "[search_query]"
    ```
    This will run the Dexscreener fetcher and the pump.fun listener at the same time.

## Testing

To run the tests, execute the following command from the root directory:
```bash
python3 -m unittest discover tests
```

This will discover and run all the tests in the `tests` directory.
