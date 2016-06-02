from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from eea.meeting.add import create_subscribers
from eea.meeting.content.subscriber import SUBSCRIBER_META_TYPE


class MeetingView(BrowserView):
    """ EEA Meeting index """

    index = ViewPageTemplateFile("pt/meeting_index.pt")

    def render(self):
        return self.index()

    def __call__(self):
        if not self.context.get('subscribers'):
            create_subscribers(self.context)
        return self.render()


class SubscribersView(BrowserView):
    """ EEA Meeting Subscribers index """

    index = ViewPageTemplateFile("pt/subscribers_index.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def get_subscribers(self):
        return self.context.objectValues(SUBSCRIBER_META_TYPE)

