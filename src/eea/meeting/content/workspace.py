""" Workspace """
from Products.statusmessages.interfaces import IStatusMessage
from eea.meeting.interfaces import IMeetingWorkspace
from plone import api
from plone.dexterity.content import Container
from zope.globalrequest import getRequest
from zope.interface import implementer


@implementer(IMeetingWorkspace)
class MeetingWorkspace(Container):
    """EEA Meeting Workspace content type"""

    def block_access(self, workspace):
        """Block access and redirect"""
        messages = IStatusMessage(workspace.REQUEST)
        messages.add(
            "The content you tried to access is available only for \
            approved participants. Please log in.",
            type="info",
        )
        return workspace.REQUEST.response.redirect(workspace.aq_parent.absolute_url())

    def can_edit(self, meeting):
        """Check permission"""
        return api.user.has_permission("Modify portal content", obj=meeting)

    @property
    def __ac_local_roles__(self):
        """Manage custom roles for specific cases
        This container and its child items should be accessed only by
        meeting members (subscribers)
        """
        # This code runs for this container and also for all its child items
        request = getRequest()
        workspaces = [
            x for x in request.PARENTS[:-1] if x.portal_type == "eea.meeting.workspace"
        ]
        if workspaces:
            workspace = workspaces[0]
            has_access = workspace.restrictedTraverse("current_user_has_access")()
            if has_access != "has_access":
                self.block_access(workspace)
            else:
                return {}
        else:
            return {}
