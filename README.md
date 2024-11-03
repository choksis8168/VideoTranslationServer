# Video Translation Client Library

## Introduction

The Video Translation Client Library provides an efficient way to poll the status of a video translation job from a server. It uses adaptive polling with exponential backoff and jitter to minimize unnecessary requests and delays. This guide will help you understand how to install, configure, and use the client library in your projects.

---

## Installation

### Prerequisites

- **Python 3.7 or higher**: Ensure you have Python installed on your system.
- **Dependencies**: The library requires `aiohttp` for asynchronous HTTP requests.

### Installing Dependencies

If you haven't already installed `aiohttp`, you can do so using `pip`:

```bash
pip install aiohttp
```

### Clone the Repository

Clone the repository containing the client library:

```bash
git clone https://github.com/yourusername/video-translation-client.git
```

---

## Usage

In your Python script, import the `VideoTranslationClient` class:

```python
from client import VideoTranslationClient
```

### Example

Here's a simple example of how to use the client library to poll the server for the job status:

```python
import asyncio

async def main():
    # Initialize the client with the server's base URL
    client = VideoTranslationClient(base_url="http://127.0.0.1:5000")

    # Start polling for the job status
    final_status = await client.get_status()

    # Print the final status
    print(f"Final Status: {final_status}")

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
```

### Using a callback function

You can provide a callback function to receive real-time updates on the job status:

```python
import asyncio

def on_status_update(status):
    print(f"Status Updated: {status}")

async def main():
    client = VideoTranslationClient(base_url="http://127.0.0.1:5000")

    final_status = await client.get_status(on_update=on_status_update)
    print(f"Final Status: {final_status}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Configuring the client 

The `VideoTranslationClient` class provides several parameters to customize its behavior:

- `base_url (str)`: The base URL of the server.
- `max_attempts (int)`: Maximum number of polling attempts (default: 10).
- `max_wait_time (int)`: Maximum total wait time in seconds (default: 60).
- `initial_wait_time (float)`: Initial wait time between attempts in seconds (default: 1.0).
- `backoff_factor (float)`: Multiplier for exponential backoff (default: 2.0).
- `jitter (float)`: Maximum amount of random jitter to add to wait times (default: 0.5).

### Handling Errors and Timeouts

The `get_status` method returns the final status of the job, which can be one of the following:

- `'completed'`: The job completed successfully.
- `'error'`: The job encountered an error.
- `'timeout'`: The polling operation timed out based on the max_attempts or max_wait_time parameters.

## Running the Test

A test script is provided to demonstrate the usage of the client library in conjunction with the server.

### Starting the Server

Start the server as follows: 

```bash
python server.py
```

The server will start listening on `http://127.0.0.1:5000`.

### Running the Test Script

```bash
python test.py
```

The script will:

- Start the server (if not already running).
- Use the client library to poll the server for the job status.
- Print status updates and the final status.

  
