""" Mail """
# -*- coding: utf-8 -*-
import logging
from smtplib import SMTPException

from Acquisition import aq_inner
from plone import api
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.actions.mail import (
    IMailAction,
    MailAction,
    MailActionExecutor,
)
from plone.base.interfaces.controlpanel import IMailSchema
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.registry.interfaces import IRegistry
from plone.stringinterp.interfaces import IStringInterpolator
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.controlpanel import IMailSchema
from Products.MailHost.MailHost import MailHostError
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import adapter, getUtility
from zope.container.interfaces import INameChooser
from zope.globalrequest import getRequest
from zope.interface import Interface, implementer
from zope.interface.interfaces import ComponentLookupError

logger = logging.getLogger("plone.contentrules")


class ICustomMailAction(IMailAction):
    """Definition of the configuration available for a mail action"""


@implementer(ICustomMailAction, IRuleElementData)
class CustomMailAction(MailAction):
    """Custom Mail"""

    element = "eea.meeting.events.CustomMail"


@adapter(Interface, ICustomMailAction, Interface)
class CustomMailActionExecutor(MailActionExecutor):
    """The executor for this action."""

    def save_email(self):
        """Save email"""
        email_type = "N/A"
        meeting = None
        if self.event.object.portal_type == "eea.meeting.subscriber":
            # This is the case for approving a subscriber:
            #    - Thank you for your registration
            meeting = self.event.object.aq_parent.aq_parent
            state = self.event.object.subscriber_status()
            if state == "approved":
                email_type = "Approval"
            elif state == "rejected":
                email_type = "Rejection"

        elif self.event.object.portal_type == "eea.meeting":
            # This is the case for new subscriber registered:
            #   - A new participant has registered to the meeting
            #   - You have registered to the meeting
            meeting = self.event.object
            email_type = "Registration"

        if meeting is None:
            return

        types = api.portal.get_tool("portal_types")
        type_info = types.getTypeInfo("eea.meeting.email")
        emails_folder = meeting["emails"]

        name_chooser = INameChooser(emails_folder)
        interpolator = IStringInterpolator(self.event.object)
        email_body = interpolator(self.element.message).strip()
        recipients = interpolator(self.element.recipients).strip()
        source = self.mail_settings.email_from_address

        data = {
            "subject": meeting.title,
            "sender": source,
            "receiver": {recipients},
            "cc": "",
            "body": email_body,
            "email_type": email_type,
        }

        if data["receiver"]:
            content_id = name_chooser.chooseName(
                data["subject"], emails_folder
            )
            obj = type_info._constructInstance(emails_folder, content_id)

            obj.title = data["subject"]
            obj.sender = data["sender"]
            obj.receiver = data["receiver"]
            obj.cc = data["cc"]
            obj.subject = data["subject"]
            obj.body = data["body"]
            obj.email_type = data["email_type"]

            obj.reindexObject()

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event
        registry = getUtility(IRegistry)
        self.mail_settings = registry.forInterface(IMailSchema, prefix="plone")

    def __call__(self):
        # super(CustomMailActionExecutor, self).__call__()
        self.send_email()
        self.save_email()

    def send_email(self):
        mailhost = getToolByName(aq_inner(self.context), "MailHost")
        if not mailhost:
            raise ComponentLookupError(
                "You must have a Mailhost utility to execute this action"
            )

        email_charset = self.mail_settings.email_charset
        obj = self.event.object
        interpolator = IStringInterpolator(obj)
        source = self.element.source

        if source:
            source = interpolator(source).strip()

        if not source:
            # no source provided, looking for the site wide from email
            # address
            from_address = self.mail_settings.email_from_address
            if not from_address:
                # the mail can't be sent. Try to inform the user
                request = getRequest()
                if request:
                    messages = IStatusMessage(request)
                    msg = _(
                        "Error sending email from content rule. You must "
                        "provide a source address for mail "
                        "actions or enter an email in the portal properties"
                    )
                    messages.add(msg, type="error")
                return False

            from_name = self.mail_settings.email_from_name.strip('"')
            source = f'"{from_name}" <{from_address}>'

        recip_string = interpolator(self.element.recipients)
        if recip_string:  # check recipient is not None or empty string
            recipients = {
                str(mail.strip())
                for mail in recip_string.split(",")
                if mail.strip()
            }
        else:
            recipients = set()

        if self.element.exclude_actor:
            mtool = getToolByName(aq_inner(self.context), "portal_membership")
            actor_email = mtool.getAuthenticatedMember().getProperty(
                "email", ""
            )
            if actor_email in recipients:
                recipients.remove(actor_email)

        # prepend interpolated message with \n to avoid interpretation
        # of first line as header
        message = f"\n{interpolator(self.element.message)}"

        subject = interpolator(self.element.subject)

        for email_recipient in recipients:
            try:
                # XXX: We're using "immediate=True" because otherwise we won't
                # be able to catch SMTPException as the smtp connection is made
                # as part of the transaction apparatus.
                # AlecM thinks this wouldn't be a problem if mail queuing was
                # always on -- but it isn't. (stevem)
                # so we test if queue is not on to set immediate
                mailhost.send(
                    message,
                    email_recipient,
                    source,
                    subject=subject,
                    charset=email_charset,
                    immediate=not mailhost.smtp_queue,
                )
            except (MailHostError, SMTPException):
                logger.exception(
                    "mail error: Attempt to send mail in content rule failed"
                )

        return True
