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
        """
        # This code runs for this container and also for all its child items
        request = getRequest()
        workspaces = [
            x for x in request.PARENTS[:-1]
            if x.portal_type == 'eea.meeting.workspace'
            ]
        if len(workspaces) > 0:
            workspace = workspaces[0]
            has_access = workspace.restrictedTraverse(
                "current_user_has_access")()
            if has_access != "has_access":
                self.block_access(workspace)
            else:
                return {}
        else:
            return {}
