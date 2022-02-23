from datetime import date
import os
from flask import Blueprint
from flask import request
import settings as s
import utils as u

locations = u.locations()
event = Blueprint("event", __name__)

entries = os.listdir("data")
entries.remove("list.txt")

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
    places = u.locations()
    event[1] = event[1].split(">")
    event[1] = f"<b>{len(event[1])} guests</b>: {', '.join(event[1])}"
    if " " in event[2]:
        event[2] = event[2].split(" ")[0]
    event[2] = f"{ymd} @ {hour}:00 ({event[2]})"
    event[3] = f"<a href='{s._url}{event[3]}'>{places[event[3]]}</a>"
    event[4] = event[4].replace("&lt;br&gt;", "<br>")
    comments = []
    if len(event) < 6:
        comments.append("<p>No comments yet.")        
        event.append(fn)
    else:
        with open("html/comment.html", "r") as template:
            template = template.read()
        comments.append("<p><table>")
        for e in event[5:]:
            e = e.split(">")
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
    print(request.form["rsvp"])
    name = u.escape(request.form["rsvp"], 12)
    if not name:
        return str(name)
    with open(f"data/{fn}", "r") as data:
        data = data.read().splitlines()
    data[1] += ">" + name
    data = "\n".join(data)
    with open(f"data/{fn}", "w") as update:
        update.write(data)
    return(u.html("Thanks", "Thanks"))

@event.route("/e/<fn>/comment", methods=['POST'])
def comment(fn):
    if s.debug:
        return "Debug mode active, can't comment yet."    
    if fn not in entries:
        return
    name = u.escape(request.form["name"], 12)
    msg = u.escape(request.form["comment"], 500, 1)
    if not name or not msg:
        return "<br>".join(name, msg)
    else:
        response = "\n" + ">".join([name, msg])
    with open(f"data/{fn}", "a") as data:
        data.write(response)
    return u.html("Thanks", "thanks")
