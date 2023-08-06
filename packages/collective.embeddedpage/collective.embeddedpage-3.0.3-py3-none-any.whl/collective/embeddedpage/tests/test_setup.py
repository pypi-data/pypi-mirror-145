"""Setup tests for this package."""
from collective.embeddedpage.testing import EMBEDDEDPAGE_INTEGRATION_TESTING
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.embeddedpage is properly installed."""

    layer = EMBEDDEDPAGE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.embeddedpage is installed."""
        self.assertTrue(self.installer.is_product_installed("collective.embeddedpage"))

    def test_browserlayer(self):
        """Test that ICollectiveEmbeddedpageLayer is registered."""
        from collective.embeddedpage.interfaces import ICollectiveEmbeddedpageLayer
        from plone.browserlayer import utils

        self.assertIn(ICollectiveEmbeddedpageLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = EMBEDDEDPAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        self.installer.uninstall_product("collective.embeddedpage")

    def test_product_uninstalled(self):
        """Test if collective.embeddedpage is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("collective.embeddedpage"))

    def test_browserlayer_removed(self):
        """Test that ICollectiveEmbeddedpageLayer is removed."""
        from collective.embeddedpage.interfaces import ICollectiveEmbeddedpageLayer
        from plone.browserlayer import utils

        self.assertNotIn(ICollectiveEmbeddedpageLayer, utils.registered_layers())
