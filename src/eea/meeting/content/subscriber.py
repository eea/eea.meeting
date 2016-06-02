from zope.interface import implementer
from plone.dexterity.content import Item
from eea.meeting.interfaces import ISubscriber

SUBSCRIBER_META_TYPE = 'EEA Meeting Subscriber'


@implementer(ISubscriber)
class Subscriber(Item):
    """ EEA Meeting Subscriber content type"""

    meta_type = SUBSCRIBER_META_TYPE
