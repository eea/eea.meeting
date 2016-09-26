from eea.meeting import _
from plone.z3cform.layout import wrap_form
from z3c.form import button, form, field
from eea.meeting.events.rules import SendEmailAddEvent
from zope.event import notify
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile
from eea.meeting.interfaces import IEmail, ISearchUser
from plone import api
from zope.container.interfaces import INameChooser
from z3c.form.browser.checkbox import CheckBoxFieldWidget

def place_results(obj, results):
    results.append({
        'user_name': obj.firstname+" "+obj.lastname,
        'user_id': obj.uid,
        'email': obj.email
    })

def user_listing(substring, criteria):

    results = []
    portal_catalog = api.portal.get_tool('portal_catalog')

    brains = portal_catalog(portal_type="eea.meeting.subscriber")

    for brain in brains:
        user = brain.getObject()

        if criteria == 'name':
            if user.firstname.find(substring)>-1 or user.lastname.find(substring)>-1:
                place_results(user, results)
        elif criteria == 'email':
            if user.email.find(substring) > -1:
                place_results(user, results)
        elif criteria == 'organization':
            pass
        elif criteria == 'user_id':
            if str(user.uid).find(substring) > -1:
                place_results(user, results)

    print results


class SearchUser(form.Form):

    fields = field.Fields(ISearchUser)
    ignoreContext = True
    prefix = 'search_user'
    template = FiveViewPageTemplateFile('search_user.pt')

    @button.buttonAndHandler(_('Search user'), name='search_user')
    def handleSave(self, action):
        data, errors = self.extractData()

        if errors:
            return False

        if data['criteria'] is not None and data['containing'] is not None:
            criteria = data['criteria']
            containing = data['containing']
            user_listing(containing, criteria)

class SendEmail(form.Form):
    fields = field.Fields(IEmail)
    ignoreContext = True

    fields['receiver'].widgetFactory = CheckBoxFieldWidget

    prefix = 'send_email'

    template = FiveViewPageTemplateFile('main_form.pt')

    def update(self):
        super(SendEmail, self).update()
        self.search_user = SearchUser(self.context, self.request)
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
