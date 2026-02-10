"""upgrade step implementation for blocks defaults"""
# -*- coding: utf-8 -*-

from logging import getLogger

from plone import api

logger = getLogger(__name__)


def _default_blocks_layout():
    blocks = {
        "488c7be8-d15b-4885-abca-b133a2295be9": {
            "@type": "slate",
            "plaintext": "",
            "value": [],
        },
        "e930e15b-4e1e-40d5-bb5e-3b6e3e32b95a": {"@type": "title"},
        "undefined": {"@type": "title"},
    }
    items = [
        "e930e15b-4e1e-40d5-bb5e-3b6e3e32b95a",
        "488c7be8-d15b-4885-abca-b133a2295be9",
    ]
    return {"blocks": blocks, "blocks_layout": {"items": items}}


def _ensure_blocks_layout(meeting):
    defaults = _default_blocks_layout()
    meeting.blocks = defaults["blocks"]
    meeting.blocks_layout = defaults["blocks_layout"]
    meeting.reindexObject()
    return True


def upgrade(setup_tool=None):
    """upgrade function"""
    logger.info("Running upgrade (Python): Blocks defaults for meetings")
    brains = api.content.find(portal_type="eea.meeting")
    updated = 0
    for brain in brains:
        obj = brain.getObject()
        if _ensure_blocks_layout(obj):
            updated += 1

    logger.info("Updated blocks on %s meeting items", updated)
