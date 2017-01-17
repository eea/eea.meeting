# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface

from eea.meeting import _
from eea.meeting.interfaces.util import validate_email


class ISubscriber(Interface):
    """ Meeting subscriber """
    userid = schema.TextLine(
        title=_("User id"),
        required=True
    )

    email = schema.TextLine(
        title=_(u"Email"),
        required=True,
        constraint=validate_email
    )


class ISubscribers(Interface):
    """ Meeting subscribers """
