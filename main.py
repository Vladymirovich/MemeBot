import argparse
from src.data.database import create_tables
from src.data.fetcher import fetch_and_store_dexscreener_pairs
from src.analysis.analyzer import analyze_all_coins

def main():
    """Main function to run the bot."""
    parser = argparse.ArgumentParser(description="Crypto Coin Analyzer Bot")
    parser.add_argument('search_query', type=str, nargs='?', default="PEPE/SOL",
                        help='The search query for fetching new pairs (e.g., "PEPE/SOL").')
    args = parser.parse_args()

    print("Starting the bot...")

    # Create database tables
    print("Initializing database...")
    create_tables()
    print("Database initialization complete.")

    # Fetch new data
    print(f"Fetching new data for query: {args.search_query}...")
    fetch_and_store_dexscreener_pairs(args.search_query)
    print("Data fetching complete.")

    # Analyze data
    print("Analyzing data...")
    analyze_all_coins()
    print("Data analysis complete.")

    print("Bot finished running.")

if __name__ == '__main__':
    main()
