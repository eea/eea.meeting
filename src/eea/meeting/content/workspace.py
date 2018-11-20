from eea.meeting.interfaces import IMeetingWorkspace
from plone import api
from plone.dexterity.content import Container
from zope.globalrequest import getRequest
from zope.interface import implementer


@implementer(IMeetingWorkspace)
class MeetingWorkspace(Container):
    """ EEA Meeting Workspace content type"""
    @property
    def __ac_local_roles__(self):
        """ Manage custom roles for specific cases
            This container and its child items should be accessed only by
            meeting members (subscribers)
        """
        # This code runs for this container and also for all its child items
        request = getRequest()
        workspace = [
            x for x in request.PARENTS[:-1]
            if x.portal_type == 'eea.meeting.workspace'
            ][0]
        meeting = workspace.aq_parent

        subscribers = meeting.get_subscribers()

        approved_subscribers_ids = [
            subscriber.userid for subscriber in subscribers
            if subscriber.state == "approved"
        ]
        import pdb; pdb.set_trace()
        return {}
