# events2
events2 is a rewrite of my old social calendar software, "events". It
uses Flask to deply a webserver that allows people to announce events
for Gikopoi (such as karaoke, radio shows, streamed video games, et al).

Registration is not required to create events, RSVP, or comment.

edit settings.py as needed; enter `python3 app.py` to start a server at
(default) port 3565 

Events can be viewed as a list or be represented on a calendar.

RSS feeds for the day & upcoming events will also be made available,
as to announce events easily to e.g. chatrooms, RSS reader apps, etc.
iCalendar also to come.

Developer chat: `#gikopoi` @ `irc.rizon.net`

static/moment.min.js (C) JS Foundation under MIT license
Source @ https://momentjs.com