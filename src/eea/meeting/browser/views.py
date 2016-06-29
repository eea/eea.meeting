from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.dexterity.utils import createContentInContainer
from plone.app.content.browser import foldercontents

from eea.meeting.content.meeting import create_subscribers


class MeetingView(foldercontents.FolderContentsView):
    """ EEA Meeting index """

    index = ViewPageTemplateFile("pt/meeting_index.pt")

    def render(self):
        return self.index()

    def __call__(self):
        if not self.context.get('subscribers'):
            create_subscribers(self.context)
        return self.render()

    def get_auth_user_name(self):
        return api.user.get_current().getId()

    def contents_table(self):
        table = FolderContentsTable(aq_inner(self.context), self.request)
        return table.render()


class FolderContentsTable(foldercontents.FolderContentsTable):
    def folderitems(self):
        items = super(FolderContentsTable, self).folderitems()
        filtered = [item for item in items if item['id'] != 'subscribers']
        return filtered


class SubscribersView(BrowserView):
    """ EEA Meeting Subscribers index """

    index = ViewPageTemplateFile("pt/subscribers_index.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()


class Register(BrowserView):

    def __call__(self):
        subscribers = self.context.get('subscribers')
        if not subscribers:
            # TODO return a warning
            pass
        if not self.context.can_register():
            # TODO return a warning
            return
        else:
            current_user = api.user.get_current()
            uid = current_user.getProperty('uid')
            firstname = current_user.getProperty('firstname')
            lastname = current_user.getProperty('lastname')
            fullname = current_user.getProperty('fullname')

            createContentInContainer(subscribers, 'eea.meeting.subscriber',
                                     title=fullname, id=uid, uid=uid,
                                     firstname=firstname, lastname=lastname)
            # TODO put success message on session
            return self.context.REQUEST.RESPONSE.redirect(
                self.context.absolute_url())
