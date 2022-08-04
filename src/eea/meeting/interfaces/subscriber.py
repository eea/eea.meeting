""" Subscriber """
# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface

from eea.meeting import _
from eea.meeting.interfaces.util import validate_email
from eea.meeting.interfaces.util import validate_userid
from z3c.form.browser.radio import RadioFieldWidget
from plone.autoform import directives


class ISubscriber(Interface):
    """Meeting subscriber"""

    userid = schema.TextLine(
        title=_("User id"),
        required=True,
        constraint=validate_userid,
    )

    email = schema.TextLine(title=_("Email"), required=True, constraint=validate_email)

    directives.widget(reimbursed=RadioFieldWidget)
    reimbursed = schema.Bool(title=_("Reimbursed participation"), required=True)

    directives.widget(visa=RadioFieldWidget)
    visa = schema.Bool(title=_("I need visa support letter"), required=True)

    role = schema.Choice(
        title=_("Role"),
        vocabulary="eea.meeting.SubscriberRolesVocabulary",
        required=True,
    )

    role_other = schema.TextLine(
        title=_("Role (other)"),
        required=False,
    )

    request_data_deletion = schema.Bool(
        title=_("Request data deletion"),
        description=_(
            "Please delete my personal information after the event "
            "has ended, at latest 4 weeks after."
        ),
    )

    anonymous_extra_data = schema.Text(
        title=_("anonymous_extra_data"),
        description=_("json for anonymous registration Volto form"),
        required=False,
    )


class ISubscribers(Interface):
    """Meeting subscribers"""
