import falcon

from .resources import Authentication


def create():
    """Create a Falcon application to expose an API for the Elmo System.
    A valid configuration is required otherwise `None` is returned.

    Returns:
        A `falcon.API()` instance, populated with API endpoints for Elmo System
    """
    # Initialize the API
    api = falcon.API()
    api.add_route("/api/v0/auth", Authentication())
    return api
