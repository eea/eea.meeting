""" Evolve email """
from plone.app.textfield.value import IRichTextValue
import plone.api as api

from eea.meeting.upgrades import LOGGER


def run(context):
    """evolve email field"""
    catalog = api.portal.get_tool("portal_catalog")
    brains = catalog(portal_type="eea.meeting.email")

    for brain in brains:
        email = brain.getObject()
        url = email.absolute_url(1)
        updated = False
        if IRichTextValue.providedBy(email.body):
            email.body = email.body.raw
            updated = True
            LOGGER.info('Updated "body" for %s.', url)

        if email.receiver is not None and not isinstance(email.receiver, set):
            email.receiver = set(email.receiver.split())
            updated = True
            LOGGER.info('Updated "receiver" for %s.', url)

        if email.cc is not None and not isinstance(email.cc, list):
            email.cc = email.cc.split()
            updated = True
            LOGGER.info('Updated "cc" for %s.', url)

        if updated:
            email.reindexObject()
