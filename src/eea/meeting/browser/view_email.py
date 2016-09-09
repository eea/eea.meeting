from Products.Five.browser import BrowserView

class ViewSentEmails(BrowserView):

    email_archive = []

    def emails(self):

        results = []

        for email in self.email_archive:
            results.append({
                'sender': email['sender'],
                'receiver': email['receiver'],
                'cc': email['cc'],
                'subject': email['subject'],
                'body': email['body'],
            })

        print results
