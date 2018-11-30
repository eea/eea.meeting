Changelog
=========


1.1.dev0 (unreleased)
---------------------


1.0 (2018-12-01)
----------------
- Feature: Workspace (a custom container to be added to meeting when you have
  items to be accessed only by meeting approved subscribers.)
- Fix: show approve / reject subscribers btns only if the meeting is not ended.
  [GhitaB #99955]

- Feature: Possibility to define a time period for meeting regitration.
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

- Feature: webminar (get rid of map in meeting view, simplify edit form).
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
