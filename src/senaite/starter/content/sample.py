# -*- coding: utf-8 -*-

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.interfaces import IAnalysisRequest
from Products.Archetypes.atapi import StringWidget
from Products.CMFCore.permissions import View
from zope.component import adapts
from zope.interface import implements

from senaite.starter import messageFactory as _
from senaite.starter.content import ExtStringField
from senaite.starter.interfaces import ISenaiteStarter
from senaite.starter.permissions import EditExtendedField


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
        # get the fields of the default schemata
        default = original["default"]

        # move  Order Number before Batch
        index = default.index("Batch")
        # remove any existing field
        default.remove("ProductionBatchNumber")
        # add the field below the reference index
        default.insert(index - 1, "ProductionBatchNumber")

        return original


class SampleSchemaModifier(object):
    """Modify Sample Schema Fields
    """
    layer = ISenaiteStarter
    implements(
        ISchemaModifier,
        IBrowserLayerAwareExtender)
    adapts(IAnalysisRequest)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        # Make the profiles field required
        # profiles = schema.get("Profiles")
        # profiles.required = True

        return schema
