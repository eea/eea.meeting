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
        result = super(SerializerToJsonMeeting, self).__call__(
            version, include_items
        )
        subscribers = self.context.get("subscribers")
        emails = self.context.get("emails")
        sm = getSecurityManager()
        if sm.checkPermission("EEA Meting: View subscribers", subscribers):
            result.update({"subscribers_link": subscribers.absolute_url()})
        else:
            result.update({"subscribers_link": None})

        if sm.checkPermission("EEA Meting: View Emails", emails):
            result.update({"emails_link": emails.absolute_url()})
        else:
            result.update({"emails_link": None})

        if result["allow_anonymous_registration"]:
            anonymousforms_list = self.context.getFolderContents(
                {"portal_type": "AnonymousForm", "review_state": "published"}
            )
            if anonymousforms_list:
                result["anonymous_registration_form"] = {
                    "url": anonymousforms_list[0].getURL(),
                    "published": True,
                }
            else:
                anonymousforms_list = self.context.getFolderContents(
                    {"portal_type": "AnonymousForm", "review_state": "private"}
                )
                if anonymousforms_list:
                    result["anonymous_registration_form"] = {
                        "url": anonymousforms_list[0].getURL(),
                        "published": False,
                    }

        result["registrations_open"] = False
        if self.context.registrations_open():
            result["registrations_open"] = True

        result["is_registered"] = self.context.is_registered()
        result["is_folderish"] = True
        return result
