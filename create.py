import os
from datetime import datetime
from flask import Blueprint
from flask import request
import settings as s
import utils as u

create = Blueprint("create", __name__)

dt = datetime.today()

# locations.txt -> locations [[code, name]]
with open("locations.txt", "r") as locations:
    locations = locations.read().splitlines()
for n, L in enumerate(locations):
    L = L.split(" ")
    locations[n] = [L[0], " ".join(L[1:])]
ld = {L[0]: L[1] for L in locations}


def date_check(y, m, d):
    """Ensure that a date is valid."""
    try:
        test = bool(datetime.strptime(f"{y}{m}{d}", "%Y%m%d"))
    except:
        test = False
    return test


def locmenu():
    """Build an HTML dropdown menu of Gikopoi rooms."""
    template = "<select name='loc'>\n"
    item = ' <option value="{0}">{1}</option>\n'
    for L in locations:
        template += item.format(L[0], L[1])
    template += "\n</select>"
    template = template.replace(f'"{s.room}"', f'"{s.room}" selected')
    return template

@create.route('/create/')
def page1():
    """Get information about an event on Gikopoi"""
    forms = {"month": "", "day": ""}
    for f in forms:
        with open(f"html/{f}.html", "r") as template:
            forms[f] = template.read()
    today = {"month": str(dt.month).zfill(2),
             "day": str(dt.day).zfill(2)}
    for x in today:
        forms[x] = forms[x].replace(today[x] +'"', today[x] + '" selected')
    with open("html/create1.html", "r") as message:
        message = message.read()
    message = message.format(forms["month"], forms["day"], locmenu())
    if s.debug:
        message = "<hr><h2 style='color:red'>Debug/lock mode active."
        "Event publishing disabled</h2><hr>" + message
    return u.html(message, "create (1/2)")


@create.route('/create/preview', methods=['POST'])
def page2():
    """Confirm details about an event on Gikopoi"""
    fields = ["title", "host", "loc", "desc",
              "year", "month", "day", "hour", "tz"]
    # dst may also be in fields
    event = {i: request.form[i] for i in fields}
    if not "dst" in request.form:
        event["dst"] = "0"
    else:
        event["dst"] = "1"
    if not event["host"]:
        event["host"] = "Anonymous"
    event["ymd"] = "".join([event[i] for i
                            in ["year", "month", "day", "hour"]])
    event["utc"] = u.offset(event["ymd"], event["tz"], event["dst"])
    event["fn"] = mkfilename(event["utc"]) + ".txt"
    with open("html/create2.html", "r") as page:
        page = page.read()
    page = eval(page)
    event2 = [f"<input type='hidden' name='{i}' value='{u.escape(event[i])}'>"
             for i in event if i != "desc"]
    event2.append(f"<textarea style='visibility:hidden' name='desc'>{event['desc']}</textarea>")
    for i in event2:
        page += i
    return u.html(page, "create (2/2)")


@create.route('/create/finish', methods=['POST'])
def page3():
    """Validate and publish details about an event on Gikopoi."""
    fields = ["title", "host", "loc", "dst",
              "year", "month", "day", "hour", "tz"]
    # dst removed
    event = {i: u.escape(request.form[i]) for i in fields}
    event["desc"] = request.form["desc"]
    if not date_check(event["year"], event["month"], event["day"]):
        return u.html("Invalid date.", "Error")
    event["desc"] = u.escape(event["desc"], 800, 1)
    event["ymd"] = "".join([event[i] for i in ["year", "month", "day", "hour"]])
    event["utc"] = u.offset(event["ymd"], event["tz"], event["dst"])    
    event["fn"] = mkfilename(event["utc"]) + ".txt"    
    writedb(event, s.debug)
    u.logger("CREATE", request.environ['HTTP_X_FORWARDED_FOR'],
             event["fn"], event["title"])
    page = u.redir(f"/e/{event['fn']}", 4) + "Go see " \
        + f"<a href='/e/{event['fn']}'>your event!</a>"
    return u.html(page, "Event published!")


def mkfilename(ymd):
    """Given year, month, day input, create a filename for an event."""
    files = os.listdir("data")
    cnt = len([i for i in files if ymd in i])
    return ".".join([ymd, str(cnt).zfill(2)])


def writedb(event, debug=0):
    """Update the list.txt with details about a new event."""
    # row 1: title
    # row 2: host, guest1, guest2
    # row 3: giko location name
    # row 4: description (<br> allowed)
    # row 5-: name, comment
    event["desc"] = event["desc"].replace("\r\n", "<br>")    
    entry = ">".join([event["fn"], "1", event["title"],
                      event["loc"], event["desc"]])
    if debug == 1:
        return
    with open("data/" + event["fn"], "w") as eventfile:
        eventfile.write("\n".join([event["title"], event["host"],
                                   event["loc"], event["desc"], ""]))
    with open("data/list.txt", "a") as index:
        index.write(entry + "\n")

