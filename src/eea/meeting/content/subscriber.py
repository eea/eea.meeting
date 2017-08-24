# -*- coding: utf-8 -*-
from zope.container.interfaces import INameChooser
from zope.interface import implementer
from plone import api
from plone.dexterity.content import Item
from Products.CMFPlone.utils import safe_unicode
from eea.meeting.interfaces import ISubscriber
from eea.meeting.constants import SUBSCRIBER_META_TYPE
from eea.meeting.constants import ACTION_APPROVE, ACTION_REJECT
import datetime
import uuid


@implementer(ISubscriber)
class Subscriber(Item):
    """ EEA Meeting Subscriber content type"""

    meta_type = SUBSCRIBER_META_TYPE

    def state(self):
        return api.content.get_state(self)

    def get_details(self):
        member = api.user.get(userid=self.userid)
        if not member:
            return {}
        return {
            'first_name': member.getProperty('first_name', ''),
            'last_name': member.getProperty('last_name', ''),
            'fullname': member.getProperty('fullname', ''),
            'telephone': member.getProperty('telephone', ''),
            'phone_numbers': ', '.join(member.getProperty('phone_numbers', [])),
            'institution': member.getProperty('institution', ''),
            'from_country': member.getProperty('from_country', ''),
            'from_city': member.getProperty('from_city', ''),
            'position': member.getProperty('position', ''),
            'address': member.getProperty('address', '')
        }

    def is_allowed_state_change(self):
        """ Used as transition guard expression to prevent state change
            for subscribers of ended meetings

            /portal_workflow/meeting_subscriber_workflow/transitions/approve
                /manage_properties
            Guard expression:
            python:here.is_allowed_state_change() is True
        """
        meeting_end_date = self.aq_parent.aq_parent.end.replace(tzinfo=None)
        today = datetime.datetime.today()
        is_meeting_ended = (meeting_end_date - today).days < -1
        is_allowed_state_change = is_meeting_ended is not True
        return is_allowed_state_change

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
