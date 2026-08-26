import logging

from src.api_client import APIClient
from src.models import User

logger = logging.getLogger(__name__)


class APIExtractor:

    def __init__(self):
        self.client = APIClient()

    def fetch_users(self):

        data = self.client.get("/users")

        if not data:
            logger.warning("API returned empty data")
            return []

        users = []

        for item in data:
            try:
                user = User.model_validate(item)
                users.append(user)

            except Exception as error:
                logger.error(
                    "Invalid user data: %s",
                    error
                )

        logger.info(
            "Successfully extracted %d users",
            len(users)
        )

        return users
