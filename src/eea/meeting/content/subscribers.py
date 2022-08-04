""" Subscribers """
from functools import partial
from operator import attrgetter
from operator import eq
from eea.meeting.interfaces import ISubscribers
import plone.api as api
from plone.dexterity.content import Container
from zope.interface import implementer

APPROVED_STATE = "approved"
NEW_STATE = "new"
REJECTED_STATE = "rejected"


@implementer(ISubscribers)
class Subscribers(Container):
    """EEA Meeting Subscribers container"""

    def get_meeting(self):
        """return meeting"""
        return self.aq_parent

    def approved_count(self):
        """Return number of approved subscribers"""
        is_approved = partial(eq, APPROVED_STATE)
        sub_states = map(api.content.get_state, self.get_subscribers())
        approved = filter(is_approved, sub_states)
        return len(list(approved))

    def subscriber_ids(self):
        """Return subscribers IDs."""
        return map(attrgetter("userid"), self.get_subscribers())

    def get_subscribers(self):
        """Return list of subscribers"""
        return [
            x for x in self.objectValues() if x.portal_type == "eea.meeting.subscriber"
        ]

    def state(self):
        """State"""
        return api.content.get_state(self)


def on_add(obj, evt):
    """on add"""
    pass


def state_change(obj, evt):
    """on state change"""
    pass
