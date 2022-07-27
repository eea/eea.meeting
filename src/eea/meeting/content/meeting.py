""" Meeting """
from datetime import datetime
import pytz
import transaction
from eea.meeting.interfaces import IMeeting
from plone import api
from plone.dexterity.content import Container
from plone.dexterity.utils import createContentInContainer
from zope.interface import implementer
from AccessControl import getSecurityManager

@implementer(IMeeting)
class Meeting(Container):
    """ EEA Meeting content type"""

    def is_anonymous(self):
        """ Check user """
        return api.user.is_anonymous()

    def is_registered(self, uid=None):
        """ Check if user requested the registration

            Use subscriber_status() to see user's curent state:
            approved, new or rejected
        """
        if not uid:
            uid = api.user.get_current().getId()
        return uid in self.subscribers.subscriber_ids()

    def subscriber_status(self, uid=None):
        """ Return subscriber's status """
        if not uid:
            uid = api.user.get_current().getId()

        if self.is_registered(uid):
            subs = [x for x in self.get_subscribers() if x.userid == uid]
            if subs:
                return api.content.get_state(subs[0])

            return None

    def can_register(self):
        """ Can register? """
        is_open = self.registrations_open()
        if not is_open:
            return False
        return True

    def is_admin(self):
        """ Is meeting admin? """
        sm = getSecurityManager()
        return sm.checkPermission("EEA Meting: Admin Meeting", self)

    def is_webinar(self):
        """ Is webinar? """
        return self.meeting_type == 'webinar'

    def is_ended(self):
        """ Is meeting ended? """
        if datetime.now(pytz.UTC) < self.end:
            return False
        return True

    def registrations_open(self):
        """ Registrations are open if (ALL are TRUE):
                * users are allowed to register
                * current time is < end of meeting
                * (the number of approved participants is < max participants)
                  or (meeting still accepts registration when max is reached)

                (If constraint is set)
                * current time is not < start time for allowed registration
                * current time is not > end time for allowed registration
        """
        if self.allow_register:
            if self.allow_register_start is not None:
                if datetime.now() < self.allow_register_start:
                    return False

            if self.allow_register_end is not None:
                if datetime.now() > self.allow_register_end:
                    return False

        return (self.allow_register and
                (not self.is_ended()) and
                ((self.subscribers.approved_count() < self.max_participants) or
                 (self.max_participants == 0) or
                 (self.allow_register_above_max is True)))

    def get_subscribers(self):
        """ Return subscribers """
        return self.subscribers.get_subscribers()

    # def get_subscriber_roles_dict(self):
    #     """ Subscriber roles """
    #     try:
    #         # defined in eni.seis.content
    #         # vocab = self.portal_vocabularies.subscriber_roles
    #     except AttributeError:
    #         # ignore this feature if vocab is not defined
    #         return {}


    #     roles_dict = {}
    #     for key in vocab.keys():
    #         roles_dict[key] = vocab[key].title
    #     return roles_dict

    @property
    def human_readable_date(self):
        """ Return start date - end date in format:
            10 September - 1 October 2018
            3-5 August 2017

            Solves timezone problem - wrong start or end day
            self.start
                datetime.datetime(2020, 9, 21, 22, 0, tzinfo=<UTC>)
            self.start.astimezone(timezone)
                datetime.datetime(2020, 9, 22, 0, 0,
                tzinfo=<DstTzInfo 'Europe/Copenhagen' CEST+2:00:00 DST>)
        """
        timezone = pytz.timezone(self.timezone)
        # We use the timezone set for each item instead of website's one
        # site_timezone = pytz.timezone(default_timezone())
        # else the dates are wrong again. When an event is listed we
        # want to show the dates as saved, ignoring hours and timezone.
        start_date = self.start.astimezone(timezone)
        end_date = self.end.astimezone(timezone)
        start_day = start_date.day
        start_month = start_date.strftime("%B")
        end_day = end_date.day
        end_month = end_date.strftime("%B")

        if start_month == end_month:
            if start_day == end_day:
                return "%s %s" % (start_day, start_month)
            return "%s-%s %s" % (start_day, end_day, start_month)

        return "%s %s - %s %s" % (start_day, start_month, end_day, end_month)

    @property
    def human_readable_date2(self):
        """ Return start date - end date in format:
            ["Oct 08, 2019", "Oct 09, 2019"]

            used in events_listing as:
            Oct 08, 2019 to
            Oct 09, 2019
        """
        timezone = pytz.timezone(self.timezone)
        start_date = self.start.astimezone(timezone)
        end_date = self.end.astimezone(timezone)

        first_line = """{0} {1}, {2}""".format(
            start_date.strftime("%B")[:3],
            start_date.strftime("%d"),
            start_date.strftime("%Y")
        )

        second_line = """{0} {1}, {2}""".format(
            end_date.strftime("%B")[:3],
            end_date.strftime("%d"),
            end_date.strftime("%Y")
        )

        return [first_line, second_line]


def on_save(obj, evt):
    """ on save """
    # This triggers also on the container creation, not only on save props!
    subscribers = getattr(obj, 'subscribers', None)
    if subscribers:
        if subscribers.registrations_open():
            if api.content.get_state(subscribers) == 'closed':
                api.content.transition(obj=subscribers,
                                       transition='to_open')
        elif api.content.get_state(subscribers) == 'open':
            api.content.transition(obj=subscribers, transition='close')


def on_add(obj, evt):
    """ on add """
    create_subscribers(obj)

    create_emails(obj)

    create_folder_for_public_items(obj)

    create_folder_for_private_items(obj)


def create_subscribers(container):
    """ create subscribers """
    createContentInContainer(container, 'eea.meeting.subscribers',
                             title='Subscribers', id='subscribers')


def create_emails(container):
    """ create emails """
    createContentInContainer(container, 'eea.meeting.emails',
                             title='Emails', id='emails')


def create_folder_for_public_items(container):
    """ Create Public folder """
    obj = api.content.create(
        type='Folder', title='Public', container=container)
    api.content.transition(obj=obj, transition='publish')


def create_folder_for_private_items(container):
    """ Create Workspace """
    obj = api.content.create(
        type='eea.meeting.workspace', title='Workspace', container=container)
    api.content.transition(obj=obj, transition='publish')

    # Cut View permission for Anonymous user.
    # This will block direct access to files for anonymous users in workspace
    # context.
    obj.manage_permission('View', roles=['Authenticated', 'Manager', 'Owner'])
    transaction.commit()
