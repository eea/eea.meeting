from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone import api
from zope.component import getMultiAdapter
from Acquisition import aq_inner

def search_user2(context, request, containing, criteria):

    results = []
    ldap_field = ''
    regular_field = ''

    searchView = getMultiAdapter((aq_inner(context), request), name='pas_search')

    if criteria[0] == 'Name':
        ldap_field = 'cn'
        regular_field = 'title'
    elif criteria[0] == 'Email':
        ldap_field = 'mail'
        regular_field = 'email'
    elif criteria[0] == 'Organization':
        ldap_field = 'o'
    elif criteria[0] == 'User ID':
        ldap_field = 'uid'
        regular_field = 'userid'

    ldapUsers = searchView.searchUsers(**{ldap_field: containing})
    localUsers = searchView.searchUsers(**{regular_field: containing})

    users = ldapUsers + [x for x in localUsers if x not in localUsers]

    for user in users:
        if user['pluginid'] == 'ldap-plugin':
            org = user.get('o', '')
            term_title = '{cn} | {mail} | {uid} | {o}'.format(cn=user['cn'], mail=user['mail'], uid=user['uid'], o=org)
            results.append(SimpleTerm(user['mail'], title=term_title))
        else:
            term_title = '{} | {} | {} '.format(user['title'], user['email'], user['userid'])
            results.append(SimpleTerm(user['email'], title=term_title))

    return results

class LDAPListingVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context, **kwargs):

        vocab = []

        containing = context.REQUEST.get('search_user.widgets.containing')
        criteria = context.REQUEST.get('search_user.widgets.criteria')

        if containing == '' and criteria == ['--NOVALUE--']:
            vocab = []

        if context.REQUEST.get('search_user.buttons.search_user') is not None or context.REQUEST.get('search_user.buttons.addCC') is not None:
            vocab = search_user2(context, context.REQUEST, containing, criteria)

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