""" Recipients vocabulary
"""

from zope.interface import implementer

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

import plone.api as api


@implementer(IVocabularyFactory)
class RecipientsVocabulary(object):

    @staticmethod
    def subscriber_list():
        portal_catalog = api.portal.get_tool('portal_catalog')

        brains = portal_catalog(portal_type="eea.meeting.subscriber")

        l = set()
        for brain in brains:
            subscriber = brain.getObject()
            term_title = '{} ({})'.format(subscriber.title, subscriber.email)
            l.add((subscriber.email, term_title))

        results = [SimpleTerm(s[0], title=s[1]) for s in l]
        return results

    def __call__(self, *args, **kwargs):
        return SimpleVocabulary(self.subscriber_list())
