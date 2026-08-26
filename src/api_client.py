import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class APIClient:

    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL")
        self.api_key = os.getenv("API_KEY")

        if not self.base_url:
            raise ValueError("API_BASE_URL is not configured")

        self.session = requests.Session()

        self.session.headers.update({
            "Accept": "application/json"
        })

        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}"
            })

    def get(self, endpoint, params=None):

        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        try:
            logger.info("Calling API: %s", endpoint)

            response = self.session.get(
                url,
                params=params,
                timeout=10
            )

            if response.status_code == 401:
                raise Exception("401 Unauthorized: Invalid API credentials")

            if response.status_code == 403:
                raise Exception("403 Forbidden: Access denied")

            if response.status_code == 404:
                raise Exception("404 Not Found: Resource does not exist")

            if response.status_code == 429:
                raise Exception("429 Too Many Requests: Rate limit exceeded")

            response.raise_for_status()

            try:
                return response.json()

            except ValueError:
                raise Exception("Invalid JSON response from API")

        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            raise Exception("API request timed out")

        except requests.exceptions.ConnectionError:
            logger.error("Unable to connect to API")
            raise Exception("API connection failed")

        except requests.exceptions.RequestException as error:
            logger.error("API request failed: %s", error)
            raise Exception(f"API request failed: {error}")
