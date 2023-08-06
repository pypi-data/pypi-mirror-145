from collective.embeddedpage.interfaces import IEmbeddedPage
from collective.embeddedpage.testing import EMBEDDEDPAGE_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.utils import get_installer
from zope.component import createObject
from zope.component import queryUtility

import unittest


class EmbeddedPageIntegrationTest(unittest.TestCase):

    layer = EMBEDDEDPAGE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name="EmbeddedPage")
        schema = fti.lookupSchema()
        self.assertEqual(IEmbeddedPage, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name="EmbeddedPage")
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name="EmbeddedPage")
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IEmbeddedPage.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory("EmbeddedPage", "EmbeddedPage")
        self.assertTrue(IEmbeddedPage.providedBy(self.portal["EmbeddedPage"]))
