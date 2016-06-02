from zope.interface import implementer
from Products.Five import BrowserView
from plone.dexterity.content import Container
from eea.meeting.interfaces import IMeeting


MEETING_META_TYPE = 'EEA Meeting'


@implementer(IMeeting)
class Meeting(Container):
    """ EEA Meeting content type"""

    meta_type = MEETING_META_TYPE


class Register(BrowserView):

    pass
