# -*- coding: utf-8 -*-

from senaite.jsonapi import url_for
from senaite.jsonapi.v1 import add_route

URL_KEY = "senaite.starter.jsonapi.version"


@add_route("/senaite.starter/version", URL_KEY, methods=["GET"])
def version(context, request):
    """Version endpoint at @@API/senaite/v1/senaite.starter/version
    """
    return {
        "url": url_for(URL_KEY),
        "version": "1.0.0",
        "date": "2024-12-20",
        "license": "GPLv2",
        "copyright": "2024, RIDING BYTES GmbH",
    }
