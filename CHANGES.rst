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

TODO: continue with:
https://github.com/eea/eea.meeting/commits/master?after=8a252a717c8a1e3158fb00ac86268f8a8984a9d9+34
Commits on Oct 10, 2017

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
