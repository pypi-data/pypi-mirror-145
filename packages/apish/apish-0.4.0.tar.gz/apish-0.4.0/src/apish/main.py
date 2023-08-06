import logging
from pydantic import BaseModel
from starlette.requests import Request

from apish.app import Application
from apish.metadata import Contact, Metadata, Version
from apish.routes import Namespace, Resource
from apish.server import run

ns = Namespace([])


log = logging.getLogger(__name__)


class Foo(BaseModel):
    bar: str
    baz: str


LOG_CONFIG = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
            "stream": "ext://sys.stdout",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "disable_existing_loggers": False,
}


@ns.route("/boom")
class BoomResource(Resource):
    def get(self):
        log.info("Test")
        raise Exception(100 * "boom!")

    async def post(self, request: Request, body: Foo):
        x = await request.body()
        raise Exception(100 * "boom!")


metadata = Metadata(
    title="<title>",
    version=Version(app="v0.1.1", api="v0.1.0"),
    description=None,
    contact=Contact(name="name", url="http://test.com", email=None),
    api_id="49786b4b-1889-46ec-bd72-27f332436e6f",
    audience="company-internal",
)

app = Application("", metadata)
app.add(ns)


run(app, log_config=LOG_CONFIG)
