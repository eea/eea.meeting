Changelog
=========

2.0a1+cs.13 (2022-10-26)
------------------------

- pin lower version [Mikel Larreategi <mlarreategi@codesyntax.com>]

-  [Mikel Larreategi <mlarreategi@codesyntax.com>]

- [ci skip] [Mikel Larreategi <mlarreategi@codesyntax.com>]



2.0a1+cs.12 (2022-10-24)
------------------------

- fill the session with the data [Mikel Larreategi <mlarreategi@codesyntax.com>]

-  [Mikel Larreategi <mlarreategi@codesyntax.com>]

- [ci skip] [Mikel Larreategi <mlarreategi@codesyntax.com>]



2.0a1+cs.11 (2022-09-13)
------------------------

- fix i18n translation domain [Mikel Larreategi <mlarreategi@codesyntax.com>]

-  [Mikel Larreategi <mlarreategi@codesyntax.com>]

- [ci skip] [Mikel Larreategi <mlarreategi@codesyntax.com>]



2.0a1+cs.10 (2022-09-05)
------------------------

- moved to our custom product clms.addon due to add more customizations [ionlizarazu <ilizarazu@codesyntax.com>]

-  [Mikel Larreategi <mlarreategi@codesyntax.com>]

- [ci skip] [Mikel Larreategi <mlarreategi@codesyntax.com>]



2.0a1+cs.9 (2022-08-04)
-----------------------

- Nothing changed yet.


2.0a1+cs.8 (2022-07-27)
-----------------------

- Nothing changed yet.


2.0a1+cs.7 (2022-07-19)
-----------------------

- Update changelog [Mikel Larreategi <mlarreategi@codesyntax.com>]

- improve default message [Mikel Larreategi <mlarreategi@codesyntax.com>]

-  [Mikel Larreategi <mlarreategi@codesyntax.com>]

- [ci skip] [Mikel Larreategi <mlarreategi@codesyntax.com>]


-  [Mikel Larreategi <mlarreategi@codesyntax.com>]

- [ci skip] [Mikel Larreategi <mlarreategi@codesyntax.com>]



2.0a1+cs.6 (2022-07-14)
-----------------------

- formatting [Mikel Larreategi <mlarreategi@codesyntax.com>]

- inhering from Serializer for Folderish [Mikel Larreategi <mlarreategi@codesyntax.com>]

-  [Mikel Larreategi <mlarreategi@codesyntax.com>]

- [ci skip] [Mikel Larreategi <mlarreategi@codesyntax.com>]



2.0a1+cs.5 (2022-07-07)
-----------------------

- require location and remove invariant [Mikel Larreategi <mlarreategi@codesyntax.com>]

- adjust required fields and default values [Mikel Larreategi <mlarreategi@codesyntax.com>]

-  [Mikel Larreategi <mlarreategi@codesyntax.com>]

- [ci skip] [Mikel Larreategi <mlarreategi@codesyntax.com>]



2.0a1+cs.4 (2022-01-27)
-----------------------

- anonymous form extra information [ionlizarazu <ilizarazu@codesyntax.com>]

- check if we have an email before creating a subscriber. If not, send the error [ionlizarazu <ilizarazu@codesyntax.com>]

- check if we have received fullname and email in the post [ionlizarazu <ilizarazu@codesyntax.com>]

- add schema [ionlizarazu <ilizarazu@codesyntax.com>]

- test if we have a receiver before creating the email element [ionlizarazu <ilizarazu@codesyntax.com>]

- add correctly the receiver at mail creation [ionlizarazu <ilizarazu@codesyntax.com>]

- add grandparent condition to create correctly the vocabulary [ionlizarazu <ilizarazu@codesyntax.com>]

- remove anonymousForm schema [ionlizarazu <ilizarazu@codesyntax.com>]

- reorganize anonymous registration responses [ionlizarazu <ilizarazu@codesyntax.com>]

- get current meeting subscribers after post [ionlizarazu <ilizarazu@codesyntax.com>]

------------------
- Improve: add Jenkins, improve code.
  [valentinab25, GhitaB #116841]

1.3.4 (2020-07-13)
------------------
- Fix: Show location as 'Webinar' in email notifications in case of webinars.
  [GhitaB #119569]

1.3.3 (2020-05-11)
------------------
- Fix: wrong order of countries in meeting view.
  [GhitaB #116290]

1.3.2 (2020-04-23)
------------------
- Fix: Remove featured options. (Tags to be used.)
  [GhitaB #116290]

1.3.1 (2020-04-13)
------------------
- Feature: Add secondary featured option for meeting item.
  [GhitaB #116290]

1.3.0 (2020-02-20)
------------------
- Feature: Add is_featured option for meeting item.
  [GhitaB #114456]

1.2.9 (2019-11-06)
------------------
- Feature: Add option to allow registration when number of participants is
  reached.
  [GhitaB #110772]

1.2.8 (2019-10-03)
------------------
- Improve: add more options for entries per page in subscribers datatable.
  Solves exporting as a single xls in case of many participants registered.
  [GhitaB #109799]

1.2.7 (2019-02-25)
------------------
- Improve: Add a new human readable date format, to be used in events_listing.
  [GhitaB #103043]

1.2.6 (2019-02-21)
------------------
- Improve: Add meeting_contact_name string substitution, available in emails.
- Improve: Add meeting_when string substitution on approve participant.
- Improve: Add subscriber_userid string substitution on approve participant.
- Improve: Add When and Where string substitutions on register participant.
  [GhitaB #102958]

1.2.5 (2019-02-20)
------------------
- Improve: Add min and max values for From and To fields in meeting edit form.
  [GhitaB #97529]

1.2.4 (2019-02-13)
------------------
- Fix: Cut View permission for Anonymous users in Workspace context.
  [GhitaB #101957]
- Fix: Prevent errors & sentry logs - redirect to meeting view and show an
  info message in case of unauthorised access of restricted content.
  [GhitaB #101957]

1.2.3 (2019-02-01)
------------------
- Improve: in case of webinar, disable E-pass field in meeting edit form.
  [GhitaB #97529]
- Fix: typo webminar -> webinar. Old items: solved. Clean code.
  [GhitaB #97529]

1.2.2 (2018-12-17)
------------------
- Improve: Update text for hide additional materials.
- Fix: typo webminar -> webinar.
- Fix: Hide private items in meeting view if no access rights.
  [GhitaB #97529]

1.2.1 (2018-12-11)
------------------
- Improve: create public folder and workspace on meeting item created.
- Improve: items listing in meeting view.
  [GhitaB #97529]

1.2 (2018-12-07)
----------------
- Improve: add request_data_deletion field in subscriber schema.
  [GhitaB #96598]

- Improve: add get meeting contents method in meeting view.
- Feature: add get meeting contents by case (to include public vs workspace
  related items).
  [GhitaB #97529]

1.1 (2018-12-05)
----------------
- Fix: add Document (Page) as addable content type to workspace.
- Fix: workspace folders to be listed in files listing of meeting view.
- Improve: items access rules by adding the view @@current_user_has_access.
  [GhitaB #97529]

1.0 (2018-12-01)
----------------
- Feature: Workspace (a custom container to be added to meeting when you have
  items to be accessed only by meeting approved subscribers.)
- Fix: show approve / reject subscribers btns only if the meeting is not ended.
  [GhitaB #99955]

- Feature: Possibility to define a time period for meeting registration.
  (From and To fields to be used when Allow registration is checked.)
  [GhitaB #99956]

- Feature: Add content rule to send email on subscriber rejection. Update email
  archive.
  [GhitaB #99957]

- Improve: improve fields texts (ex: clarify restrict_content_access field is
  used only to hide the contents in meeting view.)
- Fix: bug in subscriber status.
- Feature: add email_type in Mail arhive (Registration, Approval, Rejection).
- Improve: mail archive by adding direct link on each email in order to easily
  open it.
- Fix: responsivity of subscribers table.
  [GhitaB #97529]

- Fix: wrong start and end dates (using the self.timezone).
  [GhitaB #92650]

- Feature: webinar (get rid of map in meeting view, simplify edit form).
  [GhitaB #92256]

- Improve: editing participants - edit link in subscribers table.
  [GhitaB #92249]

- Improve: View url on subscribers in table.
  [GhitaB #88609]

- Improve: table of emails in mails archive. Custom email view. Fix sender and
  recipients.
  [GhitaB #88594]

- Fix: error on approve participant.
  [GhitaB #88167]

- Improve: email archive export function.
  [irina-botez]

- Fix: email notification / archive to work for both cases (register, approve).
  [GhitaB #88096]

- Improve: export email archive as .xlsx.
  [irina-botez]

- Fix: Return the actual user id instead of the Subscriber object id, which
  can get url normalized.
  [david-batranu #87630]

- Improve: Add meeting_level (similar with event_level) - display it in
  meeting view.
  [GhitaB #86208]

- Improve: Add new register fields to subscriber listing Position, Address.
  [irina-botez]

- Improve: content rules for sending emails and save them to archive.
  Code cleanup.
  [irina-botez]

- Fix: unicode error in subscriber.
  [david-batranu]

- Fix: UnicodeEncodeError in save_email_approved.
  [GhitaB]

- Improve: Add 2 new table classes for TinyMCE editor.
- Improve: Add City field to subscriber listing.
  [irina-botez]

- Feature: Added custom content rule action. Emails will be added to email
  archive after content rule is triggered.
  [irina-botez]

- Improve: subscribers + new StringSub: Display buttons and checkboxes on
  subscribers form only if the user has edit rights. Add meeting_url
  StringSubstitution. Fix subscriber name StringSubstitution.
- Fix: CSV download and checkboxes.
- Improve: buttons style.
- Improve: XLS Export for Subscribers
- Improve: Validate user id when adding subscriber.
- Improve: Subscribers listing by adding add/approve/deny/delete/sort/filter/
  pagination.
- Feature: content rule for new event, custom event for new subscribers.
- Fix: Remove reg. form on index. Instead go to ./register. The page is
  created in eni.seis.content. This package should implement a generic one!
- Feature: add approval email template.
- Feature: Support for new fields for subscribers. Support custom registration
  views.
  [david-batranu #83535]

- Fix: Hide all register form if login required in meeting index.
- Fix: reimbursed and role values in emails table.
- Fix: Make possible approving subscribers in the end date of a meeting.
  [GhitaB #83535]

- Fix: login redirect issue. Now when an anonymous wants to register for a
  meeting, after login will be redirected back to the meeting page.
  [irina-botez]

- Improve: Show vocabulary values instead of keys for subscriber role in
  subscribers. Use no, yes values for reimbused field. Remove Send email
  button (the emails are sent automatically now). Fix values in Email archive
  table. Save email notification in Emails archive on approving participants.
  Fix emails table when no emails. Import workflows to update guard
  transitions. Transition guard expression for subscriber (based on meeting
  ending date).
  [GhitaB #83535]

- Improve: code cleanup. Fix Microsoft Excel warning, update Excel export
  function. Add new fields to excel export.
  [irina-botez]

- Improve: Register form in meeting index. Save values for reimbursed and role.
  Use subscriber_roles vocabulary.  Add fields reimbursed and role for
  eea.meeting.subscriber.
  [GhitaB #83535]

- Improve: Add suplimentary fields to email archive
  [irina-botez]

- Improve: Add vars used for content rule (subscriber -> approved).
  [GhitaB #83535]

- Improve: subscribers view - add new fields.
  [GhitaB #82545]

- Fix: Display condition for register icon. Check the user is not already
  registered in registration method.
  [valipod]

- Improve: Adding missing condition for "No emails sent" msg.
- Improve: Back buttons and messages.
- Fix: View and email fixes.
- Improve: Restructuring interfaces and vocabularies.
- Improve: Adding dependency to geolocationbehavior.
  [david-batranu]

- Improve: Move meeting_index code from eni.seis.content override.
- Improve: Meeting view - single column layout.
  [GhitaB]

- Improve: forms, add hosting_organisation field.
  [tiberiuichim #71641]

- Fix: Meeting index template.
  [tiberiuichim]

- Fix: export of column names within email export excel
  [ichim-david ]

- Improve: meeting view, register user, add option: Restrict user access to
  meeting content.
  [melish]

- Feature: content rules to send emails. Mail archive, Excel export.
  New content content types: eea.meeting.email, eea.meeting.emails. Custom
  workflow for emails. User search.
  [irina-botez]

- Initial release. Content types, views, permissions, templates, basic
  functionality.
  [valipod]
