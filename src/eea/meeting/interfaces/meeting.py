""" Meeting """
# -*- coding: utf-8 -*-
import datetime

from eea.meeting import _
from eea.meeting.interfaces.util import validate_email
from plone.app.textfield import RichText
from plone.restapi.behaviors import BLOCKS_SCHEMA, LAYOUT_SCHEMA, IBlocks
from plone.schema import JSONField
from zope import schema
from zope.interface import Interface, Invalid, invariant
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

meeting_layout_blocks = {
    "0083ce5d-0f0b-4197-b086-f7143b38134e": {
        "@type": "metadata",
        "data": {"id": "max_participants", "widget": "integer"},
    },
    "05d875fb-e0e4-40ad-8673-1016f91cc9cc": {
        "@type": "metadata",
        "data": {"id": "allow_register_start", "widget": "datetime"},
    },
    "23e29c90-bad8-4c0c-b8f5-8f99be559ef1": {
        "@type": "metadata",
        "data": {"id": "changeNote", "widget": "string"},
    },
    "3170fbe7-c4c4-47b9-9e07-3f6d8073e83e": {
        "@type": "metadata",
        "data": {"id": "meeting_type", "widget": "choices"},
    },
    "35ea13ae-2118-4d19-89c5-3da9dce09569": {
        "@type": "metadata",
        "data": {"id": "allow_anonymous_registration", "widget": "boolean"},
    },
    "36b1c193-ee8c-4c67-810f-f6e81060de41": {
        "@type": "metadata",
        "data": {"id": "description", "widget": "description"},
    },
    "3c2ff6cb-2246-484d-9144-24d849f36602": {
        "@type": "metadata",
        "data": {"id": "products", "widget": "array"},
    },
    "457ab628-dead-4eec-b67d-a7390aee3292": {
        "@type": "metadata",
        "data": {"id": "hosting_organisation", "widget": "string"},
    },
    "5207adea-1044-4424-a110-a5919950ef1a": {
        "@type": "metadata",
        "data": {"id": "start", "widget": "datetime"},
    },
    "54ba0d84-c3cf-4198-9e66-237fcc514868": {
        "@type": "metadata",
        "data": {"id": "datasets", "widget": "array"},
    },
    "5598d8d0-1dc1-4249-ba4b-648d711ec44d": {
        "@type": "slate",
        "value": [
            {
                "type": "p",
                "children": [
                    {
                        "text": (
                            "Lorem ipsum dolor sit amet, consectetur "
                            "adipiscing elit, sed do eiusmod tempor "
                            "incididunt ut labore et dolore magna "
                            "aliqua. Ut enim ad minim veniam, "
                            "quis nostrud exercitation ullamco "
                            "laboris nisi ut aliquip ex ea commodo "
                            "consequat. Duis aute irure dolor in "
                            "reprehenderit in voluptate velit esse "
                            "cillum dolore eu fugiat nulla pariatur. "
                            "Excepteur sint occaecat cupidatat non "
                            "proident, sunt in culpa qui officia "
                            "deserunt mollit anim id est laborum."
                        )
                    }
                ],
            }
        ],
        "plaintext": (
            "Lorem ipsum dolor sit amet, consectetur "
            "adipiscing elit, sed do eiusmod tempor "
            "incididunt ut labore et dolore magna "
            "aliqua. Ut enim ad minim veniam, "
            "quis nostrud exercitation ullamco "
            "laboris nisi ut aliquip ex ea commodo "
            "consequat. Duis aute irure dolor in "
            "reprehenderit in voluptate velit esse "
            "cillum dolore eu fugiat nulla pariatur. "
            "Excepteur sint occaecat cupidatat non "
            "proident, sunt in culpa qui officia "
            "deserunt mollit anim id est laborum."
        ),
    },
    "67fd4bce-914d-4519-bb38-bd676e48c557": {
        "@type": "metadata",
        "data": {"id": "text", "widget": "richtext"},
    },
    "6b4d6356-de00-4f5c-b3dc-9fb5cd747e15": {
        "@type": "metadata",
        "data": {"id": "location", "widget": "string"},
    },
    "82a395c1-0510-42f9-8ac3-75284c751483": {
        "@type": "metadata",
        "data": {"id": "meeting_level", "widget": "choices"},
    },
    "84c0a56a-4c61-4bcc-ae88-0f6793dd5077": {
        "@type": "metadata",
        "data": {"id": "end", "widget": "datetime"},
    },
    "8dbea2f9-91c8-49ce-8c62-635b2ec82c31": {
        "@type": "metadata",
        "data": {"id": "allow_register", "widget": "boolean"},
    },
    "9843eaf6-14c3-41ac-af48-f1e07298a8c7": {"@type": "title"},
    "9a936912-1f74-454b-a3e9-bc9952c586d7": {
        "@type": "metadata",
        "data": {"id": "restrict_content_access", "widget": "boolean"},
    },
    "a189761d-278a-4ac9-9a00-4cfbbc55d1c6": {
        "@type": "metadata",
        "data": {"id": "contact_email", "widget": "string"},
    },
    "a673464e-103a-4097-bbea-81e3bf8d02a5": {
        "@type": "metadata",
        "data": {"id": "image", "widget": "image"},
    },
    "b4e032a9-696d-4c47-a739-e29fd2d9fba4": {
        "@type": "metadata",
        "data": {"id": "auto_approve", "widget": "boolean"},
    },
    "c8bc56ba-8cb7-44a7-9bc1-da77b72b96f2": {
        "@type": "metadata",
        "data": {"id": "allow_register_end", "widget": "datetime"},
    },
    "dd0c2614-8da0-4790-b88a-16efdc13d28c": {
        "@type": "metadata",
        "data": {"id": "whole_day", "widget": "boolean"},
    },
    "dddbe438-5b76-4610-8011-b91768448c6f": {
        "@type": "metadata",
        "data": {"id": "contact_name", "widget": "string"},
    },
    "e2c5016d-7050-4c05-9cc1-c7dc3dfabcc3": {
        "@type": "metadata",
        "data": {"id": "image_caption", "widget": "string"},
    },
    "ed360000-eae1-42fc-87f2-25f65b33d057": {
        "@type": "metadata",
        "data": {"id": "allow_register_above_max", "widget": "boolean"},
    },
    "f1a224d9-6006-40cb-98e8-6dfb08e04046": {
        "@type": "metadata",
        "data": {"id": "open_end", "widget": "boolean"},
    },
}


meeting_layout_items = [
    "9843eaf6-14c3-41ac-af48-f1e07298a8c7",
    "36b1c193-ee8c-4c67-810f-f6e81060de41",
    "67fd4bce-914d-4519-bb38-bd676e48c557",
    "5598d8d0-1dc1-4249-ba4b-648d711ec44d",
    "3170fbe7-c4c4-47b9-9e07-3f6d8073e83e",
    "8dbea2f9-91c8-49ce-8c62-635b2ec82c31",
    "ed360000-eae1-42fc-87f2-25f65b33d057",
    "05d875fb-e0e4-40ad-8673-1016f91cc9cc",
    "c8bc56ba-8cb7-44a7-9bc1-da77b72b96f2",
    "9a936912-1f74-454b-a3e9-bc9952c586d7",
    "b4e032a9-696d-4c47-a739-e29fd2d9fba4",
    "0083ce5d-0f0b-4197-b086-f7143b38134e",
    "457ab628-dead-4eec-b67d-a7390aee3292",
    "dddbe438-5b76-4610-8011-b91768448c6f",
    "a189761d-278a-4ac9-9a00-4cfbbc55d1c6",
    "6b4d6356-de00-4f5c-b3dc-9fb5cd747e15",
    "35ea13ae-2118-4d19-89c5-3da9dce09569",
    "5207adea-1044-4424-a110-a5919950ef1a",
    "84c0a56a-4c61-4bcc-ae88-0f6793dd5077",
    "dd0c2614-8da0-4790-b88a-16efdc13d28c",
    "f1a224d9-6006-40cb-98e8-6dfb08e04046",
    "a673464e-103a-4097-bbea-81e3bf8d02a5",
    "e2c5016d-7050-4c05-9cc1-c7dc3dfabcc3",
    "54ba0d84-c3cf-4198-9e66-237fcc514868",
    "3c2ff6cb-2246-484d-9144-24d849f36602",
    "23e29c90-bad8-4c0c-b8f5-8f99be559ef1",
    "82a395c1-0510-42f9-8ac3-75284c751483",
]


meeting_types = SimpleVocabulary(
    [
        SimpleTerm(value="meeting", title=_("Meeting")),
        SimpleTerm(value="conference", title=_("Conference")),
        SimpleTerm(value="workshop", title=_("Workshop")),
        SimpleTerm(value="webinar", title=_("Webinar")),
    ]
)

meeting_levels = SimpleVocabulary(
    [
        SimpleTerm(value="national", title=_("National Level")),
        SimpleTerm(value="regional", title=_("Regional Level")),
        SimpleTerm(value="other", title=_("Other")),
    ]
)


class IMeeting(Interface, IBlocks):
    """Meeting"""

    blocks = JSONField(
        title=_("Blocks"),
        description=_("The JSON representation of the object blocks."),
        schema=BLOCKS_SCHEMA,
        default=meeting_layout_blocks,
        required=False,
    )

    blocks_layout = JSONField(
        title=_("Blocks Layout"),
        description=_("The JSON representation of the object blocks layout."),
        schema=LAYOUT_SCHEMA,
        default={"items": meeting_layout_items},
        required=False,
    )

    text = RichText(
        title=_("Body text"),
        required=True,
    )

    meeting_type = schema.Choice(
        title=_("Meeting type"),
        vocabulary=meeting_types,
        required=True,
    )

    meeting_level = schema.Choice(
        title=_("Meeting level"),
        vocabulary=meeting_levels,
        required=False,
    )

    allow_register = schema.Bool(
        title=_("Allow users to register to the meeting"),
        required=False,
        default=False,
    )

    allow_register_above_max = schema.Bool(
        title=_(
            "Continue to allow registration when maximum number of"
            " participants is reached"
        ),
        required=False,
        default=False,
    )

    allow_register_start = schema.Datetime(
        title=_("From"),
        description=_("Allow registration starting with this datetime."),
        required=False,
        min=datetime.datetime(2018, 1, 1),
        max=datetime.datetime(datetime.datetime.now().year + 10, 12, 31),
    )

    allow_register_end = schema.Datetime(
        title=_("To"),
        description=_("Allow registration until this datetime."),
        required=False,
        min=datetime.datetime(2018, 1, 1),
        max=datetime.datetime(datetime.datetime.now().year + 10, 12, 31),
    )

    restrict_content_access = schema.Bool(
        title=_(
            "Hide the content of Additional materials table for not "
            "registered users"
        ),
        required=False,
        default=False,
    )

    auto_approve = schema.Bool(
        title=_("Automatically approve registrations"),
        required=False,
        default=False,
    )

    max_participants = schema.Int(
        title=_("Maximum number of participants"),
        required=False,
        default=0,
    )

    hosting_organisation = schema.TextLine(
        title=_("Hosting organisation"),
        required=True,
        default=None,
    )

    contact_name = schema.TextLine(
        title=_("Contact person"),
        required=True,
    )

    contact_email = schema.TextLine(
        title=_("Contact email"), required=True, constraint=validate_email
    )

    location = schema.TextLine(
        title=_("label_event_location", default="Event location"),
        description=_("help_event_location", default="Location of the event."),
        required=True,
        default="",
    )

    allow_anonymous_registration = schema.Bool(
        title=_(
            "allow_anonymous_registration",
            default="Allow registration for non-logged users",
        ),
        default=False,
    )

    # @invariant
    # def validate_location_required(data):
    #     """validate location required"""
    #     if data.meeting_type != "webinar" and data.location is None:
    #         raise Invalid(
    #             _(
    #                 u"Event location input is missing."
    #                 + " This field is not required only in "
    #                 + "'Meeting type: webinar' case."
    #             )
    #         )
