from zope.component.interfaces import IObjectEvent


class ISendEmailEvent(IObjectEvent):
    """ Base Event interface for sending email after form submission
    """


class ISendEmailAddEvent(ISendEmailEvent):
    """ Send email after form submission
    """


class ISendNewSubscriberEmailEvent(ISendEmailEvent):
    """ Notify when a new user subscribed.
    """
