import calendar
import os
from datetime import date, datetime, timedelta
import pandas as pd
from flask import Blueprint
from flask import request

import settings as s
import utils as u
index = Blueprint("index", __name__)

year = date.today().year
def eventdb():
    with open("data/list.txt", "r") as events:
        events = events.read().splitlines()
    events = sorted(events)
    for n, e in enumerate(events):
        e = e.split(">")
        events[n] = [e[0][:4], e[0][4:6], e[0][6:8], e[0], e[2], e[1]]
    return events

def month_events(month):
    events = eventdb()
    eventlist = [e for e in events if int(e[1]) == int(month)]
    table = ["<table><tr><th>date<th>title"]
    for e in eventlist:
        table.append(f"<tr><td>{e[1]}-{e[2]}<td><a href='/e/{e[3]}'>{e[4]}</a>")
    table.append("</table>")
    return "\n".join(table)
            
    
@index.route('/list/')
def event_index():
    with open("data/list.txt", "r") as entries:
        entries = entries.read().splitlines()
    entries = [e.split(">") for e in entries]
    entries = sorted(entries, key=lambda x: x[0])

    for n, e in enumerate(entries):
        when = f"{e[0][4:6]}-{e[0][6:8]}"
        entries[n].append(when)
        e[2] = f"<a href='/e/{e[0]}'>{e[2]}</a>"
    etable = ["<table><tr><th>date<th>title<th>guests"]
    for e in entries:
        etable.append("".join(["<tr><td>", "<td>".join([e[3], e[2], e[1]])]))
    etable.append("</table>")
    return u.html("".join(etable), "event list")

def cal(mont=2):
    names = ["", "January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November",
             "December"]
    monts = str(mont).zfill(2) # get month as 0 padded string
    last = calendar.monthrange(year, mont)[1]
    d1 = date(year, mont, 1)
    d2 = date(year, mont, last)
    weeks = (d2-d1).days//7
    start = pd.Timestamp(f'2022-{monts}-01').dayofweek
    end = pd.Timestamp(f'2022-{monts}-' + \
                      str(calendar.monthrange(2022, mont)[1])).dayofweek
    extra = 6 - end
    if (end == 0) or (start == 6):
        weeks += 1
    pos = [0,0]
    cnt = 0
    prev, nex = 1, 12
    if mont > 1:
        prev = mont - 1
    if mont < 12:
        nex = (mont + 1) % 13
    
    mon = ["<table>"]
    mon.append(f"<tr><td><a href='/calendar/{prev}'>&#171; {prev}</a>")
    mon.append(f"<th colspan='5'>{names[mont]} {year}</td>")
    mon.append(f"<td><a href='/calendar/{nex}'>{nex} &#187;</a>")    
    mon.append("<tr><th>Mon<th>Tue<th>Wed<th>Thu<th>Fri<th>Sat<th>Sun")
    
    while pos != [weeks, 6]:
        if pos[1] == 0:
            mon.append("\n<tr>")
        if pos[0] == 0:
            if pos[1] < start:
                mon.append("<td> .")
            else:
                cnt += 1
                mon.append("<td>" + str(cnt)\
                           .zfill(2))
        elif pos[0] == weeks and pos[1] > end:
            mon.append("<td> .")
        else:
            cnt += 1
            mon.append("<td>" + str(cnt)\
                       .zfill(2))
        pos = [pos[0], pos[1]+1]
        if pos[1] == 7:
            pos = [pos[0]+1, 0]
    if extra != 0:
        mon.append("<td> .")
    else:
        mon.append("<td>" + str(cnt+1))
    mon.append("</table>")
    month_events(mont)
    # monts = 
    return "".join(mon)

@index.route('/calendar/')
def currmonth():
    month = date.today().month
    return monthview(month)

@index.route('/calendar/<month>/')
def monthview(month):
    table = cal(int(month))
    events = eventdb()
    eventlist = [e[2] for e in events if int(e[1]) == int(month)]
    for e in eventlist:
        table = table.replace(f"<td>{e}",
                              f"<td class='event'>{e}")
    print(eventlist)
    table = table.replace("<td> .", "<td class='null'>")
    
    elist = month_events(month)
    if "-" in elist:
       table += "<p>" + elist
    return u.html(table, f"calendar: {year}/{month}")

@index.route("/e/<fn>")
def view_event(fn):
    files = os.listdir("data")
    print(files)
    files = [f for f in files if len(f.split(".")) == 3]
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
    
    return u.html(page, "Event")
