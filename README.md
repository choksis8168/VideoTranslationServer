# Video Translation Server

## Introduction

The Video Translation client library provides an efficient way to poll the status of a video translation job from a server. It uses adaptive polling with exponential backoff and jitter to minimize unnecessary requests and delays. This guide demonstrates how to use and configure the client library. 

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

## Implementation of Client

Here, I will explain the rationale behind several core features implemented in the client. 

### Asynchronous Polling

Asynchronous programming is at the core of the client’s design, allowing it to make non-blocking HTTP requests. By leveraging `asyncio` and `aiohttp`, the client can wait for responses without blocking other tasks in the application. This asynchronous approach makes it suitable for applications that may need to perform other work while waiting for the job status. Rather than pausing the entire application to wait for each server response, asynchronous polling lets the client request updates, wait efficiently, and process results as they arrive, enhancing responsiveness and usability.

### Exponential Backoff

Polling a server too frequently can cause unnecessary load, especially if a job takes time to complete. To mitigate this, I had the client employ exponential backoff where the wait time between each polling attempt increases exponentially. For example, if the initial wait time is 1 second and the backoff factor is 2, the client will wait 1 second before the first retry, 2 seconds before the next, then 4, 8, and so on. This strategy reduces the frequency of requests over time, thereby decreasing server load and lowering costs. 

### Jitter
To further improve the polling mechanism, jitter (a small amount of randomness) is added to the wait times. By adding a random variation to each wait time, jitter helps ensure that requests from different clients are spread out, reducing the risk of spikes in server load. In the client, jitter is implemented as a small random value added to or subtracted from each backoff interval, ensuring that each retry interval is slightly unique.
