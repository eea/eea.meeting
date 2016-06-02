# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s eea.meeting -t test_meeting.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src eea.meeting.testing.EEA_MEETING_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_meeting.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add an EEA Meeting
  Given a logged-in site administrator
    and an add meeting form
   When I type 'My EEA Meeting' into the title field
    and I submit the form
   Then a meeting with the title 'My EEA Meeting' has been created

Scenario: As a site administrator I can view a Meeting
  Given a logged-in site administrator
    and a meeting 'My EEA Meeting'
   When I go to the meeting view
   Then I can see the meeting title 'My EEA Meeting'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add meeting form
  Go To  ${PLONE_URL}/++add++EEAMeeting

a meeting 'My EEA Meeting'
  Create content  type=EEA Meeting  id=my-eea-meeting  title=My EEA Meeting


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the meeting view
  Go To  ${PLONE_URL}/my-meeting
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a meeting with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the meeting title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
