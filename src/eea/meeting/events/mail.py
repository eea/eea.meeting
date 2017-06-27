# -*- coding: utf-8 -*-
import logging

from plone.contentrules.rule.interfaces import IRuleElementData, IExecutable
from zope.component import adapts
from zope.interface import Interface, implements
from plone.stringinterp.interfaces import IStringInterpolator
from plone.app.contentrules.actions.mail import IMailAction, MailAction, MailActionExecutor
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

    def save_email_approved(self):
        types = api.portal.get_tool('portal_types')
        type_info = types.getTypeInfo('eea.meeting.email')
        emails_folder = self.event.object.aq_parent.aq_parent['emails']

        name_chooser = INameChooser(emails_folder)

        meeting = self.event.object.aq_parent.aq_parent

        interpolator = IStringInterpolator(self.event.object)

        subscriber_email = self.event.object.email
        email_body = interpolator(self.element.message).strip()
        source = interpolator(self.element.source).strip()

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
        self.save_email_approved()

