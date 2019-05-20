import falcon
import logging

from elmo.api.client import ElmoClient
from elmo.api.exceptions import APIException, PermissionDenied

from .conf import settings


log = logging.getLogger(__name__)


class Authentication(object):
    """Authentication endpoint to retrieve an access token.

    Endpoints:
        POST /api/v1/auth/
    """

    def on_post(self, req, resp):
        """Authenticate the user and returns an access token.

        Expected request:
        {
            "username": "str",
            "password": "str
        }

        Args:
            req: Falcon `Request` object
            resp: Falcon `Response` object
        Raises:
            HTTPBadRequest: if the request misses mandatory fields
            HTTPForbidden: if credentials are not valid
            HTTPServiceUnavailable: if the Elmo System returns a server error
        Returns:
            A JSON response with the access token.
        """
        client = ElmoClient(settings.base_url, settings.vendor)
        username = req.media.get("username")
        password = req.media.get("password")

        if username is None or password is None:
            raise falcon.HTTPBadRequest(description="Missing username and password")
        try:
            token = client.auth(username, password)
        except PermissionDenied:
            raise falcon.HTTPForbidden(description="Wrong username or password")
        except APIException as e:
            log.error("503 ServiceUnavailable: {}".format(e))
            raise falcon.HTTPServiceUnavailable(description="".format(e))

        resp.media = {"access_token": token}
        resp.status = falcon.HTTP_200
