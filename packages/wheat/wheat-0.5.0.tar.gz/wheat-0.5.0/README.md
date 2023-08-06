# Wheat #

A concise and fast CLI to log hours in Harvest.

## Managing Projects ##

Wheat keeps a "projects" file somewhere that it stores task information in. Users can set tasks as active/not active at will. Whatever tasks are present in the task file are shown each time the user is asked to do anything regarding tasks.

## Commands ##

auth: Authenticate with Harvest by providing a personal access token and account id.

projects:
    view: Displays your Current Projects and Tasks.
    activate: Set a Project or Task as active.
    sleep: Set a Project or Task as inactive.

log:
    day: Logs a day's hours.
    week: Logs a week's hours.
    month: Logs a month's hours.

Note: For any log command, pass the -c / --calendar flag to include hours for events directly from your calendar.

view:
    week: View a week's logged hours.
    month: View a month's logged hours.

distribute:
    week: Distribute a project's hours evenly across a week.
    month: Distribute a project's hours evenly across a month.

meetings:
    next: Displays your next meeting.
    today: Displays today's meetings.
    join: Joins a meeting's video chat if a link is provided.
        Supports <c1>Zoom</c1> and <c1>Google Meets</c1>.
            * Takes Meeting ID as an argument. If none is provided, joins the next meeting on the calendar, if it can.

Note: Meetings commands require you to have logged into your Google account, and will use events from your google calendar.
