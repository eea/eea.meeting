""" Meeting """
# -*- coding: utf-8 -*-
import datetime
from eea.meeting import _
from eea.meeting.interfaces.util import validate_email
from plone.app.textfield import RichText
from zope import schema
from zope.interface import Interface
from zope.interface import invariant, Invalid
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


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


class IMeeting(Interface):
    """Meeting"""

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
            "Hide the content of Additional materials table for not " "registered users"
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
