# -*- coding: utf-8 -*-

from bika.lims import api
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter
from senaite.app.listing.utils import add_column
from zope.component import adapter
from zope.interface import implementer
from bika.lims.utils import get_link


@implementer(IListingViewAdapter)
@adapter(IListingView)
class SampleListingViewAdapter(object):

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        # Add new column for all available states
        states = map(lambda r: r["id"], self.listing.review_states)
        add_column(
            listing=self.listing,
            column_id="APIURL",
            column_values={
                "title": "API URL",
                "sortable": False,
            },
            review_states=states)

    def folder_item(self, obj, item, index):
        obj = api.get_object(obj)
        uid = api.get_uid(obj)
        portal = api.get_portal()
        portal_url = api.get_url(portal)
        api_url = "{}/@@API/senaite/v1/{}".format(portal_url, uid)
        item["APIURL"] = get_link(api_url, value=api.get_id(obj))
        return item
