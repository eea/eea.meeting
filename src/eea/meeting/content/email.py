from zope.interface import implementer
from eea.meeting.interfaces import IEmail
from plone.dexterity.content import Container
from plone.dexterity.utils import createContentInContainer

@implementer(IEmail)
class Email(Container):
    """ EEA Meeting Email content type"""

# def on_add(obj, evt):
#     create_email(obj)
#
# def create_email(container):
#     createContentInContainer(container, 'eea.meeting.email',
#                              title='Email', id='email')



