# -*- coding: utf-8 -*-
from zope.container.interfaces import INameChooser
from zope.interface import implementer
from plone import api
from plone.dexterity.content import Item
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
        return {
            'first_name': member.getProperty('first_name', ''),
            'last_name': member.getProperty('last_name', ''),
            'telephone': member.getProperty('telephone', ''),
            'institution': member.getProperty('institution', ''),
            'from_country': member.getProperty('from_country', ''),
            'from_city': member.getProperty('from_city', '')
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
        is_meeting_ended = (meeting_end_date - today).days < 0
        is_allowed_state_change = is_meeting_ended is not True
        return is_allowed_state_change


def save_email_approved(context):
    types = api.portal.get_tool('portal_types')
    type_info = types.getTypeInfo('eea.meeting.email')
    emails_folder = context.aq_parent.aq_parent['emails']

    name_chooser = INameChooser(emails_folder)

    meeting = context.aq_parent.aq_parent
    meeting_title = meeting.title
    meeting_place = meeting.location

    try:
        first_name = context.get_details().get('first_name', '')
        last_name = context.get_details().get('last_name', '')
        if first_name == "" and last_name == "":
            subscriber_name = context.id
        else:
            subscriber_name = first_name + " " + last_name
    except Exception:
        subscriber_name = 'user'

    subscriber_email = context.email
    email_body = """
        Dear {subscriber_name},
        \n\n
        Thank you for your registration to the {meeting_title}.
        We invite you to carefully look at the meeting documents
        folder in order to start arranging your travel to {meeting_place}.
        Looking forward to a fruitful meeting, do not hesitate to contact
        us if needed at eni-seis2@eea.europa.eu
        \n\n
        Best regards
        \n
        ENI-SEIS II Project Team
        \n\n
        Cher {subscriber_name},
        Merci pour votre inscription à {meeting_title}.
        Nous vous invitons à prendre connaissance des documents de la réunion
        dans le dossier document afin de commencer à organiser votre voyage à
        {meeting_place}. Dans l'attente d'une réunion fructueuse, si vous avez
        des questions n'hésitez pas à nous contacter à l'adresse suivante
        eni-seis2@eea.europa.eu
        \n\n
        Meilleures salutations
        \n
        L’équipe de projet ENI-SEIS II

        """.format(
        subscriber_name=subscriber_name,
        meeting_title=meeting_title,
        meeting_place=meeting_place
    )

    data = {
        'subject': meeting_title,
        'sender': 'eni-seis2@eea.europa.eu',
        'receiver': subscriber_email,
        'cc': '',
        'body': email_body,
    }

    content_id = name_chooser.chooseName(data['subject'], emails_folder)

    obj = type_info._constructInstance(emails_folder, content_id)

    obj.title = data['subject']
    obj.sender = data['sender']
    obj.receiver = data['receiver']
    obj.cc = data['cc']
    obj.subject = data['subject']
    obj.body = data['body']

    obj.reindexObject()


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

        if evt.action == ACTION_APPROVE:
            # Send email after approving participant - content rule
            # is sending the email. Here we save the same details.
            save_email_approved(obj)


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
