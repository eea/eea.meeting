from zope.interface import implementer
from eea.meeting.interfaces import IEmail
from plone.dexterity.content import Container


@implementer(IEmail)
class Email(Container):
    """ EEA Meeting Email content type"""
