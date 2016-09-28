from zope.browserpage.viewpagetemplatefile import (
    ViewPageTemplateFile as Z3ViewPageTemplateFile
)

from z3c.form import group
from z3c.form import field
from eea.meeting.interfaces import ISearchUser

class Group(group.Group):
    label = u'LDAP Users'
    fields = field.Fields(ISearchUser).select('results')

    def updateWidgets(self, prefix=None):
        super(Group, self).updateWidgets(prefix)
        self.widgets['results'].template = Z3ViewPageTemplateFile(
            'widgets/ldap_users.pt')
