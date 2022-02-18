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
    places = u.locations()
    if " " in event[2]:
        event[2] = event[2].split(" ")[0]
    event[2] = f"{ymd} @ {hour}:00 ({event[2]})"
    event[3] = f"<a href='{s._url}{event[3]}'>{places[event[3]]}</a>"
    with open("html/event.html", "r") as page:
        page = page.read()
    event[4] = event[4].replace("&lt;br&gt;", "<br>")
    page = page.format(*event)
    with open('html/commentform.html', "r") as cform:
        cform = cform.read()
    page += cform
    
    
    
    return u.html(page, "Event")
