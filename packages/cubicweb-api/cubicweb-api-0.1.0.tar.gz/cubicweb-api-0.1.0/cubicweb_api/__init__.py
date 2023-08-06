"""cubicweb-api application package

This cube is the new api which will be integrated in CubicWeb 4.
"""
from datetime import datetime

from pyramid.config import Configurator
from pyramid.renderers import JSON


def datetime_adapter(obj, request):
    return obj.isoformat()


def includeme(config: Configurator):
    json_renderer = JSON()
    json_renderer.add_adapter(datetime, datetime_adapter)

    config.add_renderer("json", json_renderer)
    config.include(".routes")
    config.include(".pviews")
