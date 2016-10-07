from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone import api
from zope.component import getMultiAdapter
from Acquisition import aq_inner

def search_user2(context, request, containing, criteria):

    results = []

    searchView = getMultiAdapter((aq_inner(context), request), name='pas_search')

    if criteria[0] == 'Name':
        ldap_field = 'cn'
        regular_field = 'description'
    elif criteria[0] == 'Email':
        ldap_field = 'mail'
        regular_field = 'email'
    # elif criteria[0] == 'Organization':
    #     ldap_field = 'o'
    #     regular_field = None
    elif criteria[0] == 'User ID':
        ldap_field = 'uid'
        regular_field = 'userid'

    # import pdb;pdb.set_trace()
    ldapUsers = searchView.searchUsers(**{ldap_field: containing})
    localUsers = searchView.searchUsers(**{regular_field: containing})

    # for field in [ldap_field, regular_field]:
    #     explicit_users = searchView.searchUsers(**{field: containing})
    #
    import pdb;pdb.set_trace()
    #
    # for user in explicit_users:
    #     if user['pluginid'] == 'ldap-plugin':
    #         term_title = '{} | {} | {} | {}'.format(user['cn'], user['mail'], user['uid'])
    #         results.append(SimpleTerm(user['mail'], title=term_title))
    #     else:
    #         term_title = '{} | {} | {} '.format(user['title'], user['email'], user['userid'])
    #         results.append(SimpleTerm(user['email'], title=term_title))
    #
    # return results



# def place_results(obj, results):
#     term_title = '{} | {} | {}'.format(obj.firstname + " " + obj.lastname, obj.uid, obj.email)
#
#     results.append(SimpleTerm(obj.email, title=term_title))
#
# def user_listing(substring, criteria):
#     results = []
#
#     portal_catalog = api.portal.get_tool('portal_catalog')
#     brains = portal_catalog(portal_type="eea.meeting.subscriber")
#
#     for brain in brains:
#         user = brain.getObject()
#
#         if criteria[0] == 'Name':
#             if user.firstname.find(substring) > -1 or user.lastname.find(substring) > -1:
#                 place_results(user, results)
#         elif criteria[0] == 'Email':
#             if user.email.find(substring) > -1:
#                 place_results(user, results)
#         elif criteria[0] == 'Organization':
#             pass
#         elif criteria[0] == 'User ID':
#             if str(user.uid).find(substring) > -1:
#                 place_results(user, results)
#
#     return results

class LDAPListingVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context, **kwargs):

        vocab = []

        containing = context.REQUEST.get('search_user.widgets.containing')
        criteria = context.REQUEST.get('search_user.widgets.criteria')

        if containing == '' and criteria == ['--NOVALUE--']:
            vocab = []

        if context.REQUEST.get('search_user.buttons.search_user') is not None or context.REQUEST.get('search_user.buttons.addCC') is not None:
            # vocab = user_listing(containing, criteria)

            vocab = search_user2(context, context.REQUEST, containing, criteria)

            # searchView = getMultiAdapter((aq_inner(context), context.REQUEST), name='pas_search')
            #
            #
            # explicit_users = [searchView.searchUsers(**{field: containing}) for field in ['cn']]
            # import pdb;pdb.set_trace()







            # users = UsersOverviewControlPanel(context, context.REQUEST)
            # user_list = UsersOverviewControlPanel.doSearch(users, containing)
            #
            # for user in user_list:
            #     place_results2(user, vocab)





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