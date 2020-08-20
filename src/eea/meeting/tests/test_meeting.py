""" Test meeting """
# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

from eea.meeting.testing import MEETING_INTEGRATION_TESTING  # noqa
from eea.meeting.interfaces import IMeeting

import unittest2 as unittest


class MeetingIntegrationTest(unittest.TestCase):
    """ Test meeting """

    layer = MEETING_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        """ Test schema """
        fti = queryUtility(IDexterityFTI, name='EEA Meeting')
        schema = fti.lookupSchema()
        self.assertEqual(IMeeting, schema)

    def test_fti(self):
        """ Test FTI  """
        fti = queryUtility(IDexterityFTI, name='EEA Meeting')
        self.assertTrue(fti)

    def test_factory(self):
        """ Test factory """
        fti = queryUtility(IDexterityFTI, name='EEA Meeting')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IMeeting.providedBy(obj))

    def test_adding(self):
        """ Test adding """
        self.portal.invokeFactory('EEA Meeting', 'EEA Meeting')
        self.assertTrue(
            IMeeting.providedBy(self.portal['EEA Meeting'])
        )
