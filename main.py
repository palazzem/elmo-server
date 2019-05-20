import logging

from server.api import create
from server.conf import settings
from elmo.settings.exceptions import ConfigNotValid


log = logging.getLogger(__name__)

try:
    # The application must not start without a valid configuration
    settings.is_valid()
except ConfigNotValid as e:
    log.critical(e)
    exit(1)

# Use AppEngine default entrypoint (gunicorn)
app = create()
