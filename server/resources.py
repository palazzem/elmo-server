import falcon
import logging

from elmo.api.client import ElmoClient
from elmo.api.exceptions import APIException, PermissionDenied

from .conf import settings
from .hooks import authorization_required


log = logging.getLogger(__name__)


class Authentication(object):
    """Authentication endpoint to retrieve an access token.

    Endpoints:
        POST /api/v0/auth/
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


@falcon.before(authorization_required)
class AlarmsResource(object):
    """Alarms resource to arm/disarm all Elmo System alarms.

    Endpoints:
        PUT /api/v0/alarms/
        DELETE /api/v0/alarms/
    """

    def on_put(self, req, resp, token):
        """Arm all alarms after gaining the system lock. Once the operation is
        completed with success, the system lock is released.
        The endpoint requires an `Authorization` header with a valid bearer
        token.

        Expected request:
        {
            "code": "str"
        }

        Args:
            req: Falcon `Request` object
            resp: Falcon `Response` object
            token: Bearer token that must be used to make the client request
        Raises:
            HTTPBadRequest: if the request misses mandatory fields
            HTTPServiceUnavailable: if the Elmo System returns a server error
        Returns:
            A JSON response with the access token.
        """
        code = req.media.get("code")
        if code is None:
            raise falcon.HTTPBadRequest(description="`code` is a required field")

        # Initialize the client with a bearer token
        client = ElmoClient(settings.base_url, settings.vendor)
        client._session_id = token

        try:
            with client.lock(code):
                client.arm()
        except PermissionDenied:
            raise falcon.HTTPUnauthorized(
                description="The bearer token is invalid or expired"
            )
        except APIException as e:
            # This status may lead to a case where the system is locked.
            # The global system lock is automatically released after one
            # minute. Unfortunately it's not possible to recover this state
            # other than providing credentials in every call (making useless
            # the bearer token).
            log.error("503 ServiceUnavailable: {}".format(e))
            raise falcon.HTTPServiceUnavailable(description="".format(e))

        resp.status = falcon.HTTP_200
        resp.media = {"alarms_armed": True}
