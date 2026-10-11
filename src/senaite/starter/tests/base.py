# -*- coding: utf-8 -*-

import json

import transaction
import unittest2 as unittest
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import quickInstallProduct
from plone.app.testing import setRoles
from plone.testing import zope
from senaite.jsonapi.v1 import BASE_URL as JSONAPI_BASE_URL
from plone.testing.z2 import Browser


class SimpleTestLayer(PloneSandboxLayer):
    """Setup Test Layer
    """
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(SimpleTestLayer, self).setUpZope(app, configurationContext)

        import bika.lims
        import senaite.app.listing
        import senaite.app.spotlight
        import senaite.core
        import senaite.impress
        import plone.jsonapi.core
        import senaite.jsonapi
        import senaite.lims
        import senaite.starter

        # Load ZCML
        self.loadZCML(package=bika.lims)
        self.loadZCML(package=senaite.app.listing)
        self.loadZCML(package=senaite.app.spotlight)
        self.loadZCML(package=senaite.core)
        self.loadZCML(package=senaite.impress)
        self.loadZCML(package=plone.jsonapi.core)
        self.loadZCML(package=senaite.jsonapi)
        self.loadZCML(package=senaite.starter)

        # Install product and call its initialize() function
        zope.installProduct(app, "bika.lims")
        zope.installProduct(app, "senaite.app.listing")
        zope.installProduct(app, "senaite.app.spotlight")
        zope.installProduct(app, "senaite.core")
        zope.installProduct(app, "senaite.impress")
        zope.installProduct(app, "plone.jsonapi.core")
        # NOTE: senaite.jsonapi is not a Zope 2 product. It has no
        # five:registerPackage directive and no initialize(), so
        # installProduct would only print "Could not install product
        # senaite.jsonapi". Loading its ZCML above is all it needs.
        zope.installProduct(app, "senaite.starter")

    def setUpPloneSite(self, portal):
        super(SimpleTestLayer, self).setUpPloneSite(portal)

        # Apply profiles
        applyProfile(portal, "senaite.core:default")
        applyProfile(portal, "senaite.starter:default")

        quickInstallProduct(portal, "senaite.starter", reinstall=True)
        transaction.commit()


###
# Use for simple tests (w/o contents)
###
SIMPLE_FIXTURE = SimpleTestLayer()
SIMPLE_TESTING = FunctionalTesting(
    bases=(SIMPLE_FIXTURE, ),
    name="senaite.starter:SimpleTesting"
)


class SimpleTestCase(unittest.TestCase):
    layer = SIMPLE_TESTING

    def setUp(self):
        super(SimpleTestCase, self).setUp()

        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        self.api_url = "{}/@@API{}".format(self.portal_url, JSONAPI_BASE_URL)
        self.request["ACTUAL_URL"] = self.portal_url
        setRoles(self.portal, TEST_USER_ID, ["LabManager", "Manager"])

    def getBrowser(self,
                   username=TEST_USER_NAME,
                   password=TEST_USER_PASSWORD,
                   loggedIn=True):

        # Instantiate and return a testbrowser for convenience
        browser = Browser(self.portal)
        browser.addHeader("Accept-Language", "en-US")
        browser.handleErrors = False
        if loggedIn:
            browser.open(self.portal.absolute_url())
            browser.getControl("Login Name").value = username
            browser.getControl("Password").value = password
            browser.getControl("Log in").click()
            self.assertTrue("You are now logged in" in browser.contents)
        return browser

    def get_json(self, endpoint):
        browser = self.getBrowser()
        url = "{}/{}".format(self.api_url, endpoint)
        browser.open(url)
        contents = browser.contents
        return json.loads(contents)
