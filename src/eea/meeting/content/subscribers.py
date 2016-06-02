from zope.interface import implementer
from plone.dexterity.content import Container
from eea.meeting.interfaces import ISubscribers

SUBSCRIBERS_META_TYPE = 'EEA Meeting Subscribers'


@implementer(ISubscribers)
class Subscribers(Container):
    """ EEA Meeting Subscribers container"""

    meta_type = SUBSCRIBERS_META_TYPE
