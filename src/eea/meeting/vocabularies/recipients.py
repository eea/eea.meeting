""" Recipients vocabulary
"""

from zope.interface import implementer

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from eea.meeting.interfaces import IMeeting

import plone.api as api


@implementer(IVocabularyFactory)
class RecipientsVocabulary(object):

    def __call__(self, context):
        portal_catalog = api.portal.get_tool('portal_catalog')

        if IMeeting.providedBy(context.aq_parent):
            # normally this vocabulary is called from the email_sender form
            # in which the context is the 'emails' container. aq_parent should
            # be the Meeting content.
            query_path = context.aq_parent.getPhysicalPath()
        else:
            # if aq_parent is not IMeeting, use the path of the current context
            query_path = context.getPhysicalPath()

        brains = portal_catalog(
            portal_type="eea.meeting.subscriber",
            path='/'.join(query_path)
        )

        l = set()
        for brain in brains:
            subscriber = brain.getObject()
            term_title = '{} ({})'.format(subscriber.title, subscriber.email)
            l.add((subscriber.email, term_title))

        return SimpleVocabulary([SimpleTerm(s[0], title=s[1]) for s in l])
