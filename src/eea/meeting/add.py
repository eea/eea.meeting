""" Add """
from plone.dexterity.utils import createContentInContainer


def handler(obj, evt):
    """handler"""
    create_subscribers(obj)


def create_subscribers(container):
    """create subscribers"""
    createContentInContainer(
        container, "eea.meeting.subscribers", title="Subscribers", id="subscribers"
    )
