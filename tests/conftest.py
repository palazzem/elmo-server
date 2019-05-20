import pytest

from falcon import testing
from server.api import create


@pytest.fixture
def client():
    """Testing API client"""
    return testing.TestClient(create())
