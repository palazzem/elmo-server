class AreasResource(object):
    """Areas resource to arm/disarm all the alerts for an area.
    It requires an authenticated access token.

    Usage:
        PUT /api/v1/areas/: arm the status of all alerts
        DELETE /api/v1/areas/: disarm the status of all alerts
    """

    def on_put(self, req, resp):
        """TODO"""
        pass

    def on_delete(self, req, resp):
        """TODO"""
        pass
