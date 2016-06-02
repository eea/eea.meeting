# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import eea.meeting


class EEAMeetingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=eea.meeting)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'eea.meeting:default')


EEA_MEETING_FIXTURE = EEAMeetingLayer()


EEA_MEETING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EEA_MEETING_FIXTURE,),
    name='EEAMeetingLayer:IntegrationTesting'
)


EEA_MEETING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EEA_MEETING_FIXTURE,),
    name='EEAMeetingLayer:FunctionalTesting'
)


EEA_MEETING_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EEA_MEETING_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='EEAMeetingLayer:AcceptanceTesting'
)
