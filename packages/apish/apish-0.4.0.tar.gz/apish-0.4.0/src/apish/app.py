import logging

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from starlette.exceptions import HTTPException

from apish.base import Problem
from apish.metadata import Metadata
from apish.routes import Namespace, Resource, RouteGenerator

ns = Namespace(["Generic"])


log = logging.getLogger(__name__)


@ns.route("/metadata")
class Info(Resource):
    async def get(self, request: Request) -> Metadata:
        """Show API metadata"""
        return request.app.metadata


@ns.route("/health")
class Health(Resource):
    async def get(self):
        """Show health status"""
        return {"status": "ok"}


async def from_validation_error(_request: Request, exc: RequestValidationError):
    body = jsonable_encoder(Problem(title="Validation error", status=400, detail=exc.errors()))
    return JSONResponse(status_code=400, content=body)


async def from_http_exception(_request: Request, exc: HTTPException):
    problem = Problem(title=exc.detail, status=exc.status_code, detail={})
    body = jsonable_encoder(problem)
    # pylint: disable=no-member
    return JSONResponse(status_code=problem.status, content=body)


async def from_uncaught_exception(request: Request, exc: Exception):
    problem = Problem(title="Internal Server Error", status=500, detail={})
    body = jsonable_encoder(problem)
    log.error("Unhandled exception (exception: %s, body: %s)", exc, request.state.body)
    # pylint: disable=no-member
    return JSONResponse(status_code=problem.status, content=body)


class Application(FastAPI):
    def __init__(self, root: str, metadata: Metadata, **kwargs):
        self.root = root
        self.metadata = metadata
        exception_handlers = {
            HTTPException: from_http_exception,
            RequestValidationError: from_validation_error,
            Exception: from_uncaught_exception,
        }
        super().__init__(
            root_path="",
            title=metadata.title,
            version=metadata.version.api,
            exception_handlers=exception_handlers,  # type: ignore
            openapi_url=f"{root}/openapi.json",
            docs_url=f"{root}/docs",
            redoc_url=None,
            **kwargs,
        )
        self.add(ns)

    def add(self, route_generator: RouteGenerator) -> None:
        for route in route_generator.routes(prefix=self.root):
            self.routes.append(route)

    def openapi(self):
        openapi = super().openapi()
        if self.metadata.contact:
            openapi["info"]["contact"] = self.metadata.contact.dict(exclude_unset=True)
        if self.metadata.api_id:
            openapi["info"]["x-api-id"] = self.metadata.api_id
        if self.metadata.audience:
            openapi["info"]["x-audience"] = self.metadata.audience
        return openapi
