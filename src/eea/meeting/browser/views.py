from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from eea.meeting.add import create_subscribers


class EEAMeetingView(BrowserView):
    """ EEA Meeting index """

    index = ViewPageTemplateFile("pt/meeting_index.pt")

    def render(self):
        return self.index()

    def __call__(self):
        if not self.context.get('subscribers'):
            create_subscribers(self.context)
        return self.render()
