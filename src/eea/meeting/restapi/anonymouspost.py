from plone.restapi.services import Service
import plone.api as api
from eea.meeting.browser.views import add_subscriber
import plone.protect.interfaces
from zope.interface import alsoProvides
from plone.restapi.deserializer import json_body
from AccessControl import getSecurityManager
import string, random
from Acquisition import aq_parent
import json


class Register(Service):
    def __call__(self):
        if "IDisableCSRFProtection" in dir(plone.protect.interfaces):
            alsoProvides(self.request, plone.protect.interfaces.IDisableCSRFProtection)
        subscribers = aq_parent(self.context).get("subscribers")
        anonymous_registration_allowed = self.anonymous_registration_allowed()
        if not (anonymous_registration_allowed):
            self.request.response.setStatus(400)
            result = {
                "message": "Anonymous registration not allowed",
            }
            return result

        props = self.anonymous_registration_dict()
        if not (props):
            self.request.response.setStatus(400)
            result = {
                "message": "Error getting anonymous user data",
            }
            return result

        try:
            self.validate(
                subscribers,
                anonymous_id=props["id"],
            )
        except Exception as e:
            self.request.response.setStatus(400)
            result = {
                "message": str(e),
            }
            return result

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

    def validate(self, subscribers, anonymous_id=None):
        """validate"""
        if not subscribers:
            raise Exception("Can't find subscribers directory")
        if not self.context.can_register():
            raise Exception("Registration not allowed")
        if self.context.is_registered(uid=anonymous_id):
            raise Exception("User already registered")

    def anonymous_registration_allowed(self):
        eea_meeting = aq_parent(self.context)
        return eea_meeting.allow_anonymous_registration

    def get_body_data(self):
        data = json_body(self.request)
        return data

    def anonymous_registration_dict(self):
        try:
            data = self.get_body_data()
            anonymous_fullname = data.get("fullname")
            anonymous_email = data.get("email")
            uid = self.randomStringDigits()
            props = dict(
                title=anonymous_fullname,
                id=uid,
                userid=uid,
                email=anonymous_email,
                reimbursed=False,
                role="other",
                anonymous_extra_data=json.dumps(data),
            )
            return props
        except:
            return {}

    def randomStringDigits(self, stringLength=8):
        """Generate a random string of letters and digits"""
        lettersAndDigits = string.ascii_letters + string.digits
        return "".join(random.choice(lettersAndDigits) for i in range(stringLength))
