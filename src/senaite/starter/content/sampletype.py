# -*- coding: utf-8 -*-

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
