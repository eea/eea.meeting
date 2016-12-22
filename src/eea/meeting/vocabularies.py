""" Vocabularies
"""

# from Products.CMFCore.utils import getToolByName
from plone import api
from zope.component import queryMultiAdapter
from zope.component.hooks import getSite
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


def search_user(context, searchstring):

    results = {}
    users = []

    site = getSite()
    request = getattr(site, 'REQUEST', None)
    cpanel = queryMultiAdapter((site, request), name=u"usergroup-userprefs")
    if cpanel:
        users = cpanel.doSearch(searchstring)

    for user in users:
        uid = user.get('userid', '')
        fullname = user.get('fullname', '')
        email = user.get('email', '')
        org = user.get('o', '')
        title = '"{fullname} ({userid}) {org}" <{email}>'.format(
            fullname=fullname,
            userid=uid,
            email=email,
            org=org
        )
        results[email] = title

    for email, title in results.items():
        yield SimpleTerm(email, title=title)


class LDAPListingVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context, **kwargs):

        vocab = []

        containing = context.REQUEST.get('search_user.widgets.containing')
        # criteria = context.REQUEST.get('search_user.widgets.criteria')

        if context.REQUEST.get('search_user.buttons.search_user') is not None \
           or context.REQUEST.get('search_user.buttons.addCC') is not None:
            vocab = search_user(context, containing)

        return SimpleVocabulary([x for x in vocab])


class RecipientsVocabulary(object):

    implements(IVocabularyFactory)

    def subscriber_list(self):
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
