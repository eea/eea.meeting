from plone.stringinterp.adapters import BaseSubstitution
from eea.meeting import _

class SetEmailSubstitution(BaseSubstitution):

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
        return self.session.get('receiver', '')

    @property
    def subject(self):
        """Email subject"""
        return self.session.get('subject', '')

    @property
    def body(self):
        """Email body"""
        return self.session.get('body', '')

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
