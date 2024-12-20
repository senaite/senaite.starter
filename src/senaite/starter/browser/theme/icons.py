# -*- coding: utf-8 -*-

import os

from plone.resource.interfaces import IResourceDirectory
from senaite.core.browser.globals.interfaces import IIconProvider
from senaite.core.browser.globals.interfaces import ISenaiteTheme
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implementer
from zExceptions import NotFound

from senaite.starter import check_installed

ICON_BASE_URL = "++plone++senaite.starter.static/assets/icons"


@implementer(IIconProvider)
class IconProvider(object):
    adapts(ISenaiteTheme)

    def __init__(self, view, context):
        self.view = view
        self.context = context

    @check_installed({})
    def icons(self):
        icons = {}
        static_dir = getUtility(
            IResourceDirectory, name=u"++plone++senaite.starter.static")
        try:
            icon_dir = static_dir["assets"]["icons"]
        except NotFound:
            return icons
        for icon in icon_dir.listDirectory():
            name, ext = os.path.splitext(icon)
            icons[name] = "{}/{}".format(ICON_BASE_URL, icon)
            icons[icon] = "{}/{}".format(ICON_BASE_URL, icon)
        return icons
