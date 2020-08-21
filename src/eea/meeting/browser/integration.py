""" Integration """
from Acquisition import aq_inner
from plone.dexterity.browser.add import DefaultAddView


class AddView(DefaultAddView):
    """ Add form page for case studies

    The default add view, as generated by plone.autoform, cannot really use
    a custom FormExtender because the context is not the proper context (the
    one for which we want a custom form), but the container where the content
    is added. So we override this view and properly set the forms, so they can
    be overrided.
    """

    def __init__(self, context, request, ti):
        self.context = context
        self.request = request

        if self.form is not None:

            if ti.klass == 'eea.meeting.content.meeting.Meeting':
                from eea.meeting.browser.views import MeetingAddForm
                self.form = MeetingAddForm

            self.form_instance = self.form(aq_inner(self.context),
                                           self.request)
            self.form_instance.__name__ = self.__name__

        self.ti = ti

        # Set portal_type name on newly created form instance
        if self.form_instance is not None \
           and not getattr(self.form_instance, 'portal_type', None):
            self.form_instance.portal_type = ti.getId()
