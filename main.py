import argparse
import asyncio
from src.data.database import create_tables
from src.data.fetcher import fetch_and_store_dexscreener_pairs
from src.data.pump_fetcher import listen_for_new_tokens
from src.analysis.analyzer import analyze_all_coins

async def run_dexscreener_flow(search_query):
    """Runs the Dexscreener data fetching and analysis flow."""
    print("Running Dexscreener flow...")

    # Fetch new data
    print(f"Fetching new data for query: {search_query}...")
    # In a real async app, this would be an async function
    fetch_and_store_dexscreener_pairs(search_query)
    print("Data fetching complete.")

    # Analyze data
    print("Analyzing data...")
    # In a real async app, this would be an async function
    analyze_all_coins()
    print("Data analysis complete.")

async def run_pump_fun_flow():
    """Runs the pump.fun real-time listener."""
    print("Running pump.fun listener...")
    await listen_for_new_tokens()

async def main():
    """Main function to run the bot."""
    parser = argparse.ArgumentParser(description="Crypto Coin Analyzer Bot")
    subparsers = parser.add_subparsers(dest='source', required=True, help='The data source to use.')

    # Dexscreener parser
    parser_dex = subparsers.add_parser('dexscreener', help='Fetch data from Dexscreener.')
    parser_dex.add_argument('search_query', type=str, nargs='?', default="PEPE/SOL",
                           help='The search query for fetching new pairs (e.g., "PEPE/SOL").')

    # pump.fun parser
    parser_pump = subparsers.add_parser('pumpfun', help='Listen for new coins on pump.fun.')

    # All parser
    parser_all = subparsers.add_parser('all', help='Run all data sources concurrently.')
    parser_all.add_argument('search_query', type=str, nargs='?', default="PEPE/SOL",
                           help='The search query for fetching new pairs (e.g., "PEPE/SOL").')

    args = parser.parse_args()

    print("Starting the bot...")

    # Create database tables
    print("Initializing database...")
    create_tables()
    print("Database initialization complete.")

    if args.source == 'dexscreener':
        await run_dexscreener_flow(args.search_query)
    elif args.source == 'pumpfun':
        await run_pump_fun_flow()
    elif args.source == 'all':
        print("Running all data sources concurrently...")
        await asyncio.gather(
            run_dexscreener_flow(args.search_query),
            run_pump_fun_flow()
        )

    print("Bot finished running.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
