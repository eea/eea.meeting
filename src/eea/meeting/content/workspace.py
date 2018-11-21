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

    @property
    def __ac_local_roles__(self):
        """ Manage custom roles for specific cases
            This container and its child items should be accessed only by
            meeting members (subscribers)

            TODO: The access to files is not blocked. Fix it.
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
                # is_workspace_member = True
                pass  # Use default behavior: public items are public etc.
            else:
                # is_workspace_member = False
                self.block_access(workspace)
        else:
            # Workspace is not for anonymous users.
            self.block_access(workspace)
        return {}
