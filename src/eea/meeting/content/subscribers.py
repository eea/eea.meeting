from functools import partial
from operator import attrgetter
from operator import eq
from eea.meeting.content.subscriber import SUBSCRIBER_META_TYPE
from eea.meeting.interfaces import ISubscribers
import plone.api as api
from plone.dexterity.content import Container
from zope.interface import implementer

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
        is_approved = partial(eq, APPROVED_STATE)
        sub_states = map(api.content.get_state, self.get_subscribers())
        approved = filter(is_approved, sub_states)
        return len(approved)

    def subscriber_ids(self):
        return map(attrgetter('userid'), self.get_subscribers())

    def get_subscribers(self):
        return self.objectValues(SUBSCRIBER_META_TYPE)

    def state(self):
        return api.content.get_state(self)


def on_add(obj, evt):
    pass


def state_change(obj, evt):
    pass
