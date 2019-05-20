import falcon
import logging

from elmo.settings.exceptions import ConfigNotValid

from .conf import settings
from .resources import Authentication, AreasResource


log = logging.getLogger(__name__)


def create():
    """Create a Falcon application to expose a REST API for the Elmo System.
    A valid configuration is required otherwise `None` is returned.
    """
    try:
        settings.is_valid()
    except ConfigNotValid as e:
        # The application cannot start without a valid configuration
        log.critical(e)
        return None

    # Initialize the API
    api = falcon.API()
    api.add_route("/api/v0/auth", Authentication())
    api.add_route("/api/v0/areas", AreasResource())
    return api
