from eea.meeting import _
from plone.z3cform.layout import wrap_form
from z3c.form import button, form, field
from eea.meeting.events.rules import SendEmailAddEvent
from zope.event import notify
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile
from eea.meeting.browser.view_email import ViewSentEmails
from eea.meeting.interfaces import IEmail

class SendEmail(form.Form):

    fields = field.Fields(IEmail)
    ignoreContext = True

    def updateWidgets(self):
        super(SendEmail, self).updateWidgets()

    @button.buttonAndHandler(_('Send Email'), name='send_email')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            return False

        notify(SendEmailAddEvent(self.context, data))

        ViewSentEmails.email_archive.append(data)

        redirect_url = "%s/@@email_sender_confirmation" % self.context.absolute_url()
        self.request.response.redirect(redirect_url)

SendEmailView = wrap_form(SendEmail, index=FiveViewPageTemplateFile("send_email.pt"))