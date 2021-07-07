""" Mail """
# -*- coding: utf-8 -*-
import logging

from plone import api
from plone.app.contentrules.actions.mail import IMailAction
from plone.app.contentrules.actions.mail import MailAction
from plone.app.contentrules.actions.mail import MailActionExecutor
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.stringinterp.interfaces import IStringInterpolator
from zope.component import adapter
from zope.container.interfaces import INameChooser
from zope.interface import Interface, implementer

from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces.controlpanel import IMailSchema
from zope.component import getUtility

logger = logging.getLogger("plone.contentrules")


class ICustomMailAction(IMailAction):
    """ Definition of the configuration available for a mail action
    """


@implementer(ICustomMailAction, IRuleElementData)
class CustomMailAction(MailAction):
    """ Custom Mail
    """

    element = 'eea.meeting.events.CustomMail'


@adapter(Interface, ICustomMailAction, Interface)
class CustomMailActionExecutor(MailActionExecutor):
    """ The executor for this action.
    """

    def save_email(self):
        """ Save email
        """
        email_type = "N/A"

        if self.event.object.portal_type == 'eea.meeting.subscriber':
            # This is the case for approving a subscriber:
            #    - Thank you for your registration
            meeting = self.event.object.aq_parent.aq_parent
            state = self.event.object.subscriber_status()
            if state == "approved":
                email_type = u"Approval"
            elif state == "rejected":
                email_type = u"Rejection"

        elif self.event.object.portal_type == 'eea.meeting':
            # This is the case for new subscriber registered:
            #   - A new participant has registered to the meeting
            #   - You have registered to the meeting
            meeting = self.event.object
            email_type = u"Registration"

        types = api.portal.get_tool('portal_types')
        type_info = types.getTypeInfo('eea.meeting.email')
        emails_folder = meeting['emails']

        name_chooser = INameChooser(emails_folder)
        interpolator = IStringInterpolator(self.event.object)
        email_body = interpolator(self.element.message).strip()
        recipients = interpolator(self.element.recipients).strip()
        source = self.mail_settings.email_from_address

        data = {
            'subject': meeting.title,
            'sender': source,
            'receiver': recipients,
            'cc': '',
            'body': email_body,
            'email_type': email_type,
        }

        content_id = name_chooser.chooseName(data['subject'], emails_folder)
        obj = type_info._constructInstance(emails_folder, content_id)

        obj.title = data['subject']
        obj.sender = data['sender']
        obj.receiver = data['receiver']
        obj.cc = data['cc']
        obj.subject = data['subject']
        obj.body = data['body']
        obj.email_type = data['email_type']

        obj.reindexObject()

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event
        registry = getUtility(IRegistry)
        self.mail_settings = registry.forInterface(IMailSchema,
                                                   prefix='plone')

    def __call__(self):
        super(CustomMailActionExecutor, self).__call__()
        self.save_email()
