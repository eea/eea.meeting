""" LDAP Users """
from eea.meeting.interfaces import ISearchUser
from z3c.form import field
from z3c.form import group
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile as PTF
# from z3c.form.browser.checkbox import CheckBoxFieldWidget


class ResultsGroup(group.Group):
    """ Results Group """
    label = u'LDAP Users'
    fields = field.Fields(ISearchUser).select('results')

    # fields['results'].widgetFactory = CheckBoxFieldWidget

    def updateWidgets(self, prefix=None):
        """ update widgets """
        super(ResultsGroup, self).updateWidgets(prefix)
        self.widgets['results'].template = PTF('widgets/ldap_users.pt')
