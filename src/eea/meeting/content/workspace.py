from zope.interface import implementer
from plone.dexterity.content import Container
from eea.meeting.interfaces import IMeetingWorkspace


@implementer(IMeetingWorkspace)
class MeetingWorkspace(Container):
    """ EEA Meeting Workspace content type"""
    # __ac_local_roles_block__ = True
    #
    # def get_meeting(self):
    #     return self.aq_parent
    #
    # @property
    # def __ac_local_roles__(self):
    #     import pdb; pdb.set_trace()
    #     return {}
