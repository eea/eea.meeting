from plone.restapi.services import Service
import plone.api as api
from eea.meeting.browser.views import add_subscriber
import plone.protect.interfaces
from zope.interface import alsoProvides


class Register(Service):
    """Register current user"""

    def __call__(self):
        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(self.request, plone.protect.interfaces.IDisableCSRFProtection)
        subscribers = self.context.get("subscribers")
        try:
            self.validate(subscribers)
        except Exception as e:
            self.request.response.setStatus(400)
            result = {
                "message": str(e),
            }
            return result

        current_user = api.user.get_current()
        uid = current_user.getId()
        fullname = current_user.getProperty("fullname", uid)
        email = current_user.getProperty("email")

        r_val = self.request.form.get("form.widgets.reimbursed", "true")
        reimbursed = True if r_val == "true" else False

        try:
            role = self.request.form.get("form.widgets.role")[0]
        except Exception:
            role = "other"

        props = dict(
            title=fullname,
            id=uid,
            userid=uid,
            email=email,
            reimbursed=reimbursed,
            role=role,
        )
        try:
            add_subscriber(subscribers, **props)
        except Exception as e:
            self.request.response.setStatus(400)
            result = {
                "message": str(e),
            }
            return result

        self.request.response.setStatus(201)
        result = {
            "message": "You have succesfully registered to this meeting",
        }
        return result

    def validate(self, subscribers):
        """validate"""
        if not subscribers:
            raise Exception("Can't find subscribers directory")
        if not self.context.can_register():
            raise Exception("Registration not allowed")
        if self.context.is_registered():
            raise Exception("User already registered")
        if self.context.allow_anonymous_registration:
            raise Exception("Fill in the registration form")
