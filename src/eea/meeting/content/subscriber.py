from zope.interface import implementer
from plone.dexterity.content import Item
from eea.meeting.interfaces import ISubscriber


@implementer(ISubscriber)
class Subscriber(Item):
    """ Subscriber content type"""
