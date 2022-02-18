import os
from flask import Blueprint
from flask import request
from flask import escape
import settings as s
import utils as u

import datetime
create = Blueprint("create", __name__)

dt = datetime.datetime.today()

# locations.txt -> locations [[code, name]]
with open("locations.txt", "r") as locations:
    locations = locations.read().splitlines()
for n, L in enumerate(locations):
    L = L.split(" ")
    locations[n] = [L[0], " ".join(L[1:])]
ld = {L[0]: L[1] for L in locations}

def locmenu():
    template = "<select name='loc'>\n"
    item = ' <option value="{0}">{1}</option>\n'
    for L in locations:
        template += item.format(L[0], L[1])
    template += "\n</select>"
    template = template.replace(f'"{s.room}"', f'"{s.room}" selected')
    return template

@create.route('/create/')
def page1():
    forms = {"month":"", "day":""}
    for f in forms:
        with open(f"html/{f}.html", "r") as template:
            forms[f] = template.read()
    today = {"month": str(dt.month).zfill(2),
             "day": str(dt.day).zfill(2)}
    for x in today:
        today[x] = f'"{today[x]}"'
        forms[x] = forms[x].replace(today[x], today[x] + " selected")
    with open("html/create1.html", "r") as create1:
        create1 = create1.read()
    create1 = create1.format(forms["month"], forms["day"], locmenu())
    return u.html(create1, "create (1/3)")

@create.route('/create/next', methods=['POST'])
def page2():
    event_d = [request.form[n] for n in ["year", "month", "day", "hour"]]
    fields = ["title", "loc", "year", "month", "day", "hour", "tz"]
    loc = request.form["loc"]
    with open("html/create2.html", "r") as page:
        page = page.read()
    message = eval(page)
    print(fields)
    for i in fields:
        print(i)
        print(request.form[i])
    print([request.form[i] for i in fields])
    for i in fields:
        message += f"<input type='hidden' name='{i}' value='{request.form[i]}'>"
        print(i, request.form[i])
    if "dst" in request.form:
        message += "<input type='hidden' name='dst' value='1'>"
    else:
        message += "<input type='hidden' name='dst' value='0'>"
    message += "</form>"
    return u.html(message, "create (2/3)")

@create.route('/create/preview', methods=['POST'])
def page3():
    fields = ["title", "host", "loc", "desc",
              "year", "month", "day", "hour", "tz", "dst"]
    event = {i: request.form[i] for i in fields}
    if not event["host"]:
        event["host"] = "Anonymous"    
    event["ymd"] = "".join([event[i] for i in ["year", "month", "day", "hour"]])
    event["fn"] = mkfilename(event["ymd"]) + ".txt"
    with open("html/create3.html", "r") as page:
        page = page.read()
    page = eval(page)
    for i in event:
        page += f"<input type='hidden' name='{i}' value='{event[i]}'>"
    return u.html(page, "create (3/3)")

@create.route('/create/finish', methods=['POST'])
def page4():
    fields = ["title", "host", "loc", "desc",
              "year", "month", "day", "hour", "tz", "dst"]
    event = {i: escape(request.form[i]) for i in fields}
    event["ymd"] = "".join([event[i] for i in ["year", "month", "day", "hour"]])
    event["fn"] = mkfilename(event["ymd"]) + ".txt"    
    writedb(event, s.debug)
    return request.form

def mkfilename(ymd):
    print(ymd)
    files = os.listdir("data")
    cnt = len([i for i in files if ymd in i])
    return ".".join([ymd, str(cnt).zfill(2)])

def writedb(event, debug=0):
    entry = ">".join([event["fn"], "1", event["title"]])
    if debug == 1:
        return
    event["desc"] = event["desc"].replace("\r\n", "<br>")\
        
    with open("data/" + event["fn"], "w") as eventfile:
        eventfile.write("\n".join([event["title"], event["host"],
                                   event["tz"] + " " + event["dst"],
                                   event["loc"], event["desc"], ""]))
    with open("data/list.txt", "a") as index:
        index.write(entry + "\n")
    print("entry")
    
# row 1: title
# row 2: host, guest1, guest2
# row 3: giko location name
# row 4: description (<br> allowed)
# row 5-: name, comment
