from zope.interface import implementer
from plone.app.contentrules.handlers import execute
from interfaces import ISendEmailEvent
from interfaces import ISendEmailAddEvent

@implementer(ISendEmailEvent)
class SendEmailEvent(object):
    def __init__(self, context, **kwargs):
        self.object = context

@implementer(ISendEmailAddEvent)
class SendEmailAddEvent(SendEmailEvent):
    """ Sending email after form submission
    """

def execute_event(event):
    """ Execute custom rules
    """
    execute(event.object, event)
