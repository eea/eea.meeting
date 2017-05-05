# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface

from eea.meeting import _
from eea.meeting.interfaces.util import validate_email
from z3c.form.browser.radio import RadioFieldWidget
from plone.autoform import directives


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

    directives.widget(reimbursed=RadioFieldWidget)
    reimbursed = schema.Bool(
        title=_(u"Reimbursed participation"),
        required=True
    )

    directives.widget(visa=RadioFieldWidget)
    visa = schema.Bool(
        title=_(u"I need visa support letter"),
        required=True
    )

    role = schema.Choice(
        title=_(u"Role"),
        vocabulary="subscriber_roles",
        required=True,
    )

    role_other = schema.TextLine(
        title=_(u"Role (other)"),
        required=False,
    )


class ISubscribers(Interface):
    """ Meeting subscribers """
