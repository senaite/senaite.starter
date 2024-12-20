# How to create custom SENAITE JSON API endpoints

This guide explains how you can extend the [SENAITE JSON API](https://github.com/senaite/senaite.jsonapi)
with your own logic and endpoints to interface external applications with SENAITE.


## Package overview

The `senaite.starter.jsonapi` package contains the following contents:

``` shell
senaite.starter.jsonapi
├── README.md
├── __init__.py
├── configure.zcml
└── version.py
```


## Version Route

The custom version route returns the `version`, `date`, `license` and
`copyright` of your custom JSON API:

``` python
>>> response = self.get_json("senaite.starter/version")
>>> response.get("version")
u'1.0.0'

```


## Registering a new API endpoint

Endpoints can be implemented as functions that take the parameters `context` and
`request` and are decorated with the `@add_route` decorator.

!!! info

    You need to import your new route to hook your custom endpoint into the
    SENAITE JSON API! Please check the `__init__.py` module on how this was done
    for the `version` route.


### Custom JSON API route to fetch all samples belonging to a Client

In the following example, we want to return all samples that belong to a specific client
that is identified by its `Client ID`, e.g. `HH` for the client `Happy Hills` or
the Object ID, e.g. `client-1` or the UID, e.g.  `19724892738723897489127428`.

``` python
from bika.lims import api
from senaite.core.catalog import CLIENT_CATALOG
from senaite.core.catalog import SAMPLE_CATALOG
from senaite.jsonapi import request as req
from senaite.jsonapi.api import fail
from senaite.jsonapi.api import get_batch
from senaite.jsonapi.api import url_for
from senaite.jsonapi.v1 import add_route

URL_KEY = "senaite.starter.jsonapi.client_samples"


@add_route("/senaite.starter/client/<string:id>/samples", URL_KEY, methods=["GET"])
def client_samples(context, request):
    """Returns all Samples belonging to a Client

    :param context: The portal object
    :param request: The current request
    :param id: Object ID, UID or ClientID
    :returns: items containing the Samples of the Client
    """

    client = get_client(id)

    if client is None:
        fail(404, "No Client found for '%s'" % id)

    items = search_client_samples(client)

    # fetch the batch params from the request
    size = req.get_batch_size()
    start = req.get_batch_start()
    complete = req.get_complete()

    return {
        "count": len(items),
        "items": get_batch(items, size, start, complete=complete),
        "url": url_for(URL_KEY, id=id),
    }


def get_client(id, default=None):
    """Fetch Client by ID

    :param id: ID/UID or ClientID
    :param default: default value to return when no Client was found
    :returns: Client object
    """
    if api.is_uid(id):
        return api.get_object(id, default=None)

    # Try to fetch the Client by ID
    results = search_clients(getId=id)
    if len(results) == 1:
        return api.get_object(results[0])

    # Try to fetch the Client by Client ID
    results = search_clients(getClientID=id)
    if len(results) == 1:
        return api.get_object(results[0])

    # Nothing found, return the default value
    return default


def search_clients(**kw):
    """Search for Clients
    """
    query = {
        "portal_type": "Client",
        "is_active": True,
    }
    query.update(kw)
    return api.search(query, catalog=CLIENT_CATALOG)


def search_client_samples(client, **kw):
    """Return all Samples of the given Client

    :param client: Client object
    :returns: catalog brains
    """
    client = api.get_object(client)

    query = {
        "portal_type": "AnalysisRequest",
        "getClientUID": api.get_uid(client),
        "sort_on": "created",
        "sort_order": "descending",
    }
    query.update(kw)
    return api.search(query, SAMPLE_CATALOG)

```

## Further Information and References

Please check out the official documentation page or the code repository for any further information.


- [SENAITE JSON API Online Documentation](https://senaitejsonapi.readthedocs.io/en/latest)
- [SENAITE JSON API GitHub Code Repository](https://github.com/senaite/senaite.jsonapi)
- [Ask questions on SENAITE Community Site](https://community.senaite.org)
- [SENAITE Core Contribution Guide](https://github.com/senaite/senaite.core/blob/2.x/CONTRIBUTING.md)
