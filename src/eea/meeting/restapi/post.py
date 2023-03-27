# -*- coding: utf-8 -*-
import plone.protect.interfaces
from eea.meeting.browser.views import add_subscriber
from plone import api
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zope.interface import alsoProvides

SUBSCRIBER_NOT_DELETED = 1
SUBSCRIBER_NOT_APPROVED = 2
SUBSCRIBER_NOT_REJECTED = 3


class SubscribersManipulation(Service):
    def delete(self, subscribers):
        """delete"""
        try:
            self.context.manage_delObjects(subscribers)
            return None
        except Exception as e:
            return SUBSCRIBER_NOT_DELETED

    def approve(self, subscribers):
        """approve"""
        try:
            self._change_state("approve", subscribers)
            return None
        except Exception as e:
            return SUBSCRIBER_NOT_APPROVED

    def reject(self, subscribers):
        """reject"""
        try:
            self._change_state("reject", subscribers)
            return None
        except Exception as e:
            return SUBSCRIBER_NOT_REJECTED

    def _change_state(self, state, subscribers):
        """change state"""
        for subscriber in subscribers:
            elem = self.context.get(subscriber)
            api.content.transition(obj=elem, transition=state)

    def reply(self):

        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(
                self.request, plone.protect.interfaces.IDisableCSRFProtection
            )
        data = json_body(self.request)
        manipulation_type = data.get("manipulation_type", None)
        subscriberSelection = data.get("subscriberSelection", [])
        return_dict = {}
        error = None
        if manipulation_type and subscriberSelection:
            if manipulation_type == "delete":
                error = self.delete(subscriberSelection)
                return_dict = {"message": "Correctly deleted"}
            elif manipulation_type == "approve":
                error = self.approve(subscriberSelection)
                return_dict = {"message": "Correctly approved"}
            elif manipulation_type == "reject":
                error = self.reject(subscriberSelection)
                return_dict = {"message": "Correctly rejected"}

        if error is not None:
            self.request.response.setStatus(500)
            return {
                "error": {
                    "message": "There was an error handling your request"
                }
            }

        subscribers = api.content.find(
            context=self.context, portal_type="eea.meeting.subscriber"
        )

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
            alsoProvides(
                self.request, plone.protect.interfaces.IDisableCSRFProtection
            )
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
