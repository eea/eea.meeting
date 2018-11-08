# -*- coding: utf-8 -*-

from eea.meeting import _
from eea.meeting.interfaces.util import validate_email
from plone.app.textfield import RichText
from zope import schema
from zope.interface import Interface
from zope.interface import invariant, Invalid
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


meeting_types = SimpleVocabulary(
    [SimpleTerm(value=u'meeting', title=_(u'Meeting')),
     SimpleTerm(value=u'conference', title=_(u'Conference')),
     SimpleTerm(value=u'workshop', title=_(u'Workshop')),
     SimpleTerm(value=u'webminar', title=_(u'Webminar'))]
)

meeting_levels = SimpleVocabulary(
    [SimpleTerm(value=u'national', title=_(u'National Level')),
     SimpleTerm(value=u'regional', title=_(u'Regional Level')),
     SimpleTerm(value=u'other', title=_(u'Other'))]
)


class IMeeting(Interface):
    """ Meeting """
    text = RichText(
        title=_(u"Body text"),
        required=True,
    )

    meeting_type = schema.Choice(
        title=_(u"Meeting type"),
        vocabulary=meeting_types,
        required=True,
    )

    meeting_level = schema.Choice(
        title=_(u"Meeting level"),
        vocabulary=meeting_levels,
        required=True,
    )

    allow_register = schema.Bool(
        title=_(u"Allow users to register to the meeting"),
        required=True,
    )

    allow_register_start = schema.Datetime(
        title=_(u"From"),
        description=_(u"Allow registration starting with this datetime."),
        required=False,
    )

    allow_register_end = schema.Datetime(
        title=_(u"To"),
        description=_(u"Allow registration until this datetime."),
        required=False,
    )

    restrict_content_access = schema.Bool(
        title=_(u"Hide meeting content list for not registered users"),
        required=True
    )

    auto_approve = schema.Bool(
        title=_(u"Automatically approve registrations"),
        required=True,
    )

    max_participants = schema.Int(
        title=_(u"Maximum number of participants"),
        required=True,
    )

    hosting_organisation = schema.TextLine(
        title=_(u"Hosting organisation"),
        required=True,
        default=None,
    )

    contact_name = schema.TextLine(
        title=_(u"Contact person"),
        required=True,
    )

    contact_email = schema.TextLine(
        title=_(u"Contact email"),
        required=True,
        constraint=validate_email
    )

    location = schema.TextLine(
        title=_(
            u'label_event_location',
            default=u'Event location'
        ),
        description=_(
            u'help_event_location',
            default=u'Location of the event.'
        ),
        required=False,
        default=None
    )

    @invariant
    def validate_location_required(data):
        if data.meeting_type != 'webminar' and data.location is None:
            raise Invalid(_(
                u"Event location input is missing." +
                " This field is not required only in " +
                "'Meeting type: webminar' case."))
