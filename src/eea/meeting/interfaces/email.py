""" Email """
# -*- coding: utf-8 -*-

from eea.meeting import _
from eea.meeting.interfaces.util import cc_constraint
from plone.autoform import directives
from plone.schema import Email
from z3c.form.browser.text import TextFieldWidget
from zope import schema
from zope.interface import Interface


class IEmails(Interface):
    """Meeting emails"""


class IEmail(Interface):
    """Email"""

    sender = Email(
        title=_("From"),
        required=True,
    )

    receiver = schema.Set(
        title="Recipients",
        missing_value=set(),
        value_type=schema.Choice(
            vocabulary="eea.meeting.vocabularies.RecipientsVocabulary",
            required=True,
        ),
        required=True,
    )

    cc = schema.List(
        title=_("CC"),
        description=_("Add CC addresses one per line, no separator"),
        value_type=schema.TextLine(),
        constraint=cc_constraint,
        required=False,
    )

    subject = schema.TextLine(
        title=_("Subject"),
        required=True,
    )

    body = schema.Text(
        title=_("Body"),
        required=True,
    )

    email_type = schema.TextLine(
        title=_("Email type"),
        required=False,
    )

    directives.widget("sender", TextFieldWidget, klass="mail_widget")
