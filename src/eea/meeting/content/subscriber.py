from zope.interface import implementer
from plone import api
from plone.dexterity.content import Item
from eea.meeting.interfaces import ISubscriber
from eea.meeting.constants import SUBSCRIBER_META_TYPE
from eea.meeting.constants import ACTION_APPROVE, ACTION_REJECT
import uuid


@implementer(ISubscriber)
class Subscriber(Item):
    """ EEA Meeting Subscriber content type"""

    meta_type = SUBSCRIBER_META_TYPE

    def state(self):
        return api.content.get_state(self)

    def get_details(self):
        member = api.user.get(userid=self.userid)
        return {
            'first_name': member.getProperty('first_name', ''),
            'last_name': member.getProperty('last_name', ''),
            'telephone': member.getProperty('telephone', ''),
            'institution': member.getProperty('institution', ''),
            'from_country': member.getProperty('from_country', ''),
            'from_city': member.getProperty('from_city', '')
        }


def state_change(obj, evt):

    subscribers = obj.aq_parent
    meeting = subscribers.get_meeting()
    subscribers_state = api.content.get_state(subscribers)
    if hasattr(evt, 'action'):
        if (evt.action == ACTION_APPROVE and subscribers_state != 'full' and
                subscribers.approved_count() >= meeting.max_participants):
            api.content.transition(obj=subscribers, transition='to_full')
        elif (evt.action == ACTION_REJECT and subscribers_state == 'full' and
                subscribers.approved_count() < meeting.max_participants):
            api.content.transition(obj=subscribers, transition='to_open')


def on_add(obj, evt):

    obj.uid = uuid.uuid4()
    meeting = obj.aq_parent.aq_parent
    if meeting.auto_approve:
        api.content.transition(obj=obj, transition='approve')


def on_delete(obj, evt):
    subscribers = obj.aq_parent
    meeting = subscribers.get_meeting()
    subscribers_state = api.content.get_state(subscribers)
    if (subscribers_state == 'full' and meeting.allow_register and
            subscribers.approved_count() < meeting.max_participants):
        api.content.transition(obj=subscribers, transition='to_open')
