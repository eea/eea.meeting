""" Browser controllers
"""
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from Acquisition import aq_inner
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.dexterity.utils import createContentInContainer
from plone.app.content.browser import foldercontents
from zope.contentprovider.interfaces import IContentProvider

from eea.meeting import _
from eea.meeting.content.meeting import create_subscribers
from eea.meeting.content.subscribers import APPROVED_STATE


class MeetingView(BrowserView):
    """ EEA Meeting index """

    index = ViewPageTemplateFile("pt/meeting_index.pt")

    def formatted_date(self, occ):
        provider = getMultiAdapter(
            (self.context, self.request, self),
            IContentProvider, name='formatted_date'
        )
        return provider(occ)

    def get_auth_user_name(self):
        return api.user.get_current().getId()

    def contents_table(self):
        table = MeetingContentsTable(aq_inner(self.context), self.request)
        return table.render()

    @property
    def allowedPortalTypes(self):
        """ Get allowed children portal_types
        """
        allowed_content = self.context.allowedContentTypes()
        results = [ct_type.title for ct_type in allowed_content]
        return results

    def __call__(self):
        if not self.context.get('subscribers'):
            create_subscribers(self.context)
        return self.index()

class MeetingContentsTable(foldercontents.FolderContentsTable):
    def folderitems(self):
        items = super(MeetingContentsTable, self).folderitems()
        filtered = [item for item in items if item['id'] != 'subscribers' and item['id']!= 'emails']
        return filtered


class SubscribersView(BrowserView):
    """ EEA Meeting Subscribers index """

    index = ViewPageTemplateFile("pt/subscribers_index.pt")

    def __call__(self):
        return self.index()

    def contents_table(self):
        table = SubscribersContentsTable(aq_inner(self.context), self.request)
        return table.render()


class SubscribersContentsTable(foldercontents.FolderContentsTable):
    def folderitems(self):
        items = super(SubscribersContentsTable, self).folderitems()
        if not self.context.is_admin():
            return [item for item in items
                    if item['wf_state'] == APPROVED_STATE]
        else:
            return items


class Register(BrowserView):
    """ Register current user
    """
    def __call__(self):
        subscribers = self.context.get('subscribers')
        if not subscribers:
            IStatusMessage(self.request).addStatusMessage(
                "Can't find subscribers directory", type="error")
            return
        if not self.context.can_register():
            IStatusMessage(self.request).addStatusMessage(
                "Registration not allowed", type="error")
            return
        else:
            current_user = api.user.get_current()
            uid = current_user.getId()
            fullname = current_user.getProperty('fullname', uid)
            email = current_user.getProperty('email')

            createContentInContainer(subscribers, 'eea.meeting.subscriber',
                                     checkConstraints=False,
                                     title=fullname, id=uid,
                                     email=email)

            IStatusMessage(self.request).addStatusMessage(
                "You have succesfully registered to this meeting", type="info")
            return self.request.response.redirect(self.context.absolute_url())


class RegisterUser(BrowserView):
    """ Register a user
    """
    label = _(u"Register user")

    def __init__(self, context, request):
        super(RegisterUser, self).__init__(context, request)
        self._searchString = ''

    @property
    def searchString(self):
        """ Search string
        """
        if not self._searchString:
            self._searchString = self.request.get('searchstring', '')
        return self._searchString

    @property
    def users(self):
        """ Users
        """
        if not self.searchString:
            return []

        site = getSite()
        cpanel = getMultiAdapter((site, self.request), name=u"usergroup-userprefs")
        return cpanel.doSearch(self.searchString)

    def _register(self, users):
        """ Register users
        """
        subscribers = self.context.get('subscribers')
        emails = [sub.email for sub in subscribers.values()]
        for username in users:
            user = api.user.get(username)
            fullname = user.getProperty('fullname', username)
            email = user.getProperty('email')
            if email in emails:
                continue

            createContentInContainer(
                subscribers, 'eea.meeting.subscriber',
                checkConstraints=False,
                title=fullname, id=username,
                email=email)

        IStatusMessage(self.request).addStatusMessage(
                "Users registered to this meeting", type="info")
        return self.request.response.redirect(
            self.context.absolute_url() + '/register_user')


    def __call__(self, *args, **kwargs):
        if self.request.method.lower() != 'post':
            return self.index()

        if not self.request.get('form.button.register', None):
            return self.index()

        users = self.request.get('users', [])
        if not users:
            return self.index()

        return self._register(users)


class ViewSentEmails(BrowserView):
    """Sent Emails Archive"""

    def email_archive(self):
        results = []
        portal_catalog = api.portal.get_tool('portal_catalog')
        current_path = "/".join(self.context.getPhysicalPath())

        brains = portal_catalog(portal_type="eea.meeting.email",
                                path=current_path)

        for brain in brains:
            email = brain.getObject()
            results.append({
                'sender': email.sender,
                'receiver': email.receiver,
                'cc': email.cc,
                'subject': email.subject,
                'body': email.body,
            })

        return results
