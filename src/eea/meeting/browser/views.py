from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.dexterity.utils import createContentInContainer
from plone.app.content.browser import foldercontents

from eea.meeting.content.meeting import create_subscribers
from eea.meeting.content.subscribers import APPROVED_STATE


class MeetingView(BrowserView):
    """ EEA Meeting index """

    index = ViewPageTemplateFile("pt/meeting_index.pt")

    def __call__(self):
        if not self.context.get('subscribers'):
            create_subscribers(self.context)
        return self.index()

    def get_auth_user_name(self):
        return api.user.get_current().getId()

    def contents_table(self):
        table = MeetingContentsTable(aq_inner(self.context), self.request)
        return table.render()


class MeetingContentsTable(foldercontents.FolderContentsTable):
    def folderitems(self):
        items = super(MeetingContentsTable, self).folderitems()
        filtered = [item for item in items if item['id'] != 'subscribers' and item['id']!= 'emails']
        return filtered


class SubscribersView(BrowserView):
    """ EEA Meeting Subscribers index """

    index = ViewPageTemplateFile("pt/subscribers_index.pt")

    def __call__(self):
        return self.index()

    def contents_table(self):
        table = SubscribersContentsTable(aq_inner(self.context), self.request)
        return table.render()


class SubscribersContentsTable(foldercontents.FolderContentsTable):
    def folderitems(self):
        items = super(SubscribersContentsTable, self).folderitems()
        if not self.context.is_admin():
            return [item for item in items
                    if item['wf_state'] == APPROVED_STATE]
        else:
            return items

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
            email = current_user.getProperty('email')

            createContentInContainer(subscribers, 'eea.meeting.subscriber',
                                     title=fullname, id=uid, uid=uid,
                                     firstname=firstname, lastname=lastname,
                                     email=email)
            # TODO put success message on session
            return self.context.REQUEST.RESPONSE.redirect(
                self.context.absolute_url())

class ViewSentEmails(BrowserView):
    """Sent Emails Archive"""

    def email_archive(self):
        results = []
        portal_catalog = api.portal.get_tool('portal_catalog')
        current_path = "/".join(self.context.getPhysicalPath())

        brains = portal_catalog(portal_type="eea.meeting.email",
                                path=current_path)

        for brain in brains:
            email = brain.getObject()
            results.append({
                'sender': email.sender,
                'receiver': email.receiver,
                'cc': email.cc,
                'subject': email.subject,
                'body': email.body,
            })

        return results
