# -*- coding: utf-8 -*-
import logging

from plone.contentrules.rule.interfaces import IRuleElementData
from zope.component import adapts
from zope.interface import Interface, implements
from plone.stringinterp.interfaces import IStringInterpolator
from plone.app.contentrules.actions.mail import IMailAction
from plone.app.contentrules.actions.mail import MailActionExecutor
from plone.app.contentrules.actions.mail import MailAction
from zope.container.interfaces import INameChooser

from plone import api

logger = logging.getLogger("plone.contentrules")


class ICustomMailAction(IMailAction):
    """Definition of the configuration available for a mail action
    """


class CustomMailAction(MailAction):

    implements(ICustomMailAction, IRuleElementData)

    element = 'eea.meeting.events.CustomMail'


class CustomMailActionExecutor(MailActionExecutor):
    """The executor for this action.
    """
    adapts(Interface, ICustomMailAction, Interface)

    def save_email(self):
        if self.event.object.portal_type == 'eea.meeting.subscriber':
            """ This is the case for approving a subscriber:
                - Thank you for your registration
            """
            meeting = self.event.object.aq_parent.aq_parent
            subscriber_email = self.event.object.email

        elif self.event.object.portal_type == 'eea.meeting':
            """ This is the case for new subscriber registered:
                - A new participant has registered to the meeting
                - You have registered to the meeting
            """
            meeting = self.event.object
            subscriber_email = api.user.get_current().getProperty('email')

        types = api.portal.get_tool('portal_types')
        type_info = types.getTypeInfo('eea.meeting.email')
        emails_folder = meeting['emails']

        name_chooser = INameChooser(emails_folder)
        interpolator = IStringInterpolator(self.event.object)
        email_body = interpolator(self.element.message).strip()

        try:
            source = interpolator(self.element.source).strip()
        except Exception:
            source = ''

        data = {
            'subject': meeting.title,
            'sender': source,
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

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        super(CustomMailActionExecutor, self).__call__()
        self.save_email()
