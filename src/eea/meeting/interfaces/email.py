# -*- coding: utf-8 -*-

from eea.meeting import _
from plone.autoform import directives
from plone.schema import Email
from z3c.form.browser.text import TextFieldWidget
from zope import schema
from zope.interface import Interface
from eea.meeting.interfaces.util import cc_constraint


class IEmails(Interface):
    """ Meeting emails """


class IEmail(Interface):
    """ Email """
    sender = Email(
        title=_(u"From"),
        required=True,
    )

    receiver = schema.Set(
        title=u'Recipients',
        missing_value=set(),
        value_type=schema.Choice(
            vocabulary='eea.meeting.vocabularies.RecipientsVocabulary',
            required=True,
        ),
        required=True,
    )

    cc = schema.List(
        title=_(u"CC"),
        description=_(u'Add CC addresses one per line, no separator'),
        value_type=schema.TextLine(),
        constraint=cc_constraint,
        required=False,
    )

    subject = schema.TextLine(
        title=_(u"Subject"),
        required=True,
    )

    body = schema.Text(
        title=_(u"Body"),
        required=True,
    )

    directives.widget(
        'sender',
        TextFieldWidget,
        klass=u'mail_widget'
    )
