# How to extend listing tables with custom columns

This guide explains how you can extend listing tables with custom columns using the
[Zope Component Architecture](https://zopecomponent.readthedocs.io/en/latest/narr.html)


## Extending the Sample Listing View

Listing tables in SENAITE inherit from [senaite.app.listing.view.ListingView](https://github.com/senaite/senaite.app.listing/blob/2.x/src/senaite/app/listing/view.py) and allow modification by subscriber adapters.


To extend custom columns of a specific listing view in SENAITE, the extended view and the underlying context need to be adapted to `ILisitngViewAdapter`:

``` xml title="configure.zcml"
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser">

  <!-- Sample listing with additional columns -->
  <subscriber
    for="senaite.core.browser.samples.view.SamplesView
         bika.lims.interfaces.IAnalysisRequestsFolder"
    provides="senaite.app.listing.interfaces.IListingViewAdapter"
    factory=".sample_listing.SampleListingViewAdapter" />

</configure>
```

- `for`: Adapts the listing view (`samples` view) and the underlying context (`samples` folder)
- `provides`: The interface the adapter provides
- `factory`: Defines the factory class responsible to create the adapter

!!! tip

    Please read the [subscriber ZCML directive](https://zopecomponent.readthedocs.io/en/latest/zcml.html#subscriber) for more details.

The additional columns depending on the workflow state can be injected in the adapters' `before_render` method and populated in `folder_item`:


``` python title="sample_listing.py"
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

```

!!! note

    The methods `before_render` and `folder_item` are the only ones called by the listing view


!!! important

    Please restart your SENAITE instance in order for the changes to take effect


!!! tip

    Please press the "Reset Columns" button of the column configuration of the sample listing table if the column does not appear!


## Further Information and References

Please check out the official documentation page or the code repository for any further information.

- [Adapting Listings](https://github.com/senaite/senaite.app.listing?tab=readme-ov-file#adapting-listings)
- [SENAITE CORE GitHub Code Repository](https://github.com/senaite/senaite.core)
- [SENAITE APP LISTING GitHub Code Repository](https://github.com/senaite/senaite.app.listing)
- [Ask questions on SENAITE Community Site](https://community.senaite.org)
- [SENAITE Core Contribution Guide](https://github.com/senaite/senaite.core/blob/2.x/CONTRIBUTING.md)
