from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone import api

class RecipientsVocabulary(object):

    implements(IVocabularyFactory)

    def subscriber_list(self):
        results = []
        portal_catalog = api.portal.get_tool('portal_catalog')

        brains = portal_catalog(portal_type="eea.meeting.subscriber")

        for brain in brains:
            subscriber = brain.getObject()
            term_title = '{} {} ({})'.format(subscriber.firstname, subscriber.lastname, subscriber.email)
            results.append(SimpleTerm(subscriber.email, title=term_title))
        return results

    def __call__(self, *args, **kwargs):
        return SimpleVocabulary(self.subscriber_list())

class SearchCriteriaVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, *args, **kwargs):
        items = (
            SimpleTerm("name", u"Name"),
            SimpleTerm("email", u"Email"),
            SimpleTerm("organization", u"Organization"),
            SimpleTerm("user_id", u"User ID"),
        )
        return SimpleVocabulary(items)