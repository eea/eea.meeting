# -*- coding: utf-8 -*-
import logging
from zope.component import queryAdapter
from zope.component.hooks import getSite
from plone.app.controlpanel.security import ISecuritySchema
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

logger = logging.getLogger('eea.meeting')


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

    # Add memcached
    if 'MEMCache' not in site.objectIds():
        try:
            oid = site.manage_addProduct[
                'MemcachedManager'].manage_addMemcachedManager('MEMCache')
        except Exception, err:
            logger.exception(err)
        else:
            cache = site._getOb('MEMCache')
            cache._settings['servers'] = ('memcached:11211',)
            cache._p_changed = True

            # Set cache for ldap-plugin
            ldap_plugin = site['acl_users']['ldap-plugin']
            ldap_plugin.ZCacheable_setManagerId(manager_id='MEMCache')


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
