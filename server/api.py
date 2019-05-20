import falcon

from .conf import settings
from .resources import AreasResource


# Check required configuration
settings.is_valid()

# Initialize the API
api = falcon.API()
api.add_route("/api/v0/areas", AreasResource())
