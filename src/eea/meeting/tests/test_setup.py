# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest
from eea.meeting.testing import EEA_MEETING_INTEGRATION_TESTING  # noqa
from plone import api


class TestSetup(unittest.TestCase):
    """Test that eea.meeting is properly installed."""

    layer = EEA_MEETING_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if eea.meeting is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'eea.meeting'))

    def test_browserlayer(self):
        """Test that IMeetingLayer is registered."""
        from eea.meeting.interfaces import (
            IMeetingLayer)
        from plone.browserlayer import utils
        self.assertIn(IMeetingLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):
    """ Test Uninstall """

    layer = EEA_MEETING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['eea.meeting'])

    def test_product_uninstalled(self):
        """Test if eea.meeting is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'eea.meeting'))

    def test_browserlayer_removed(self):
        """Test that IMeetingLayer is removed."""
        from eea.meeting.interfaces import IMeetingLayer
        from plone.browserlayer import utils
        self.assertNotIn(IMeetingLayer, utils.registered_layers())
