""" Vocabularies
"""

from zope.component import queryMultiAdapter
from zope.component.hooks import getSite
from zope.interface import implementer

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


def search_user(searchstring):
    """ search user """

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


@implementer(IVocabularyFactory)
class LDAPListingVocabulary(object):
    """ LDAP Listing """

    def __call__(self, context, **kwargs):

        vocab = []

        containing = context.REQUEST.get('search_user.widgets.containing')

        if context.REQUEST.get('search_user.buttons.search_user') is not None \
           or context.REQUEST.get('search_user.buttons.addCC') is not None:
            vocab = search_user(containing)

        return SimpleVocabulary([x for x in vocab])
