from plone.restapi.serializer.dxcontent import SerializeToJson
from zope.component import adapter
from eea.meeting.interfaces import IMeeting
from zope.interface import Interface
from plone.restapi.interfaces import ISerializeToJson
from zope.interface import implementer
from AccessControl import getSecurityManager


@implementer(ISerializeToJson)
@adapter(IMeeting, Interface)
class SerializerToJsonMeeting(SerializeToJson):
    def __call__(self, version=None, include_items=True):

        result = super(SerializerToJsonMeeting, self).__call__(version, include_items)
        subscribers = self.context.get("subscribers")
        emails = self.context.get("emails")
        sm = getSecurityManager()
        if sm.checkPermission("EEA Meting: View subscribers", subscribers):
            result.update({"subscribers_link": True})
        else:
            result.update({"subscribers_link": False})

        if sm.checkPermission("EEA Meting: View Emails", emails):
            result.update({"emails_link": True})
        else:
            result.update({"emails_link": False})
        return result
