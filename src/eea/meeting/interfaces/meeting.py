# -*- coding: utf-8 -*-

from eea.meeting import _
from plone.app.textfield import RichText
from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from eea.meeting.interfaces.util import validate_email


meeting_types = SimpleVocabulary(
    [SimpleTerm(value=u'meeting', title=_(u'Meeting')),
     SimpleTerm(value=u'conference', title=_(u'Conference')),
     SimpleTerm(value=u'workshop', title=_(u'Workshop'))]
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

    restrict_content_access = schema.Bool(
        title=_(u"Restrict user access to the contents in the meeting"),
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
        required=True,
        default=None
    )
