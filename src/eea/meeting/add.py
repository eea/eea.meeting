from plone import api
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes


def handler(obj, evt):
    aspect = ISelectableConstrainTypes(obj)
    import pdb; pdb.set_trace()
    create_subscribers(obj)


def create_subscribers(container):
    api.content.create(
        type='Subscribers',
        title='Subscribers',
        id='subscribers',
        container=container)
