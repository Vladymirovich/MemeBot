from src.data.database import create_tables
from src.data.fetcher import fetch_and_store_dexscreener_pairs
from src.analysis.analyzer import analyze_all_coins

def main():
    """Main function to run the bot."""
    print("Starting the bot...")

    # Create database tables
    print("Initializing database...")
    create_tables()
    print("Database initialization complete.")

    # Fetch new data
    # For now, we'll continue to search for "PEPE/SOL" as an example
    print("Fetching new data...")
    fetch_and_store_dexscreener_pairs("PEPE/SOL")
    print("Data fetching complete.")

    # Analyze data
    print("Analyzing data...")
    analyze_all_coins()
    print("Data analysis complete.")

    print("Bot finished running.")

if __name__ == '__main__':
    main()
