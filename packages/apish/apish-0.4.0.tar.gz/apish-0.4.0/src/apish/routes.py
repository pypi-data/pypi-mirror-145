import json
from abc import ABC, abstractmethod
from enum import Enum, auto
from itertools import chain
from typing import Callable, Iterator, List, Optional, Tuple

from fastapi.params import Depends
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from apish.base import Problem
from apish.utils import get_return_type


class CustomRoute(APIRoute):
    MAX_BODY_LENGTH = 400

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except Exception as exc:
                body = await request.body()
                try:
                    request.state.body = json.dumps(body)[: self.MAX_BODY_LENGTH]
                except Exception:  # pylint: disable=broad-except
                    request.state.body = str(body)[: self.MAX_BODY_LENGTH]
                raise exc

        return custom_route_handler


class Verb(Enum):
    GET = auto()
    PUT = auto()
    POST = auto()
    PATCH = auto()
    DELETE = auto()

    @classmethod
    def handler_names(cls) -> Iterator[str]:
        for verb in cls:
            yield verb.handler_name

    @property
    def handler_name(self):
        # pylint: disable=no-member
        return self.name.lower()


class RouteGenerator(ABC):
    @abstractmethod
    def routes(self, tags=None, prefix=None, dependencies=None) -> Iterator[APIRoute]:
        pass


class Namespace(RouteGenerator):
    _children: List[RouteGenerator]

    def __init__(
        self, tags=None, prefix: Optional[str] = None, dependencies: List[Depends] = None
    ):
        self._tags = tags
        self._prefix = prefix
        self._dependencies = dependencies
        self._children = []

    def add(self, route_generator: RouteGenerator) -> None:
        self._children.append(route_generator)

    def route(self, *args, **kwargs):
        def decorator(cls):
            self.add(cls(*args, **kwargs))
            return cls

        return decorator

    def routes(self, tags=None, prefix=None, dependencies=None) -> Iterator[APIRoute]:
        tags = (self._tags or []) + (tags or [])
        prefix = "".join(s for s in [prefix, self._prefix] if s is not None)
        dependencies = (self._dependencies or []) + (dependencies or [])
        return chain(*[child.routes(tags, prefix, dependencies) for child in self._children])


class Resource(RouteGenerator):

    _RESPONSES = {"4XX": {"model": Problem}}

    def __init__(
        self,
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None,
        dependencies: List[Depends] = None,
    ):
        self._prefix = prefix
        self._tags = tags
        self._dependencies = dependencies

    def handlers(self) -> Iterator[Tuple[Verb, Callable]]:
        for verb in Verb:
            if hasattr(self, verb.handler_name):
                yield (verb, getattr(self, verb.handler_name))

    def routes(self, tags=None, prefix=None, dependencies=None) -> Iterator[APIRoute]:
        tags = (self._tags or []) + (tags or [])
        prefix = "".join(s for s in [prefix, self._prefix] if s is not None)
        dependencies = (self._dependencies or []) + (dependencies or [])
        for (verb, handler) in self.handlers():
            yield self._route_from_handler(tags, prefix, verb, handler, dependencies)

    def _route_from_handler(self, tags, prefix, verb: Verb, handler, dependencies) -> APIRoute:
        # pylint: disable=too-many-arguments
        kwargs = {
            "path": prefix,
            "methods": [verb.name],
            "endpoint": handler,
            "summary": handler.__doc__,
            "status_code": 200,
            "tags": tags,
            "response_class": JSONResponse,
            "responses": self._RESPONSES,
            "dependencies": dependencies,
        }

        response_model = get_return_type(handler)
        if response_model is not None:
            kwargs["response_model"] = response_model

        return CustomRoute(**kwargs)
