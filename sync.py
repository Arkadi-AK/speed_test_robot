import logging
import sys
import time
from typing import Any
from urllib.parse import urlparse

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def is_valid_url(url: str) -> bool:
    """Checks whether the string is a valid URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def get_url_from_user() -> str:
    """Requests the URL from the user or uses the default value."""
    default_url = "https://example-file.com/files/image/sample-image-1mb.jpg"
    user_input = input(
        "Enter URL for testing (or press Enter to use default): "
    ).strip()

    if not user_input:
        logger.info(f"Using default URL: {default_url}")
        return default_url

    if is_valid_url(user_input):
        logger.info(f"URL accepted: {user_input}")
        return user_input
    else:
        logger.error(
            "Invalid URL format. URL must start with http:// or https://.\nPlease try again.\n"
        )

        return get_url_from_user()


def measure_speed(url: str, attempts: int = 10) -> dict[str, Any]:
    """
    Measure internet speed by performing multiple requests to the specified URL.

    Args:
        url (str): URL to test against
        attempts (int): Number of requests to perform (default: 10)

    Returns:
        None: Results are printed to console
    """

    total_time = 0.0
    total_bytes = 0
    successful_attempts = 0
    failed_attempts = 0

    session = requests.Session()
    session.headers.update(
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )

    for i in range(attempts):
        try:
            start = time.perf_counter()

            with session.get(url, stream=True, timeout=30) as response:
                response.raise_for_status()

                downloaded = 0
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        downloaded += len(chunk)

            elapsed = time.perf_counter() - start

            if downloaded == 0:
                logger.warning(
                    f"Request {i + 1}: 0 bytes downloaded (possible caching or empty response)"
                )
                failed_attempts += 1
                continue

            total_time += elapsed
            total_bytes += downloaded
            successful_attempts += 1

        except requests.exceptions.Timeout:
            logger.error(f"Request {i + 1}: timeout (exceeded 30s limit)")
            failed_attempts += 1

        except requests.exceptions.ConnectionError:
            logger.error(f"Request {i + 1}: connection error (host unreachable)")
            failed_attempts += 1

        except requests.exceptions.HTTPError as e:
            logger.error(f"Request {i + 1}: HTTP error - {e}")
            failed_attempts += 1

        except Exception as e:
            logger.error(f"Request {i + 1}: unknown error - {e}")
            failed_attempts += 1

    return {
        "total_bytes": total_bytes,
        "total_time": total_time,
        "successful_attempts": successful_attempts,
    }


def print_results(results: dict[str, Any]) -> None:
    """
    Print formatted speed test results to console.

    Args:
        results: Dictionary containing test results from measure_speed()
    """
    total_bytes = results["total_bytes"]
    total_time = results["total_time"]
    successful_attempts = results["successful_attempts"]

    print("\n" + "=" * 50)
    logger.info("TEST RESULTS")
    print("-" * 50)

    if successful_attempts == 0:
        logger.error("No successful requests! Check URL and connection.")
        return

    avg_time = total_time / successful_attempts
    total_mb = total_bytes / 1024 / 1024
    speed_mb_s = total_mb / total_time

    logger.info(f"Total downloaded: {total_mb:.2f} MB")
    logger.info(f"Average request time: {avg_time:.3f} sec")
    logger.info(f"Average speed: {speed_mb_s:.2f} MB/s")


def main():
    """Main function to run the speed test program"""

    print("\n" + "=" * 50)
    print("Internet Speed Test")
    print("=" * 50)

    try:
        url = get_url_from_user()

        # Run the speed test
        results = measure_speed(url, attempts=10)
        print_results(results)

    except KeyboardInterrupt:
        logger.warning("\nTest interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Critical error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
