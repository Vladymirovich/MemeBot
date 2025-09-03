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

*   **[Filters]**:
    *   `min_market_cap`: The minimum market cap for a coin to be analyzed.
    *   `min_liquidity`: The minimum liquidity for a coin to be analyzed.

*   **[CoinBlacklist]**:
    *   `tokens`: A comma-separated list of coin mint addresses to be ignored.

*   **[DeveloperBlacklist]**:
    *   `developers`: A comma-separated list of developer addresses to be ignored. (Note: This is a placeholder as developer addresses are not yet available from the current data source).

## Usage

To run the bot, execute the following command from the root directory of the project:
```bash
python3 main.py
```
This will:
1.  Initialize the SQLite database (`coins.db`).
2.  Fetch the latest data for the "PEPE/SOL" pair from Dexscreener.
3.  Run the (placeholder) analysis functions on the collected data.

## Testing

To run the tests, execute the following command from the root directory:
```bash
python3 -m unittest discover tests
```

This will discover and run all the tests in the `tests` directory.
