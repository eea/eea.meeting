from eea.meeting.interfaces import ISubscriber, ISubscribers, IEmail, IEmails
from plone.restapi.serializer.dxcontent import SerializeToJson
from zope.component import adapter
from zope.interface import Interface
from plone.restapi.interfaces import ISerializeToJson
from zope.interface import implementer
from AccessControl import getSecurityManager

# -*- coding: utf-8 -*-
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from zope.component import queryMultiAdapter


class ContentGetSubscribers(Service):
    """Returns a serialized content object."""

    def reply(self):
        sm = getSecurityManager()
        if sm.checkPermission("EEA Meting: View subscribers", self.context):
            serializer = queryMultiAdapter(
                (self.context, self.request), ISerializeToJson
            )

            if serializer is None:
                self.request.response.setStatus(501)
                return dict(error=dict(message="No serializer available."))

            return serializer(version=self.request.get("version"))
        else:
            self.request.response.setStatus(401)
            return dict(
                error=dict(
                    type="Unathorized",
                    message="You are not allowed to see this content",
                )
            )


class ContentGetEmails(Service):
    """Returns a serialized content object."""

    def reply(self):
        sm = getSecurityManager()
        if sm.checkPermission("EEA Meting: View Emails", self.context):
            serializer = queryMultiAdapter(
                (self.context, self.request), ISerializeToJson
            )

            if serializer is None:
                self.request.response.setStatus(501)
                return dict(error=dict(message="No serializer available."))

            return serializer(version=self.request.get("version"))
        else:
            self.request.response.setStatus(401)
            return dict(
                error=dict(
                    type="Unathorized",
                    message="You are not allowed to see this content",
                )
            )
