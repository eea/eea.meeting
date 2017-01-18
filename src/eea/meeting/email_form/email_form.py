from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FPT
from Products.statusmessages.interfaces import IStatusMessage
from eea.meeting import _
from eea.meeting.email_form.widgets import CustomCheckBoxFieldWidget
from eea.meeting.events.rules import SendEmailAddEvent
from eea.meeting.interfaces import IEmail, ISearchUser
from plone import api
from plone.z3cform.layout import wrap_form
from z3c.form import button, form, field
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope.container.interfaces import INameChooser
from zope.event import notify


class SearchUser(form.Form):

    fields = field.Fields(ISearchUser)
    ignoreContext = True

    fields['results'].widgetFactory = CustomCheckBoxFieldWidget

    prefix = 'search_user'
    template = FPT('search_user.pt')

    _parent_form = None

    def __init__(self, context, request, parent_form=None):
        super(SearchUser, self).__init__(context, request)
        self._parent_form = parent_form

    @button.buttonAndHandler(_('Search'), name='search_user')
    def handleSave(self, action):
        data, errors = self.extractData()

        if errors:
            return False

    @button.buttonAndHandler(_('Add'), name='addCC')
    def handle_addCC(self, action):
        data, errors = self.extractData()

        self._parent_form.widgets['cc'].value += \
            '\n'+"\n".join(data['results'])

        del self.widgets['results'].items
        self.widgets['results'].value = ''

        if errors:
            return False


class SendEmail(form.Form):
    fields = field.Fields(IEmail)
    ignoreContext = True

    label = _(u"Send email")

    fields['receiver'].widgetFactory = CheckBoxFieldWidget

    prefix = 'send_email'

    template = FPT('main_form.pt')

    def update(self):
        super(SendEmail, self).update()
        self.search_user = SearchUser(self.context, self.request, self)
        self.search_user.update()
        self.widgets['body'].rows = 10

    @button.buttonAndHandler(_('Send Email'), name='send_email')
    def handleSave(self, action):
        data, errors = self.extractData()

        if errors:
            return False

        types = api.portal.get_tool('portal_types')
        type_info = types.getTypeInfo('eea.meeting.email')

        name_chooser = INameChooser(self.context)
        content_id = name_chooser.chooseName(data['subject'], self.context)

        obj = type_info._constructInstance(self.context, content_id)

        obj.title = data['subject']
        obj.sender = data['sender']
        obj.receiver = data['receiver']
        obj.cc = data['cc']
        obj.subject = data['subject']
        obj.body = data['body']

        obj.reindexObject()

        notify(SendEmailAddEvent(self.context, data))

        msg = _(u"Email successfully sent")
        IStatusMessage(self.request).addStatusMessage(msg, type='info')
        self.request.response.redirect(
            self.context.getParentNode().absolute_url())

SendEmailView = wrap_form(SendEmail, index=FPT("send_email.pt"))
