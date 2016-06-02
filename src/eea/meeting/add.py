from plone import api


def handler(obj, evt):
    create_subscribers(obj)


def create_subscribers(container):
    api.content.create(
        type='eea.meeting.subscribers',
        title='Subscribers',
        id='subscribers',
        container=container)
