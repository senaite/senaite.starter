# How to extend custom fields on existing contents

This guide explains how you can extend custom fields to SENAITE content types such as Analyses, Samples, Clients, etc.


## Extending AT based content types

AT contents are based on [Products.Archetypes](https://github.com/plone/Products.Archetypes),
a framework to create content types within the context of SENAITE.


!!! important

    AT based contents are obsolete and refactored to the new [Dexterity](https://github.com/plone/plone.dexterity)
    framework. Therefore, AT based schema extensions must be sooner or later be migrated as soon as the content type
    is migrated to Dexterity.

Custom fields for AT based contents such as `Analysis`, `AnalysisRequest`, `Client`, etc. are registered as an [adapter](https://zopecomponent.readthedocs.io/en/latest/narr.html#adapters) for the content interface, e.g.
`IAnalysisRequest`, that provides `archetypes.schemaextender.interfaces.ISchemaExtender`:

``` xml title="configure.zcml"
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:plone="http://namespaces.plone.org/plone"
    xmlns:browser="http://namespaces.zope.org/browser">

  <!-- Sample Schema Extender (AT) -->
  <adapter
      factory=".sample.SampleSchemaExtender"
      name="sample-extender"
      provides="archetypes.schemaextender.interfaces.ISchemaExtender"/>

</configure>
```

- `factory`: Defines the factory class responsible to create the adapter
- `name`: The adapter name for the schema extender
- `provides`: The interface the adapter provides

!!! tip

    Please read the [adapter ZCML directive](https://zopecomponent.readthedocs.io/en/latest/zcml.html#adapter) for more details.

``` python title="sample.py"
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from bika.lims.interfaces import IAnalysisRequest
from Products.Archetypes.public import StringField
from Products.Archetypes.atapi import StringWidget
from Products.CMFCore.permissions import View
from zope.component import adapts
from zope.interface import implements

from senaite.starter import messageFactory as _
from senaite.starter.content import ExtStringField
from senaite.starter.interfaces import ISenaiteStarter
from senaite.starter.permissions import EditExtendedField


class ExtStringField(ExtensionField, StringField):
    """A general purpose extended string field
    """


class SampleSchemaExtender(object):
    """Extend Schema Fields for Samples
    """
    layer = ISenaiteStarter
    implements(
        ISchemaExtender,
        IBrowserLayerAwareExtender,
        IOrderableSchemaExtender)
    adapts(IAnalysisRequest)

    fields = [
        ExtStringField(
            "ProductionBatchNumber",
            mode="rw",
            read_permission=View,
            write_permission=EditExtendedField,
            widget=StringWidget(
                label=_("Production batch number"),
                visible={
                    "add": "edit",
                },
                description=_("The production batch number of this sample"),
                render_own_label=True,
                i18n_domain="senaite.starter",
            )),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, original):
        """Change the order of the extended fields
        """
        return original
```


## Extending DX based content types

DX contents are based on [plone.dexterity](https://github.com/plone/plone.dexterity),
a framework to create Python 3 compatible content types with the context of SENAITE.

!!! note

    Dexterity based contents are the new and preferred way to create future-proof SENAITE contents.


Custom fields for DX based contents such as `SamplePoint`, `SampleType`, `Profile`,
etc. in SENAITE version 2.6 are registered as a [behavior](https://github.com/plone/plone.behavior?tab=readme-ov-file#usage) for the content interface, e.g. `senaite.core.interfaces.ISampleType`:

``` xml title="configure.zcml"
  <plone:behavior
      for="senaite.core.interfaces.ISampleType" 
      name="sampletype-extender"
      title="Custom Sample Type Fields"
      description="Add custom fields to the Sample Type Schema"
      provides=".sampletype.ISampleTypeSchemaExtender"
      factory=".sampletype.SampleTypeSchemaExtender"
      />
```

!!! tip

    Please read the [ZCML Reference](https://github.com/plone/plone.behavior?tab=readme-ov-file#zcml-reference) for details how to use the `plone:behavior` directive.


``` python title="sampletype.py"
from datetime import timedelta

from AccessControl import ClassSecurityInfo
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFCore import permissions
from senaite.core.api import dtime
from senaite.core.interfaces import ISampleType
from senaite.core.schema import DurationField
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider

from senaite.starter import messageFactory as _


@provider(IFormFieldProvider)
class ISampleTypeSchemaExtender(model.Schema):
    """Extended schema fields
    """
    directives.order_after(process_time="retention_period")
    process_time = DurationField(
        title=_(u"Process Time"),
        description=_(u"The work time needed to process this type of sample"),
        required=False
    )


@implementer(ISampleTypeSchemaExtender)
@adapter(ISampleType)
class SampleTypeSchemaExtender(object):
    """Extends sample types with additional fields
    """
    security = ClassSecurityInfo()

    def __init__(self, context):
        self.context = context

    @security.protected(permissions.View)
    def get_process_time(self):
        accessor = self.context.accessor("process_time")
        raw_value = accessor(self.context)
        return dtime.timedelta_to_dict(raw_value)

    @security.protected(permissions.ModifyPortalContent)
    def set_process_time(self, value):
        mutator = self.context.mutator("process_time")
        mutator(self.context, dtime.to_timedelta(value, default=timedelta(0)))

    process_time = property(get_process_time, set_process_time)
```


!!! important

    In order to activate the custom fields, the Factory Type Information (FTI) of the adapted content needs to be updated.
    This can be done via the Zope Management Interface (ZMI), e.g. [http://localhost:8080/senaite/portal_types/SampleType/manage_propertiesForm](http://localhost:8080/senaite/portal_types/SampleType/manage_propertiesForm) or programmatically
    
    
Registering a specific setuphandler in the root of the package that is executed on installation:

``` xml title="configure.zcml"
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:five="http://namespaces.zope.org/five"
    xmlns:i18n="http://namespaces.zope.org/i18n"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup">

  <!-- [...] -->

  <!-- Setup handler -->
  <genericsetup:importStep
      name="senaite.starter.install"
      title="SENAITE.STARTER: Run Setuphandler"
      description="Install senaite.starter"
      handler="senaite.starter.setuphandlers.install"/>

</configure>
```


``` python title="setuphandlers.py"
from bika.lims import api

from senaite.starter import logger


BEHAVIORS = [
    ("SampleType", [
        "senaite.starter.content.sampletype.ISampleTypeSchemaExtender",
    ]),
]


def install(context):
    """Install handler
    """
    if context.readDataFile("senaite.starter.txt") is None:
        return
    logger.info("Install handler [BEGIN]")
    portal = context.getSite()  # noqa

    # Run Installers
    setup_behaviors(portal)

    logger.info("Install handler [DONE]")


def setup_behaviors(portal):
    """Assigns additional behaviors to existing content types
    """
    logger.info("*** Setup Behaviors ***")
    pt = api.get_tool("portal_types")
    for portal_type, behavior_ids in BEHAVIORS:
        fti = pt.get(portal_type)
        if not hasattr(fti, "behaviors"):
            # Skip, type is not registered yet probably (AT2DX migration)
            logger.warn("Behaviors is missing: {} [SKIP]".format(portal_type))
            continue
        fti_behaviors = fti.behaviors
        additional = filter(lambda b: b not in fti_behaviors, behavior_ids)
        if additional:
            fti_behaviors = list(fti_behaviors)
            fti_behaviors.extend(additional)
            fti.behaviors = tuple(fti_behaviors)
```


!!! important

    The import step is only executed once on the initial installation and can be only triggered again via the `portal_quickinstaller` tool in the Zope Management Interface (ZMI), e.g. [http://localhost:8080/senaite/portal_quickinstaller/manage_installProductsForm](http://localhost:8080/senaite/portal_quickinstaller/manage_installProductsForm)



## Further Information and References

Please check out the official documentation page or the code repository for any further information.

- [Archetypes Schemaextender](https://github.com/plone/archetypes.schemaextender/tree/master?tab=readme-ov-file#introduction)
- [Dexterity Behaviors](https://github.com/plone/plone.behavior?tab=readme-ov-file#plonebehavior)
- [SENAITE CORE GitHub Code Repository](https://github.com/senaite/senaite.core)
- [Ask questions on SENAITE Community Site](https://community.senaite.org)
- [SENAITE Core Contribution Guide](https://github.com/senaite/senaite.core/blob/2.x/CONTRIBUTING.md)
