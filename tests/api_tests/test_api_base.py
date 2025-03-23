import pytest
import requests

@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    return session 