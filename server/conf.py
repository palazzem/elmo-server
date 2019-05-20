import os

from elmo.settings import validators
from elmo.settings.base import BaseSettings
from elmo.settings.options import Option


class Settings(BaseSettings):
    """Application settings with lazy evaluation. Once they are imported
    for the first time, the evaluation happens. The module that is
    importing this instance must call `is_valid()` to validate the
    settings.
    """

    base_url = Option(
        default=os.getenv("ELMO_BASE_URL"),
        allow_null=False,
        validators=[validators.is_https_url],
    )
    vendor = Option(default=os.getenv("ELMO_VENDOR"), allow_null=False)


settings = Settings()
