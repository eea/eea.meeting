from zope.interface import implementer
from Products.Five import BrowserView
from plone.dexterity.content import Container
from eea.meeting.interfaces import ISubscribers


@implementer(ISubscribers)
class Subscribers(Container):
    """ Subscribers container"""

    meta_type = 'EEA Meeting subscribers'
