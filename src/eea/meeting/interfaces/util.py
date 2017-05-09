# -*- coding: utf-8 -*-

import re
from zope.interface import Invalid

from Products.CMFDefault.exceptions import EmailAddressInvalid
from Products.CMFDefault.utils import checkEmailAddress

import plone.api as api

from eea.meeting import _


def validate_email(email):
    try:
        checkEmailAddress(email)
    except EmailAddressInvalid:
        raise EmailAddressInvalid(email)
    return True


def validate_userid(userid):
    user = api.user.get(userid=userid)
    if user:
        return True

    raise Invalid(_(u'User does not exist!'))


def cc_constraint(value):
    for idx, email in enumerate(value):
        idx += 1
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise Invalid(_(u"Invalid email address on line %d" % idx))

    return True
