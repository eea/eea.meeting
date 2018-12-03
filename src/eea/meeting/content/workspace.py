from AccessControl import Unauthorized
from eea.meeting.interfaces import IMeetingWorkspace
from plone import api
from plone.dexterity.content import Container
from zope.globalrequest import getRequest
from zope.interface import implementer


@implementer(IMeetingWorkspace)
class MeetingWorkspace(Container):
    """ EEA Meeting Workspace content type"""

    def block_access(self, workspace):
        raise Unauthorized(workspace)

    def can_edit(self, meeting):
        return api.user.has_permission(
            'Modify portal content',
            obj=meeting
        )

    # TODO WIP
    # def current_user_has_access(self):
    #     """ Used in at_download.py override to fix file access.
    #     """
    #     meeting = self.aq_parent
    #
    #     subscribers = meeting.get_subscribers()
    #
    #     approved_subscribers_ids = [
    #         subscriber.userid for subscriber in subscribers
    #         if subscriber.state() == "approved"
    #     ]
    #
    #     is_anonymous = api.user.is_anonymous()
    #     if not is_anonymous:
    #         current_user = api.user.get_current()
    #         return current_user in approved_subscribers_ids
    #     else:
    #         return False

    @property
    def __ac_local_roles__(self):
        """ Manage custom roles for specific cases
            This container and its child items should be accessed only by
            meeting members (subscribers)
        """
        # This code runs for this container and also for all its child items
        request = getRequest()
        workspaces = [
            x for x in request.PARENTS[:-1]
            if x.portal_type == 'eea.meeting.workspace'
            ]
        if len(workspaces) > 0:
            workspace = workspaces[0]
        else:
            return {}

        meeting = workspace.aq_parent

        subscribers = meeting.get_subscribers()

        approved_subscribers_ids = [
            subscriber.userid for subscriber in subscribers
            if subscriber.state() == "approved"
        ]

        is_anonymous = api.user.is_anonymous()
        if not is_anonymous:
            current_user = api.user.get_current()

            if (current_user.id in approved_subscribers_ids) or self.can_edit(
                    meeting):
                pass  # Use default behavior: public items are public etc.
            else:
                self.block_access(workspace)
        else:
            self.block_access(workspace)
        return {}
