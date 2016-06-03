from zope.interface import implementer
from Products.Five import BrowserView
from plone.dexterity.content import Container
from eea.meeting.interfaces import IMeeting
from plone import api
from plone.dexterity.utils import createContentInContainer


MEETING_META_TYPE = 'EEA Meeting'


@implementer(IMeeting)
class Meeting(Container):
    """ EEA Meeting content type"""

    meta_type = MEETING_META_TYPE

    def is_registered(self, uid=None):
        if not uid:
            uid = api.user.get_current().getId()
        return uid in self.subscribers.subscriber_ids()

    def can_register(self):
        if self.is_registered():
            # TODO remove debugging prints
            print 'Already registered'
            return False
        if not self.subscribers.approved_count() < self.max_participants:
            # TODO remove debugging prints
            print 'max participants exceeded'
            return False

        return True


class Register(BrowserView):

    def __call__(self):
        subscribers = self.context.get('subscribers')
        if not subscribers:
            # TODO return a warning
            pass
        if api.user.is_anonymous():
            return self.context.REQUEST.redirect(
                subscribers.absolute_url() + '/++add++eea.meeting.subscriber')
        current_user = api.user.get_current()
        uid = current_user.getId()
        if not self.context.can_register():
            # TODO return a warning
            return
        # TODO get user name for title
        createContentInContainer(subscribers, 'eea.meeting.subscriber',
                                 title=uid, id=uid)
        # TODO put success message on session
        return self.context.REQUEST.RESPONSE.redirect(
            self.context.absolute_url())
