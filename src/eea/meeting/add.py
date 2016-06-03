from plone.dexterity.utils import createContentInContainer


def handler(obj, evt):
    create_subscribers(obj)


def create_subscribers(container):
    createContentInContainer(container, 'eea.meeting.subscribers',
                             title='Subscribers', id='subscribers')
