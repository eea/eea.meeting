from eea.meeting import _
from plone.z3cform.layout import wrap_form
from z3c.form import button, form, field, group
from eea.meeting.events.rules import SendEmailAddEvent
from zope.event import notify
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile
from eea.meeting.interfaces import IEmail, ISearchUser
from plone import api
from zope.container.interfaces import INameChooser
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from widgets import CustomCheckBoxFieldWidget

class SearchUser(form.Form):

    fields = field.Fields(ISearchUser)
    ignoreContext = True

    fields['results'].widgetFactory = CustomCheckBoxFieldWidget

    prefix = 'search_user'
    template = FiveViewPageTemplateFile('search_user.pt')

    _parent_form = None

    def __init__(self, context, request, parent_form=None):
        super(SearchUser, self).__init__(context, request)
        self._parent_form = parent_form

    @button.buttonAndHandler(_('Search user'), name='search_user')
    def handleSave(self, action):
        data, errors = self.extractData()

        if errors:
            return False


    @button.buttonAndHandler(_('Add to CC'), name='addCC')
    def handle_addCC(self, action):
        data, errors = self.extractData()

        self._parent_form.widgets['cc'].value += '\n'+"\r\n".join(data['results'])

        if errors:
            return False


class SendEmail(form.Form):
    fields = field.Fields(IEmail)
    ignoreContext = True

    fields['receiver'].widgetFactory = CheckBoxFieldWidget

    prefix = 'send_email'

    template = FiveViewPageTemplateFile('main_form.pt')

    def update(self):
        super(SendEmail, self).update()
        self.search_user = SearchUser(self.context, self.request, self)
        self.search_user.update()


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

        obj.receiver = "\r\n".join(data['receiver'])

        data['receiver'] = obj.receiver

        obj.cc = data['cc']

        obj.subject = data['subject']
        obj.body = data['body']
        obj.reindexObject()

        notify(SendEmailAddEvent(self.context, data))

        redirect_url = "%s/@@email_sender_confirmation" % self.context.absolute_url()
        self.request.response.redirect(redirect_url)

SendEmailView = wrap_form(SendEmail, index=FiveViewPageTemplateFile("send_email.pt"))


