# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface

from eea.meeting import _
from eea.meeting.interfaces.util import validate_email
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form.browser.radio import RadioFieldWidget
from plone.autoform import directives


# [TODO] Move in portal_vocabularies to be editable for East and South
roles = SimpleVocabulary(
    [SimpleTerm(
        value=u'eni-seis-ii-south-nfp',
        title=_(u'ENI-SEIS II South NFP')),
     SimpleTerm(
        value=u'medpol-nfp',
        title=_(u'MedPOL NFP')),
     SimpleTerm(
        value=u'h2020-nfp',
        title=_(u'H2020 NFP')),
     SimpleTerm(
        value=u'other',
        title=_(u'Other'))]
)


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

    role = schema.Choice(
        title=_(u"Role"),
        vocabulary=roles,
        required=True,
    )


class ISubscribers(Interface):
    """ Meeting subscribers """
