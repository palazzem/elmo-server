import falcon

from .resources import AreasResource


# Initialize the API
api = falcon.API()
api.add_route("/api/v0/areas", AreasResource())
