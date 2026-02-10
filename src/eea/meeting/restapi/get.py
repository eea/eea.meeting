"""REST API GET services."""
from AccessControl import getSecurityManager
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from zope.component import queryMultiAdapter


class ContentGetSubscribers(Service):
    """Returns a serialized subscribers container."""

    def reply(self):
        """Return serialized subscribers or an error response."""
        sm = getSecurityManager()
        if sm.checkPermission("EEA Meting: View subscribers", self.context):
            serializer = queryMultiAdapter(
                (self.context, self.request), ISerializeToJson
            )

            if serializer is None:
                self.request.response.setStatus(501)
                return dict(error=dict(message="No serializer available."))

            return serializer(version=self.request.get("version"))
        self.request.response.setStatus(401)
        return dict(
            error=dict(
                type="Unathorized",
                message="You are not allowed to see this content",
            )
        )


class ContentGetEmails(Service):
    """Returns a serialized emails container."""

    def reply(self):
        """Return serialized emails or an error response."""
        sm = getSecurityManager()
        if sm.checkPermission("EEA Meting: View Emails", self.context):
            serializer = queryMultiAdapter(
                (self.context, self.request), ISerializeToJson
            )

            if serializer is None:
                self.request.response.setStatus(501)
                return dict(error=dict(message="No serializer available."))

            return serializer(version=self.request.get("version"))
        self.request.response.setStatus(401)
        return dict(
            error=dict(
                type="Unathorized",
                message="You are not allowed to see this content",
            )
        )
