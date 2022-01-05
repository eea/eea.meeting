""" Subscriber """
# -*- coding: utf-8 -*-
import datetime
import uuid
from eea.meeting.constants import ACTION_APPROVE, ACTION_REJECT
from eea.meeting.interfaces import ISubscriber
from plone import api
from plone.api.exc import MissingParameterError
from plone.dexterity.content import Item
from zope.interface import implementer


@implementer(ISubscriber)
class Subscriber(Item):
    """EEA Meeting Subscriber content type"""

    def state(self):
        """Subscriber's state"""
        return api.content.get_state(self)

    def get_details(self):
        """Details for subscriber"""
        try:
            member = api.user.get(userid=self.userid)
        except MissingParameterError:
            member = None

        if not member:
            return {"edit_url": "{0}/edit".format(self.absolute_url())}

        return {
            "first_name": member.getProperty("first_name", ""),
            "last_name": member.getProperty("last_name", ""),
            "fullname": member.getProperty("fullname", ""),
            "telephone": member.getProperty("telephone", ""),
            "phone_numbers": ", ".join(member.getProperty("phone_numbers", [])),
            "institution": member.getProperty("institution", ""),
            "from_country": member.getProperty("from_country", ""),
            "from_city": member.getProperty("from_city", ""),
            "position": member.getProperty("position", ""),
            "address": member.getProperty("address", ""),
            "edit_url": "{0}/edit".format(self.absolute_url()),
        }

    def is_allowed_state_change(self):
        """Used as transition guard expression to prevent state change
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
    """state change"""

    subscribers = obj.aq_parent
    meeting = subscribers.get_meeting()
    subscribers_state = api.content.get_state(subscribers)
    if hasattr(evt, "action"):
        if (
            evt.action == ACTION_APPROVE
            and subscribers_state != "full"
            and subscribers.approved_count() >= meeting.max_participants
        ):
            api.content.transition(obj=subscribers, transition="to_full")
        elif (
            evt.action == ACTION_REJECT
            and subscribers_state == "full"
            and subscribers.approved_count() < meeting.max_participants
        ):
            api.content.transition(obj=subscribers, transition="to_open")


def on_add(obj, evt):
    """on add"""

    obj.uid = uuid.uuid4()
    meeting = obj.aq_parent.aq_parent
    if meeting.auto_approve:
        api.content.transition(obj=obj, transition="approve")


def on_delete(obj, evt):
    """on delete"""
    subscribers = obj.aq_parent
    meeting = subscribers.get_meeting()
    subscribers_state = api.content.get_state(subscribers)
    if (
        subscribers_state == "full"
        and meeting.allow_register
        and subscribers.approved_count() < meeting.max_participants
    ):
        api.content.transition(obj=subscribers, transition="to_open")
