import asyncio
import random
import logging
from typing import Callable, Optional

import aiohttp

class VideoTranslationClient:
    def __init__(
        self,
        base_url: str,
        max_attempts: int = 10,
        max_wait_time: int = 60,
        initial_wait_time: float = 1.0,
        backoff_factor: float = 2.0,
        jitter: float = 0.5,
        logger: Optional[logging.Logger] = None,
    ):
        self.base_url = base_url
        self.max_attempts = max_attempts
        self.max_wait_time = max_wait_time
        self.initial_wait_time = initial_wait_time
        self.backoff_factor = backoff_factor
        self.jitter = jitter
        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    async def get_status(
        self, on_update: Optional[Callable[[str], None]] = None
    ) -> str:
        attempt = 0
        wait_time = self.initial_wait_time
        total_elapsed_time = 0

        async with aiohttp.ClientSession() as session:
            while attempt < self.max_attempts and total_elapsed_time < self.max_wait_time:
                try:
                    async with session.get(f"{self.base_url}/status") as response:
                        response.raise_for_status()
                        data = await response.json()
                        result = data.get("result")
                        self.logger.info(f"Attempt {attempt + 1}: Status - {result}")

                        if on_update:
                            on_update(result)

                        if result in ["completed", "error"]:
                            return result

                        # Calculate next wait time with jitter
                        sleep_time = wait_time + random.uniform(-self.jitter, self.jitter)
                        sleep_time = max(0, sleep_time)
                        await asyncio.sleep(sleep_time)
                        total_elapsed_time += sleep_time
                        wait_time *= self.backoff_factor
                        attempt += 1

                except aiohttp.ClientError as e:
                    self.logger.error(f"Request failed: {e}")
                    # Implement retries for transient errors
                    sleep_time = wait_time + random.uniform(-self.jitter, self.jitter)
                    sleep_time = max(0, sleep_time)
                    await asyncio.sleep(sleep_time)
                    total_elapsed_time += sleep_time
                    wait_time *= self.backoff_factor
                    attempt += 1

            return "timeout"
