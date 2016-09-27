from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone import api

def place_results(obj, results):
     # term_title = '| | |'.format(obj.firstname + " " + obj.lastname, obj.uid, obj.email) #, title=term_title)
    results.append(SimpleTerm(obj.email))

def user_listing(substring, criteria):
    results = []
    portal_catalog = api.portal.get_tool('portal_catalog')

    print type(criteria)
    print substring == ''

    brains = portal_catalog(portal_type="eea.meeting.subscriber")

    for brain in brains:
        user = brain.getObject()

        if criteria[0] == 'Name':
            if user.firstname.find(substring) > -1 or user.lastname.find(substring) > -1:
                place_results(user, results)
        elif criteria[0] == 'Email':
            if user.email.find(substring) > -1:
                place_results(user, results)
        elif criteria[0] == 'Organization':
            pass
        elif criteria[0] == 'User ID':
            if str(user.uid).find(substring) > -1:
                place_results(user, results)


    return results

class LDAPListingVocabulary(object):

    implements(IVocabularyFactory)


    def __call__(self, context, **kwargs):

        vocab = []

        if context.REQUEST.get('search_user.buttons.search_user') is not None:
            criteria = context.REQUEST.get('search_user.widgets.criteria')
            containing = context.REQUEST.get('search_user.widgets.containing')
            if containing != '':
                vocab = user_listing(containing, criteria)

        return SimpleVocabulary(vocab)

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