from Products.Five.browser import BrowserView

class ViewSentEmails(BrowserView):

    email_archive = []

    def emails(self):
        return self.email_archive
