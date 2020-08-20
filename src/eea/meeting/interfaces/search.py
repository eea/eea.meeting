""" Search """
# -*- coding: utf-8 -*-

from eea.meeting import _
from zope import schema
from zope.interface import Interface


class ISearchUser(Interface):
    """ Search user """
    containing = schema.TextLine(
        title=_(u"Add users to E-mail CC"),
        required=True,
    )

    results = schema.Set(
        required=False,
        value_type=schema.Choice(
            vocabulary='eea.meeting.vocabularies.LDAPListingVocabulary')
    )
