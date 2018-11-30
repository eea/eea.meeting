Changelog
=========


1.0 (unreleased)
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

  ... WIP ...

- Improve: subscribers view - add new fields.
  [GhitaB #82545]

- Fix: Display condition for register icon. Check the user is not already
  registered in registration method.
  [valipod]

- Improve: Adding missing condition for "No emails sent" msg.
= Improve: Back buttons and messages.
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
