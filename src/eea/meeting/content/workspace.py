from zope.interface import implementer
from plone.dexterity.content import Container
from eea.meeting.interfaces import IMeetingWorkspace


@implementer(IMeetingWorkspace)
class MeetingWorkspace(Container):
    """ EEA Meeting Workspace content type"""
