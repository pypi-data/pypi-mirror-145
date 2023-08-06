import os

import uvicorn
from starlette.applications import Starlette


_DEFAULTS = {"port": "8080"}


def run(app: Starlette, **kwargs):
    # The log_config argument takes a logging.dictConfig that is applied to the
    # uvicorn logging.

    overrides = {}
    port = os.environ.get("SERVER_PORT")
    if port is not None:
        overrides["port"] = port
    uvicorn.run(app, **{**_DEFAULTS, **overrides, **kwargs})
