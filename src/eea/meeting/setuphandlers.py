# -*- coding: utf-8 -*-
from zope.component import queryAdapter
from zope.component.hooks import getSite
from plone.app.controlpanel.security import ISecuritySchema
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'eea.meeting:uninstall',
        ]


def post_install(context):
    """Post install script"""
    site = getSite()
    security = queryAdapter(site, ISecuritySchema)
    if security:
        security.enable_self_reg = True
        security.enable_user_pwd_choice = True


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
