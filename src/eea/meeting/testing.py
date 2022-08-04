""" Testing """
# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import eea.meeting


class MeetingLayer(PloneSandboxLayer):
    """Meeting Layer"""

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Setup"""
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=eea.meeting)

    def setUpPloneSite(self, portal):
        """Setup site"""
        applyProfile(portal, "eea.meeting:default")


MEETING_FIXTURE = MeetingLayer()


MEETING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEETING_FIXTURE,), name="MeetingLayer:IntegrationTesting"
)


MEETING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MEETING_FIXTURE,), name="MeetingLayer:FunctionalTesting"
)


MEETING_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(MEETING_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="MeetingLayer:AcceptanceTesting",
)
