from z3c.form import interfaces, util
from z3c.form.browser import widget
from z3c.form.widget import FieldWidget, SequenceWidget
from zope.i18n import translate
import zope.schema.interfaces


@zope.component.adapter(zope.schema.interfaces.IField, interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def CustomCheckBoxFieldWidget(field, request):
    return FieldWidget(field, CustomCheckBoxWidget(request))


@zope.interface.implementer(interfaces.ISequenceWidget)
class CustomSequenceWidget(SequenceWidget):

    def extract(self, default=interfaces.NO_VALUE):
        """See z3c.form.interfaces.IWidget."""
        if ((self.name not in self.request) and (self.name + '-empty-marker' in
                                                 self.request)):
            return []

        return self.request.get(self.name, default)


@zope.interface.implementer_only(interfaces.ICheckBoxWidget)
class CustomCheckBoxWidget(widget.HTMLInputWidget, CustomSequenceWidget):
    """Input type checkbox widget implementation."""

    klass = u'checkbox-widget'
    css = u'checkbox'
    items = ()

    def isChecked(self, term):
        return term.token in self.value

    def update(self):
        """See z3c.form.interfaces.IWidget."""
        super(CustomCheckBoxWidget, self).update()
        widget.addFieldClass(self)
        # ZZZ: this is to early for setup items. See select widget how this
        # sould be done. Setup the items here doens't allow to override the
        # widget.value in updateWidgets, ri
        self.items = []
        for count, term in enumerate(self.terms):
            checked = self.isChecked(term)
            id = '%s-%i' % (self.id, count)
            if zope.schema.interfaces.ITitledTokenizedTerm.providedBy(term):
                label = translate(term.title, context=self.request,
                                  default=term.title)
            else:
                label = util.toUnicode(term.value)
            self.items.append({
                'id': id,
                'name': self.name + ':list',
                'value': term.token,
                'label': label,
                'checked': checked
            })

    def json_data(self):
        data = super(CustomCheckBoxWidget, self).json_data()
        data['options'] = self.items
        data['type'] = 'check'
        return data
