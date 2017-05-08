from plone.stringinterp.adapters import BaseSubstitution
from eea.meeting import _


class SetEmailSubstitution(BaseSubstitution):

    attribute = u''

    def __init__(self, context, **kwargs):
        super(SetEmailSubstitution, self).__init__(context, **kwargs)
        self._session = None

    @property
    def session(self):
        """ User session
        """
        if self._session is None:
            sdm = getattr(self.context, 'session_data_manager', None)
            self._session = sdm.getSessionData(create=False) if sdm else {}
        return self._session

    @property
    def sender(self):
        """Email sender"""
        return self.session.get('sender', '')

    @property
    def receiver(self):
        """Email receiver"""
        return ','.join(self.session.get('receiver', []) or [])

    @property
    def subject(self):
        """Email subject"""
        return self.session.get('subject', '')

    @property
    def body(self):
        """Email body"""
        return self.session.get('body', '')

    @property
    def cc(self):
        """Email cc addresses"""
        return ','.join(self.session.get('cc', []) or [])

    def safe_call(self):
        """ Safe call
        """
        return getattr(self, self.attribute, u'')


class SetEmailSender(SetEmailSubstitution):
    category = _(u'Email Send')
    description = _(u'Email sender address')
    attribute = u'sender'


class SetEmailReceiver(SetEmailSubstitution):
    category = _(u'Email Send')
    description = _(u'Email receiver address')
    attribute = u'receiver'


class SetEmailSubject(SetEmailSubstitution):
    category = _(u'Email Send')
    description = _(u'Email subject')
    attribute = u'subject'


class SetEmailBody(SetEmailSubstitution):
    category = _(u'Email Send')
    description = _(u'Email body')
    attribute = u'body'


class SetEmailCC(SetEmailSubstitution):
    category = _(u'Email Send')
    description = _(u'Email CC addresses')
    attribute = u'cc'


class SetMeetingContactEmail(BaseSubstitution):
    category = _(u'Notify meeting contact person')
    description = _(u'Meeting contact email')

    def safe_call(self):
        """ Safe call
        """
        try:
            email = self.context.contact_email
        except Exception:
            email = ''

        return email


class SetEmailReceiverOnApproved(BaseSubstitution):
    category = _(u'Approve Subscriber')
    description = _(u'Subscriber Email')

    def safe_call(self):
        """ Safe call
        """
        try:
            email = self.context.email
        except Exception:
            email = ''

        return email


class SetNameReceiverOnApproved(BaseSubstitution):
    category = _(u'Approve Subscriber')
    description = _(u'Subscriber Name')

    def safe_call(self):
        """ Safe call
        """
        try:
            first_name = self.context.get_details().get('first_name', '')
            last_name = self.context.get_details().get('last_name', '')
            if first_name == "" and last_name == "":
                name = self.context.id
            else:
                name = first_name + " " + last_name
        except Exception:
            name = 'user'

        return name


class SetMeetingPlaceOnApproved(BaseSubstitution):
    category = _(u'Approve Subscriber')
    description = _(u'Meeting place')

    def safe_call(self):
        """ Safe call
        """
        try:
            location = self.context.aq_parent.aq_parent.location
        except Exception:
            location = ""

        return location


class SetMeetingTitleOnApproved(BaseSubstitution):
    category = _(u'Approve Subscriber')
    description = _(u'Meeting title')

    def safe_call(self):
        """ Safe call
        """
        try:
            title = self.context.aq_parent.aq_parent.title
        except Exception:
            title = ""

        return title
