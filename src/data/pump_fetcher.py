import asyncio
import websockets
import json
import configparser
from src.data.database import get_db_connection

async def listen_for_new_tokens():
    """
    Connects to the pumpportal.fun WebSocket and listens for new token creation events.
    """
    print("Starting pump.fun fetcher...")
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    uri = config['api']['pumpportal_websocket_url']

    conn = get_db_connection()
    try:
        async with websockets.connect(uri) as websocket:
            # Subscribe to new token creation events
            payload = {
                "method": "subscribeNewToken",
            }
            await websocket.send(json.dumps(payload))
            print("Subscribed to new token events on pump.fun.")

            cursor = conn.cursor()
            async for message in websocket:
                try:
                    data = json.loads(message)
                    if 'mint' in data:
                        print(f"New token created: {data.get('name')} ({data.get('symbol')})")

                        try:
                            cursor.execute("""
                                INSERT INTO coins (mint_address, name, symbol, description, image_uri, source)
                                VALUES (?, ?, ?, ?, ?, ?)
                                ON CONFLICT(mint_address) DO NOTHING
                            """, (
                                data.get('mint'),
                                data.get('name'),
                                data.get('symbol'),
                                data.get('description'),
                                data.get('image_uri'),
                                'pump.fun'
                            ))
                            conn.commit()
                        except Exception as e:
                            print(f"Error inserting new token from pump.fun: {e}")
                except json.JSONDecodeError:
                    print(f"Received non-JSON message: {message}")
                except Exception as e:
                    print(f"An error occurred in the message loop: {e}")
    except Exception as e:
        print(f"Failed to connect to WebSocket: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(listen_for_new_tokens())
    except KeyboardInterrupt:
        print("Fetcher stopped by user.")
    except Exception as e:
        print(f"Fetcher failed: {e}")
