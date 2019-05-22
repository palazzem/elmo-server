import pytest
import falcon

from falcon import testing
from server.api import create
from server.hooks import authorization_required, code_required


@pytest.fixture
def client():
    """Testing API client"""
    return testing.TestClient(create())


@pytest.fixture
def hooks_client():
    """Testing API client with a fake app"""

    class AuthorizationResponder(object):
        @falcon.before(authorization_required)
        def on_get(self, req, resp, token):
            resp.media = {"token": token}
            resp.status = falcon.HTTP_200

    class CodeResponder(object):
        @falcon.before(code_required)
        def on_get(self, req, resp, code):
            resp.media = {"code": code}
            resp.status = falcon.HTTP_200

    api = falcon.API()
    api.add_route("/hooks/authorization_required", AuthorizationResponder())
    api.add_route("/hooks/code_required", CodeResponder())
    return testing.TestClient(api)
