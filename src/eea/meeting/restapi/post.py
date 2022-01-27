from plone.restapi.services import Service
import plone.api as api
from eea.meeting.browser.views import add_subscriber
import plone.protect.interfaces
from zope.interface import alsoProvides
from plone.restapi.deserializer import json_body
import plone.api as api


class SubscribersManipulation(Service):
    def delete(self, subscribers):
        """delete"""
        self.context.manage_delObjects(subscribers)

    def approve(self, subscribers):
        """approve"""
        self._change_state("approve", subscribers)

    def reject(self, subscribers):
        """reject"""
        self._change_state("reject", subscribers)

    def _change_state(self, state, subscribers):
        """change state"""
        for subscriber in subscribers:
            elem = self.context.get(subscriber)
            try:
                api.content.transition(obj=elem, transition=state)
            except:
                pass

    def reply(self):

        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(self.request, plone.protect.interfaces.IDisableCSRFProtection)
        data = json_body(self.request)
        manipulation_type = data.get("manipulation_type", None)
        subscriberSelection = data.get("subscriberSelection", [])
        return_dict = {}
        if manipulation_type and subscriberSelection:
            if manipulation_type == "delete":
                self.delete(subscriberSelection)
                return_dict = {"message": "Well deleted"}
            elif manipulation_type == "approve":
                self.approve(subscriberSelection)
                return_dict = {"message": "Well approved"}
            elif manipulation_type == "reject":
                self.reject(subscriberSelection)
                return_dict = {"message": "Well rejected"}
        subscribers = api.content.find(context=self.context, portal_type="eea.meeting.subscriber")
        
        objects = [subscriber.getObject() for subscriber in subscribers]
        return_dict["items"] = [
            {
                "id": subscriber.id,
                "title": subscriber.Title(),
                "email": subscriber.email,
                "review_state": subscriber.state(),
            }
            for subscriber in objects
        ]

        return return_dict


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
        email = current_user.getProperty("email", None)

        r_val = self.request.form.get("form.widgets.reimbursed", "true")
        reimbursed = True if r_val == "true" else False

        try:
            role = self.request.form.get("form.widgets.role")[0]
        except Exception:
            role = "other"

        if email:
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
                "email": email,
                "message": "You have succesfully registered to this meeting",
            }
            return result
        else:
            self.request.response.setStatus(201)
            result = {
                "message": "You have no email address in your profile",
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
