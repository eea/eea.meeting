""" upgrade step implementation """
# -*- coding: utf-8 -*-

from logging import getLogger
from eea.meeting.upgrades.base import reload_gs_profile

logger = getLogger(__name__)


def upgrade(setup_tool=None):
    """upgrade function"""
    logger.info("Running upgrade (Python): Configuration for version 2000")
