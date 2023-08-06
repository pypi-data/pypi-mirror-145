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

from cubicweb.pyramid.core import CubicWebPyramidRequest
from cubicweb.schema_exporters import JSONSchemaExporter
from pyramid.config import Configurator
from pyramid.request import Request

from cubicweb_api.api_transaction import ApiTransactionsRepository


class Context:
    def __init__(self, request: Request):
        self.request = request
        self.cwreq: CubicWebPyramidRequest = request.cw_request
        self.repo = self.cwreq.cnx.repo

    def render(self):
        raise NotImplementedError


class SchemaContext(Context):
    def render(self):
        schema = self.cwreq.cnx.repo.schema
        exporter = JSONSchemaExporter()
        return exporter.export_as_dict(schema)


class RQLContext(Context):
    def render(self):
        query = self.request.json["query"]
        params = self.request.json["params"]
        if not query:
            return {"error": "No query provided."}
        rset = self.cwreq.execute(query, params)
        return rset.rows


class TransactionContext(Context):
    def __init__(self, request):
        super().__init__(request)
        self._transactions: ApiTransactionsRepository = self.repo.api_transactions

    def render(self):
        action = self.request.json["action"]
        if action == "begin":
            return self._begin()
        elif action == "execute":
            return self._execute()
        elif action == "commit":
            return self._commit()
        elif action == "rollback":
            return self._rollback()

    def _begin(self):
        user = self.cwreq.user
        return self._transactions.begin_transaction(user)

    def _execute(self):
        uuid = self.request.json["uuid"]
        rql = self.request.json["query"]
        params = self.request.json["params"]
        rset = self._transactions[uuid].execute(rql, params)
        return rset.rows

    def _commit(self):
        uuid = self.request.json["uuid"]
        commit_result = self._transactions[uuid].commit()
        self._transactions[uuid].rollback()
        return commit_result

    def _rollback(self):
        uuid = self.request.json["uuid"]
        rollback_result = self._transactions[uuid].rollback()
        self._transactions.end_transaction(uuid)
        return rollback_result


class HelpContext(Context):
    def render(self):
        """TO IMPLEMENT"""
        pass


ROUTE_NAME_TO_CONTEXT = {
    "schema": SchemaContext,
    "transaction": TransactionContext,
    "rql": RQLContext,
    "help": HelpContext,
}


def get_route_name(route_part: str):
    return f"v1_{route_part}"


def get_route_pattern(route_part: str):
    return rf"/api/v1/{route_part}"


def includeme(config: Configurator):
    repo = config.registry["cubicweb.repository"]
    repo.api_transactions = ApiTransactionsRepository(repo)
    for route_part, context in ROUTE_NAME_TO_CONTEXT.items():
        config.add_route(
            get_route_name(route_part), get_route_pattern(route_part), factory=context
        )
