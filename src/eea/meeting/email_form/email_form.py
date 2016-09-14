from eea.meeting import _
from plone.z3cform.layout import wrap_form
from z3c.form import button, form, field
from eea.meeting.events.rules import SendEmailAddEvent
from zope.event import notify
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile
from eea.meeting.interfaces import IEmail
from plone import api
from zope.container.interfaces import INameChooser

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

        types = api.portal.get_tool('portal_types')
        type_info = types.getTypeInfo('eea.meeting.email')

        name_chooser = INameChooser(self.context)
        content_id = name_chooser.chooseName(data['title'], self.context)

        obj = type_info._constructInstance(self.context, content_id)

        obj.sender = data['sender']
        obj.receiver = data['receiver']
        obj.cc = data['cc']
        obj.subject = data['subject']
        obj.body = data['body']

        obj.reindexObject()

        notify(SendEmailAddEvent(obj))

        redirect_url = "%s/@@email_sender_confirmation" % self.context.absolute_url()
        self.request.response.redirect(redirect_url)

SendEmailView = wrap_form(SendEmail, index=FiveViewPageTemplateFile("send_email.pt"))