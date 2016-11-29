""" Browser controllers
"""

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from eea.meeting import _
from eea.meeting.content.meeting import create_subscribers
from eea.meeting.content.subscribers import APPROVED_STATE
from plone import api
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.utils import createContentInContainer
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from zope.contentprovider.interfaces import IContentProvider


class MeetingView(DefaultView):
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

    @property
    def can_list_content(self):
        if not self.context.restrict_content_access:
            return True

        if self.context.is_admin():
            return True

        user = self.get_auth_user_name()
        for subscriber in self.context.subscribers.values():
            if subscriber.state() != APPROVED_STATE:
                continue
            if subscriber.userid == user:
                return True
        return False

    def _allowedPortalTypes(self):
        """ Filter allowed ctypes
        """
        allowed = [ctype.title for ctype in self.context.allowedContentTypes()]
        if not allowed:
            allowed = ['Folder', 'File', 'Image', 'Link']

        for ctype in allowed:
            if 'Subscribers' in ctype:
                continue
            if 'Emails' in ctype:
                continue
            yield ctype

    @property
    def allowedPortalTypes(self):
        """ Get allowed children portal_types
        """
        return [ctype for ctype in self._allowedPortalTypes()]

    def update(self):
        super(MeetingView, self).update()
        if not self.context.get('subscribers'):
            create_subscribers(self.context)


class SubscribersView(BrowserView):
    """ EEA Meeting Subscribers index """


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
                                     title=fullname, id=uid, userid=uid,
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
                title=fullname, id=username, userid=username,
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
