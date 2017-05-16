import logging

from plone.contentrules.rule.interfaces import IRuleElementData, IExecutable
from zope.component import adapts
from zope.interface import Interface, implements
from plone.app.contentrules.actions.mail import IMailAction, MailAction, MailActionExecutor

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
    # implements(IExecutable)
    adapts(Interface, ICustomMailAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        super(CustomMailActionExecutor, self).__call__()

