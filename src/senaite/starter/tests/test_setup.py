# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import get_installer
from senaite.impress.interfaces import ITemplateFinder
from zope.component import getUtility

from senaite.starter.tests.base import SimpleTestCase
from senaite.starter.interfaces import ISenaiteStarter


class TestSetup(SimpleTestCase):
    """Test Setup
    """

    def test_is_addon_installed(self):
        qi = get_installer(self.portal)
        self.assertTrue(qi.is_product_installed("senaite.starter"))

    def test_browser_layer_active(self):
        self.assertTrue(ISenaiteStarter.providedBy(self.request))

    def test_custom_report_templates(self):
        finder = getUtility(ITemplateFinder)
        record = {}
        for resource in finder.resources:
            if resource.get("name") == "senaite.starter":
                record = resource
        self.assertTrue(len(record.get("contents", [])) > 0)

    def test_jsonapi_registered(self):
        endpoint = "senaite.starter/version"
        response = self.get_json(endpoint)
        self.assertEquals(response.get("version"), "1.0.0")


def test_suite():
    from unittest import TestSuite
    from unittest import makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSetup))
    return suite
