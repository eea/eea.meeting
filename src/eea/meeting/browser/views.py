""" Browser controllers
"""

from DateTime import DateTime
from functools import partial
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from eea.meeting import _
from eea.meeting.content.meeting import create_subscribers
from eea.meeting.content.subscribers import APPROVED_STATE
import plone.api as api
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.browser.view import DefaultView
from plone.dexterity.interfaces import IDexterityEditForm
from plone.dexterity.utils import createContentInContainer
from plone.z3cform import layout
from plone.z3cform.fieldsets.extensible import FormExtender
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import classImplements


def add_subscriber(subscribers, **kwargs):
    return createContentInContainer(
        subscribers,
        'eea.meeting.subscriber',
        checkConstraints=False,
        **kwargs
    )


class MeetingView(DefaultView):
    """ EEA Meeting index """

    def formatted_date(self, occ):
        provider = getMultiAdapter(
            (self.context, self.request, self),
            IContentProvider, name='formatted_date'
        )
        return provider(occ)

    def get_auth_user_name(self):
        return api.user.get_current().getId()

    def has_sent_emails(self):
        """ Check if there are any sent mails in the archive.
        """
        return self.context.unrestrictedTraverse('emails').keys()

    def has_subscribers(self):
        """ Check if there are any subscribers.
        """
        return self.context.unrestrictedTraverse('subscribers').keys()

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


class MeetingFormExtender(FormExtender):
    def update(self):
        self.move('IGeolocatable.geolocation', after='location')
        self.form.fields['IGeolocatable.geolocation'].field.title = \
            u'Event location on map'


class MeetingEditForm(DefaultEditForm):
    """ Edit form for case studies
    """


MeetingEditView = layout.wrap_form(MeetingEditForm)
classImplements(MeetingEditView, IDexterityEditForm)


class MeetingAddForm(DefaultAddForm):
    """ Add Form for case studies
    """


class SubscribersView(BrowserView):
    """ EEA Meeting Subscribers index """

    def __call__(self, *args, **kwargs):
        if not self.context.aq_parent.allow_register:
            IStatusMessage(self.request).addStatusMessage(
                "Users are not allowed to register to this meeting. "
                "Please edit the meeting and enable the property "
                "\"Allow users to register to the meeting\" if you want "
                "this feature to be active.", type="info")
        return super(SubscribersView, self).__call__(*args, **kwargs)

    def can_edit(self):
        return api.user.has_permission(
            'Modify portal content',
            obj=self.context
        )


class SubscribersApi(BrowserView):
    """ Manage subscribers.
    """

    def __call__(self):
        if self.request.method == 'POST':
            return self.on_post()

    def on_post(self):
        subscribers = tuple(
            self.context.get(s)
            for s in self.request.get('subscribers', [])
        )

        if 'button.delete' in self.request:
            self.delete(subscribers)
        elif 'button.approve' in self.request:
            self.approve(subscribers)
        elif 'button.reject' in self.request:
            self.reject(subscribers)

        return self.request.response.redirect(self.context.absolute_url())

    def _change_state(self, state, subscribers):
        action = partial(api.content.transition, to_state=state)
        map(action, subscribers)

    def delete(self, subscribers):
        self.context.manage_delObjects([s.getId() for s in subscribers])

    def approve(self, subscribers):
        self._change_state('approved', subscribers)

    def reject(self, subscribers):
        self._change_state('rejected', subscribers)


class Register(BrowserView):
    """ Register current user
    """

    def __call__(self):
        subscribers = self.context.get('subscribers')

        try:
            self.validate(subscribers)
        except Exception as e:
            IStatusMessage(self.request).addStatusMessage(
                e.message, type="error")
            return self.request.response.redirect(self.context.absolute_url())

        current_user = api.user.get_current()
        uid = current_user.getId()
        fullname = current_user.getProperty('fullname', uid)
        email = current_user.getProperty('email')

        r_val = self.request.form.get("form.widgets.reimbursed", "true")
        reimbursed = True if r_val == 'true' else False

        try:
            role = self.request.form.get("form.widgets.role")[0]
        except Exception:
            role = "other"

        props = dict(
            title=fullname,
            id=uid,
            userid=uid,
            email=email,
            reimbursed=reimbursed,
            role=role,
        )

        add_subscriber(subscribers, **props)

        IStatusMessage(self.request).addStatusMessage(
            "You have succesfully registered to this meeting", type="info")

        return self.request.response.redirect(self.context.absolute_url())

    def validate(self, subscribers):
        if not subscribers:
            raise Exception("Can't find subscribers directory")
        if not self.context.can_register():
            raise Exception("Registration not allowed")
        if self.context.is_registered():
            raise Exception("User already registered")


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
        cpanel = getMultiAdapter((site, self.request),
                                 name=u"usergroup-userprefs")
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


class ViewEmail(BrowserView):
    """ Email view in mail archive
    """


class ViewSentEmails(BrowserView):
    """Sent Emails Archive"""

    def email_archive(self):
        results = []
        portal_catalog = api.portal.get_tool('portal_catalog')
        current_path = "/".join(self.context.getPhysicalPath())

        brains = portal_catalog(
            portal_type="eea.meeting.email",
            sort_on='created',
            sort_order='descending',
            path=current_path
        )

        for brain in brains:
            email = brain.getObject()

            email_receiver = email.receiver
            if isinstance(email_receiver, basestring) is True:
                email_receiver = [email_receiver]

            if isinstance(email_receiver, set):
                email_receiver = list(email_receiver)

            results.append({
                'sender': email.sender,
                'receiver': ', '.join(email_receiver or []),
                'cc': ', '.join(email.cc or []),
                'subject': email.subject,
                'body': email.body,
                'ModificationDate': self.context.toLocalizedTime(
                    DateTime(email.ModificationDate())),
                'absolute_url': email.absolute_url(),
                'email_type': email.email_type
            })

        return results


class WorkspaceAccessView(DefaultView):
    """ /@@current_user_has_access
    """

    def __call__(self, *args, **kwargs):
        YES_FLAG = "has_access"
        NO_FLAG = "has_not_access"
        workspace = self.aq_parent
        meeting = workspace.aq_parent  # meeting/workspace/@@current...

        if workspace.can_edit(meeting):
            return YES_FLAG

        subscribers = meeting.get_subscribers()

        approved_subscribers_ids = [
            subscriber.userid for subscriber in subscribers
            if subscriber.state() == "approved"
        ]

        is_anonymous = api.user.is_anonymous()
        if not is_anonymous:
            current_user = api.user.get_current()
            has_access = current_user.id in approved_subscribers_ids
            if has_access is True:
                has_access = YES_FLAG
            else:
                has_access = NO_FLAG
        else:
            has_access = NO_FLAG

        return has_access
