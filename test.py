import threading
import time
import asyncio
import logging
from server import app
from client import VideoTranslationClient

def run_server():
    app.run(host="127.0.0.1", port=5000)

def on_status_update(status):
    print(f"Status Updated: {status}")

async def main():
    # Initialize the client
    client = VideoTranslationClient(base_url="http://127.0.0.1:5000")

    # Get the status
    final_status = await client.get_status(on_update=on_status_update)
    print(f"Final Status: {final_status}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Start the server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Allow some time for the server to start
    time.sleep(1)

    # Run the async main function
    asyncio.run(main())
