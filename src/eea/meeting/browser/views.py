""" Browser controllers
"""

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


class Register(BrowserView):
    """ Register current user
    """

    def __call__(self):
        subscribers = self.context.get('subscribers')
        if not subscribers:
            IStatusMessage(self.request).addStatusMessage(
                "Can't find subscribers directory", type="error")
        if not self.context.can_register():
            IStatusMessage(self.request).addStatusMessage(
                "Registration not allowed", type="error")
        if self.context.is_registered():
            IStatusMessage(self.request).addStatusMessage(
                "User already registered", type="error")
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

        subs_brains = portal_catalog(
                portal_type="eea.meeting.subscriber",
                        )

        user_name = ''
        name = ''
        surname = ''
        institution = ''
        from_country = ''
        from_city = ''
        phone_number = ''
        state = ''
        reimbursed = ''
        role = ''

        for brain in brains:
            email = brain.getObject()
            for x in subs_brains:
                subscriber = x.getObject()
                subscriber_details = subscriber.get_details()
                if email.sender == subscriber.email:
                    user_name = subscriber.getId()
                    name = subscriber_details.get('first_name','')
                    surname = subscriber_details.get('last_name','')
                    institution = subscriber_details.get('institution','')
                    from_country = subscriber_details.get('from_country','')
                    from_city = subscriber_details.get('from_city','')
                    phone_number = subscriber_details.get('telephone','')
                    state = subscriber.state()
                    reimbursed = subscriber.reimbursed
                    role = subscriber.role


            results.append({
                'sender': email.sender,
                # 'receiver': ', '.join(email.receiver or []),
                # 'cc': ', '.join(email.cc or []),
                # 'subject': email.subject,
                # 'body': email.body,
                'user_name':user_name,
                'name': name,
                'surname': surname,
                'institution': institution,
                'from_country': from_country,
                'from_city': from_city,
                'phone_number': phone_number,
                'state': state,
                'reimbursed' : reimbursed,
                'role' : role,

            })

        return results

