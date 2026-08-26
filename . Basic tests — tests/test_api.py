from unittest.mock import Mock, patch

from src.api_client import APIClient


@patch("src.api_client.requests.Session.get")
def test_successful_api_call(mock_get):

    mock_response = Mock()

    mock_response.status_code = 200

    mock_response.json.return_value = {
        "id": 1,
        "name": "John"
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    client = APIClient()

    result = client.get("/users")

    assert result["id"] == 1
    assert result["name"] == "John"


@patch("src.api_client.requests.Session.get")
def test_unauthorized_api(mock_get):

    mock_response = Mock()

    mock_response.status_code = 401

    mock_get.return_value = mock_response

    client = APIClient()

    try:
        client.get("/users")
        assert False
    except Exception as error:
        assert "401 Unauthorized" in str(error)


@patch("src.api_client.requests.Session.get")
def test_timeout(mock_get):

    import requests

    mock_get.side_effect = requests.exceptions.Timeout()

    client = APIClient()

    try:
        client.get("/users")
        assert False
    except Exception as error:
        assert "timed out" in str(error)
