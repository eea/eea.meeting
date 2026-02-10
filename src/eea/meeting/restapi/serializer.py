"""REST API serializers."""
from AccessControl import getSecurityManager
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.dxcontent import SerializeFolderToJson
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer

from eea.meeting.interfaces import IMeeting


@implementer(ISerializeToJson)
@adapter(IMeeting, Interface)
class SerializerToJsonMeeting(SerializeFolderToJson):
    """Serialize meeting objects to JSON."""

    def _extract_field_custom_ids(self, obj):
        field_custom_ids = []
        blocks = getattr(obj, "blocks", None)
        if not blocks:
            return field_custom_ids

        for block_id in obj.blocks_layout["items"]:
            block = blocks.get(block_id)
            if not block or block.get("@type") != "form":
                continue
            subblocks = block.get("subblocks")
            if not subblocks:
                continue
            for field in subblocks:
                field_custom_id = field.get("field_custom_id")
                if field_custom_id:
                    field_custom_ids.append(field_custom_id)
        return field_custom_ids

    def _get_anonymous_form(self, review_state, published):
        anonymousforms_list = self.context.getFolderContents(
            {
                "portal_type": "AnonymousForm",
                "review_state": review_state,
            }
        )
        if not anonymousforms_list:
            return None

        obj = anonymousforms_list[0].getObject()
        field_custom_ids = self._extract_field_custom_ids(obj)
        return {
            "url": anonymousforms_list[0].getURL(),
            "email": "email" in field_custom_ids,
            "fullname": "fullname" in field_custom_ids,
            "published": published,
        }

    def __call__(self, version=None, include_items=True):
        result = super(SerializerToJsonMeeting, self).__call__(
            version,
            include_items,
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
            form_info = self._get_anonymous_form("published", True)
            if not form_info:
                form_info = self._get_anonymous_form("private", False)
            if form_info:
                result["anonymous_registration_form"] = form_info

        result["registrations_open"] = self.context.registrations_open()
        result["is_registered"] = self.context.is_registered()
        result["can_register"] = self.context.can_register()
        result["is_folderish"] = True

        return result
