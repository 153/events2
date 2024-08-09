from datetime import date
import os
from flask import Blueprint
from flask import request
import settings as s
import utils as u

locations = u.locations()
event = Blueprint("event", __name__)

@event.route("/e/<fn>")
def view_event(fn):
    files = [f for f in os.listdir("data") if len(f.split(".")) == 3]
    if fn not in files:
        return(u.html("Sorry, event can't be found!", "404"))
    with open(f"data/{fn}", "r") as event:
        event = event.read().splitlines()
        # title, host, timezone, location, description
    ymd = "/".join([fn[:4], fn[4:6], fn[6:8]])
    hour = fn[8:10]
    mins = fn[10:12]
    places = u.locations()
    event[1] = event[1].split(">")
    event[1] = f"<b>{len(event[1])} guests</b>: {', '.join(event[1])}"
    event.insert(2, "&#127760; UTC (Universal time): " \
        + f"<br> &emsp;{ymd} @ {hour}:{mins}<br>" \
        + "<span onload='mydate' id='utc'>" \
        + f"{ymd.replace('/', '-')}T{hour}:{mins}:00Z</span>")
    beats = int(hour) + 1 % 23
    beats = ((3600 * beats) + (60 * int(mins))) / 86.4
    event[2] += "<br>&#128760; Internet time "
    event[2] += "<a href='//gwil.co/internet-time/'>(details)</a>"
    event[2] += "<br>&emsp;@{:.2f}".format(beats)
    event[3] = f"<a href='{s._url}{event[3]}'>{places[event[3]]}</a>"
    event[4] = event[4].replace("&lt;br&gt;", "<br>")
    comments = []
    if len(event) < 6:
        comments.append("<p>No comments yet.")        
        event.append(fn)
    else:
        with open("html/comment.html", "r") as template:
            template = template.read()
        comments.append("<p><table><th colspan=2>Newest comments first")
        for e in reversed(event[5:]):
            e = e.split("<>")
            comments.append(template.format(*e))
        comments.append("</table>")        
        event.insert(5, fn)
    with open("html/event.html", "r") as page:
        page = page.read().format(*event)
    with open('html/commentform.html', "r") as cform:
        cform = cform.read().format(*event)
    page += cform + "\n".join(comments)
        
    return u.html(page, f"Event: {event[0]}")

@event.route("/e/<fn>/rsvp", methods=['POST'])
def rsvp(fn):
    if s.debug:
        return "Debug mode active, can't rsvp yet."
    if "list" in fn:
        return str("!" + fn)
    name = u.escape(request.form["rsvp"], 20)
    if not name:
        return str(name)
    u.logger("RSVP", request.environ['HTTP_X_FORWARDED_FOR'], fn, name)    
    with open(f"data/{fn}", "r") as data:
        data = data.read().splitlines()
    data[1] += ">" + name
    data = "\n".join(data)
    with open(f"data/{fn}", "w") as update:
        update.write(data + "\n")
    with open("data/list.txt", "r") as entries:
        entries = entries.read().splitlines()
    entries = [e.split(">") for e in entries]
    for n, e in enumerate(entries):
        if e[0] == fn:            
            entries[n] = [e[0], str(int(e[1]) + 1), *e[2:]]
    entries = "\n".join([">".join(e) for e in entries])
    with open("data/list.txt", "w") as index:
        index.write(entries + "\n")
    return(u.html(f"<a href='/e/{fn}'>Return to event</a>" \
                  + u.redir(f"/e/{fn}", 3),
                  "You have RSVP'd"))

@event.route("/e/<fn>/comment", methods=['POST'])
def comment(fn):
    entries = os.listdir("data")
    entries.remove("list.txt")
    if s.debug:
        return "Debug mode active, can't comment yet."    
    if fn not in entries:
        return "Error"
    name = u.escape(request.form["name"], 20)
    msg = u.escape(request.form["comment"], 500, 1)
    if not name:
        name = "Anonymous"
    if not msg:
        return "needs a message"
    else:
        response = "<>".join([name, msg])
    u.logger("COMMENT", request.environ['HTTP_X_FORWARDED_FOR'], fn, msg)
    with open(f"data/{fn}", "a") as data:
        data.write(response + "\n")
    return u.html(f"<a href='/e/{fn}'>Return to event</a>" \
                  + u.redir(f"/e/{fn}", 3),
    "Comment posted",)
