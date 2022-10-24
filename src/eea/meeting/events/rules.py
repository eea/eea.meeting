""" Rules """
from zope.interface import implementer
from plone.app.contentrules.handlers import execute
from eea.meeting.events.interfaces import ISendEmailEvent
from eea.meeting.events.interfaces import ISendEmailAddEvent
from eea.meeting.events.interfaces import ISendNewSubscriberEmailEvent


@implementer(ISendEmailEvent)
class SendEmailEvent(object):
    """Send Email Event"""

    def __init__(self, context, **kwargs):
        self.object = context


@implementer(ISendEmailAddEvent)
class SendEmailAddEvent(SendEmailEvent):
    """Sending email after form submission"""

    def __init__(self, context, data):
        super(SendEmailAddEvent, self).__init__(context)
        sdm = getattr(context, "session_data_manager", None)
        session = sdm.getSessionData(create=True) if sdm else None

        data["body"] = data["body"]

        session.update(data)


@implementer(ISendNewSubscriberEmailEvent)
class SendNewSubscriberEmailEvent(SendEmailEvent):
    """Notify when a new user subscribed."""

    def __init__(self, context, **data):
        super(SendNewSubscriberEmailEvent, self).__init__(context)
        sdm = getattr(context, "session_data_manager", None)
        session = sdm.getSessionData(create=True) if sdm else None
        session.update(data)


def execute_event(event):
    """Execute custom rules"""
    execute(event.object, event)
