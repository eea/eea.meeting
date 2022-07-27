""" upgrade profile base utilities """
# -*- coding: utf-8 -*-
from plone.app.upgrade.utils import loadMigrationProfile


def reload_gs_profile(context):
    """function to reload the base profile"""
    loadMigrationProfile(
        context,
        "profile-eea.meeting:default",
    )
