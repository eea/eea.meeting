from datetime import datetime
import pytz
from zope.interface import implementer
from AccessControl import getSecurityManager
from plone import api
from plone.dexterity.content import Container
from plone.dexterity.utils import createContentInContainer
from eea.meeting.interfaces import IMeeting


MEETING_META_TYPE = 'EEA Meeting'


@implementer(IMeeting)
class Meeting(Container):
    """ EEA Meeting content type"""

    meta_type = MEETING_META_TYPE

    def is_anonymous(self):
        return api.user.is_anonymous()

    def is_registered(self, uid=None):
        if not uid:
            uid = api.user.get_current().getId()
        return uid in self.subscribers.subscriber_ids()

    def subscriber_status(self, uid=None):
        if not uid:
            uid = api.user.get_current().getId()
        if self.is_registered(uid):
            return api.content.get_status(getattr(self.subscribers, uid))

    def can_register(self):
        open = self.registrations_open()
        if not open:
            return False
        return True

    def is_admin(self):
        sm = getSecurityManager()
        return sm.checkPermission("EEA Meting: Admin Meeting", self)

    def registrations_open(self):
        return (self.allow_register and
                datetime.now(pytz.UTC) < self.end and
                self.subscribers.approved_count() < self.max_participants)

        return True

    def get_subscribers(self):
        return self.subscribers.get_subscribers()


def on_save(obj, evt):
    # This triggers also on the container creation, not only on save props!
    subscribers = getattr(obj, 'subscribers', None)
    if subscribers:
        if subscribers.registrations_open():
                if api.content.get_state(subscribers) == 'closed':
                    api.content.transition(obj=subscribers,
                                           transition='to_open')
        elif api.content.get_state(subscribers) == 'open':
            api.content.transition(obj=subscribers, transition='close')


def on_add(obj, evt):
    create_subscribers(obj)

    create_emails(obj)


def create_subscribers(container):
    createContentInContainer(container, 'eea.meeting.subscribers',
                             title='Subscribers', id='subscribers')


def create_emails(container):
    createContentInContainer(container, 'eea.meeting.emails',
                             title='Emails', id='emails')
