from datetime import datetime
import pytz
from AccessControl import getSecurityManager
from plone import api
from plone.app.dexterity.behaviors.constrains import ConstrainTypesBehavior
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from eea.meeting.interfaces import IMeeting, ISubscribers

ACQUIRE = -1  # acquire locallyAllowedTypes from parent (default)
DISABLED = 0  # use default behavior of PortalFolder which uses the FTI info
ENABLED = 1  # allow types from locallyAllowedTypes only


class MeetingConstrainTypes(ConstrainTypesBehavior):

    def allowedContentTypes(self, context=None):
        """
        If constraints are enabled, return the locally allowed types.
        If the setting is ACQUIRE, acquire the locally allowed types according
        to the ACQUIRE rules, described in the interface.
        If constraints are disabled, use the default addable types

        This method returns the FTI, NOT the FTI id, like most other methods.
        """
        portal = api.portal.getSite()
        subscribers = portal.portal_types.get('eea.meeting.subscribers')
        if context is None:
            context = self.context
        mode = self.getConstrainTypesMode()
        default_addable = self.getDefaultAddableTypes(context)

        if mode == DISABLED:
            allowed = default_addable
        elif mode == ENABLED:
            if hasattr(self.context, 'locally_allowed_types'):
                allowed = [t for t in default_addable if t.getId() in
                           self.context.locally_allowed_types]
            else:
                allowed = default_addable
        elif mode == ACQUIRE:
            parent = self.context.__parent__
            parent_constrain_adapter = ISelectableConstrainTypes(parent, None)
            if not parent_constrain_adapter:
                allowed = default_addable
            else:
                return_tids = self._filterByDefaults(
                    parent_constrain_adapter.getLocallyAllowedTypes(context))
                allowed = [t for t in default_addable if
                           t.getId() in return_tids]
        else:
            raise Exception(
                "Wrong constraint setting. %i is an invalid value",
                mode)

        if (IMeeting.providedBy(context) and
                context.get('subscribers')):
            if subscribers in allowed:
                allowed.remove(subscribers)

        return allowed

    def getDefaultAddableTypes(self, context=None):
        portal = api.portal.getSite()
        subscribers = portal.portal_types.get('eea.meeting.subscribers')
        if context is None:
            context = self.context
        allowed = self._getAddableTypesFor(self.context, context)
        if (IMeeting.providedBy(context) and
                context.get('subscribers')):
            if subscribers in allowed:
                allowed.remove(subscribers)
        return allowed


class IMeetingConstrainTypes(ISelectableConstrainTypes):

    """ """


class SubscribersConstrainTypes(ConstrainTypesBehavior):

    def allowedContentTypes(self, context=None):
        """
        If constraints are enabled, return the locally allowed types.
        If the setting is ACQUIRE, acquire the locally allowed types according
        to the ACQUIRE rules, described in the interface.
        If constraints are disabled, use the default addable types

        This method returns the FTI, NOT the FTI id, like most other methods.
        """
        portal = api.portal.getSite()
        subscriber = portal.portal_types.get('eea.meeting.subscriber')
        if context is None:
            context = self.context
        mode = self.getConstrainTypesMode()
        default_addable = self.getDefaultAddableTypes(context)

        if mode == DISABLED:
            allowed = default_addable
        elif mode == ENABLED:
            if hasattr(self.context, 'locally_allowed_types'):
                allowed = [t for t in default_addable if t.getId() in
                           self.context.locally_allowed_types]
            else:
                allowed = default_addable
        elif mode == ACQUIRE:
            parent = self.context.__parent__
            parent_constrain_adapter = ISelectableConstrainTypes(parent, None)
            if not parent_constrain_adapter:
                allowed = default_addable
            else:
                return_tids = self._filterByDefaults(
                    parent_constrain_adapter.getLocallyAllowedTypes(context))
                allowed = [t for t in default_addable if
                           t.getId() in return_tids]
        else:
            raise Exception(
                "Wrong constraint setting. %i is an invalid value",
                mode)

        if ISubscribers.providedBy(context) and subscriber in allowed:
            if not allow_register(context):
                allowed.remove(subscriber)

        return allowed

    def getDefaultAddableTypes(self, context=None):
        portal = api.portal.getSite()
        subscribers = portal.portal_types.get('eea.meeting.subscribers')
        if context is None:
            context = self.context
        allowed = self._getAddableTypesFor(self.context, context)
        if (ISubscribers.providedBy(context) and
                context.get('subscribers')):
            if subscribers in allowed:
                allowed.remove(subscribers)
        return allowed


class ISubscribersConstrainTypes(ISelectableConstrainTypes):

    """ """


def allow_register(context):
    sm = getSecurityManager()
    meeting = context.aq_parent
    if not IMeeting.providedBy(meeting):
        return False
    if (not meeting.allow_register or datetime.now(pytz.UTC) > meeting.end or
        len(context.objectValues(
            'EEA Meeting Subscriber')) >= context.max_participants):
        if not sm.checkPermission("EEA Meting: Admin Meeting", meeting):
            return False

    return True
