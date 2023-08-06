# -*- coding: utf-8 -*-
# copyright 2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from typing import List, Type

from pyramid.config import Configurator
from pyramid.request import Request
from cubicweb import (
    ValidationError,
    Unauthorized,
    UnknownEid,
    UniqueTogetherError,
    ViolatedConstraint,
    QueryError,
    Forbidden,
)
from rql import RQLSyntaxError

from cubicweb_api.routes import ROUTE_NAME_TO_CONTEXT, get_route_name


class JsonApiView:
    def __init__(self, request: Request):
        self.request = request
        self.cwreq = request.cw_request

    def __call__(self):
        return self.request.context.render()


class JsonApiExceptionView(JsonApiView):
    status_int = 500

    def __init__(self, exc: Exception, request: Request):
        super().__init__(request)
        self.exc = exc

    def __call__(self):
        self.request.response.status_int = self.status_int
        return {"error": self.exc.__class__.__name__, "message": str(self.exc)}


class JsonApiBadRequestView(JsonApiExceptionView):
    status_int = 400


class JsonApiUnauthorizedView(JsonApiExceptionView):
    status_int = 401


class JsonApiForbiddenView(JsonApiExceptionView):
    status_int = 403


def add_exception_view(
    config: Configurator,
    route_part: str,
    exception_view: Type[JsonApiExceptionView],
    exception: Type[Exception] = None,
):
    config.add_exception_view(
        exception_view,
        route_name=get_route_name(route_part),
        context=exception,
        renderer="json",
    )


def add_bad_request_view(
    config: Configurator, route_part: str, exception: Type[Exception]
):
    add_exception_view(config, route_part, JsonApiBadRequestView, exception)


def add_exception_views(config: Configurator, bad_request_routes: List[str]):
    for route_part in ROUTE_NAME_TO_CONTEXT:
        add_exception_view(config, route_part, JsonApiUnauthorizedView, Unauthorized)
        add_exception_view(config, route_part, JsonApiForbiddenView, Forbidden)
        add_exception_view(config, route_part, JsonApiExceptionView)

    for route_part in bad_request_routes:
        for exception_cls in (
            RQLSyntaxError,
            ValidationError,
            UnknownEid,
            UniqueTogetherError,
            ViolatedConstraint,
            QueryError,
        ):
            add_bad_request_view(config, route_part, exception_cls)


def includeme(config: Configurator):
    for route_part in ROUTE_NAME_TO_CONTEXT:
        config.add_view(
            JsonApiView,
            route_name=get_route_name(route_part),
            renderer="json",
            require_csrf=False,
        )
    add_exception_views(config, ["transaction", "rql"])
