from zope.interface import provider
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from eea.meeting import _
from zope import schema
from plone.autoform import directives
from plone.schema import Email
from z3c.form.browser.text import TextFieldWidget
from plone.z3cform.layout import wrap_form
from z3c.form import button, form, field
from eea.meeting.events.rules import SendEmailAddEvent
from zope.event import notify
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile

@provider(IFormFieldProvider)
class ISendEmail(model.Schema):

    sender = Email(
        title=_(u"From"),
        required=True,
    )

    receiver = Email(
        title=_(u"To"),
        required=True,
    )

    subject = schema.TextLine(
        title=_(u"Subject"),
        required=True,
    )

    body = schema.Text(
        title=_(u"Body"),
        required=True,
    )

    directives.widget(
        'sender',
        TextFieldWidget,
        klass=u'mail_widget'
    )

    directives.widget(
        'receiver',
        TextFieldWidget,
        klass=u'mail_widget'
    )

class SendEmail(form.Form):

    fields = field.Fields(ISendEmail)
    ignoreContext = True

    def updateWidgets(self):
        super(SendEmail, self).updateWidgets()

    @button.buttonAndHandler(_('Send Email'), name='send_email')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            return False

        notify(SendEmailAddEvent(self.context, data))

        redirect_url = "%s/@@email_sender" % self.context.absolute_url()
        self.request.response.redirect(redirect_url)

SendEmailView = wrap_form(SendEmail, index=FiveViewPageTemplateFile("send_email.pt"))