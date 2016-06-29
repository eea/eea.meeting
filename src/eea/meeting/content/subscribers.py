from zope.interface import implementer
from plone import api
from plone.dexterity.content import Container
from eea.meeting.interfaces import ISubscribers
from eea.meeting.content.subscriber import SUBSCRIBER_META_TYPE

SUBSCRIBERS_META_TYPE = 'EEA Meeting Subscribers'
APPROVED_STATE = 'approved'
NEW_STATE = 'new'
REJECTED_STATE = 'rejected'


@implementer(ISubscribers)
class Subscribers(Container):
    """ EEA Meeting Subscribers container"""

    meta_type = SUBSCRIBERS_META_TYPE

    def get_meeting(self):
        return self.aq_parent

    def approved_count(self):
        all_subscribers = self.objectValues(SUBSCRIBER_META_TYPE)
        return len([part for part in all_subscribers if
                    api.content.get_state(part) == APPROVED_STATE])

    def subscriber_ids(self):
        return [subscriber.getId() for subscriber in
                self.objectValues(SUBSCRIBER_META_TYPE)]

    def get_subscribers(self):
        return self.objectValues(SUBSCRIBER_META_TYPE)

    def state(self):
        return api.content.get_state(self)


def on_add(obj, evt):
    pass


def state_change(obj, evt):
    pass
