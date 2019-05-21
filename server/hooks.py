import falcon

from uuid import UUID


def authorization_required(req, resp, resource, params):
    """Require Authorization header before accepting clients request.
    The Authorization header must include the session identifier
    retrieved during a client login.

    When this hook is used, the Authorization header is extracted as
    `token` kwarg, and is available in the responder function.

    Args:
        req: Falcon `Request` object
        resp: Falcon `Response` object
        resource: Falcon `Resource` after routing
        params: Parameters to pass to a responder function
    Raises:
        HTTPUnauthorized: if the Authorization header is empty or not valid
    """
    if req.auth is None:
        raise falcon.HTTPUnauthorized("Authentication credentials were not provided")

    try:
        # Extract the bearer token and validate if it's a valid UUID
        token = req.auth.split(" ")[1]
        UUID(token, version=4)
    except (ValueError, IndexError, AttributeError):
        raise falcon.HTTPUnauthorized("Incorrect authentication credentials")

    params["token"] = token
