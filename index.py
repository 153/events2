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
month_names = ["", "January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November",
             "December"]

def eventdb():
    """Load the events and return it as a 2D array of strings.

    events[] = [year, month, day, filename, title, comments]"""
    with open("data/list.txt", "r") as events:
        events = events.read().splitlines()
    events = sorted(events)
    for n, e in enumerate(events):
        e = e.split(">")
        events[n] = [e[0][:4], e[0][4:6], e[0][6:8], e[0], e[2], e[1]]
    return events

def month_events(month):
    """Return an HTML table of events in a given month."""
    
    events = eventdb()
    eventlist = [e for e in events if int(e[1]) == int(month)]
    table = ["<table><tr><th>date<th>title"]
    for e in eventlist:
        table.append(f"<tr><td>{e[1]}-{e[2]}<td><a href='/e/{e[3]}'>{e[4]}</a>")
    table.append("</table>")
    return "\n".join(table)
            
    
@index.route('/list/')
def event_index():
    """Show a table of monthly events in HTML."""
    with open("data/list.txt", "r") as entries:
        entries = entries.read().splitlines()
    entries = [e.split(">") for e in entries]
    entries = sorted(entries, key=lambda x: x[0])

    for n, e in enumerate(entries):
        when = f"{e[0][4:6]}-{e[0][6:8]}"
        entries[n].append(when)
        e[2] = f"<a href='/e/{e[0]}'>{e[2]}</a>"
    etable = ["<table><tr><th>date<th>title<th>guests"]
    etable.append("<tr><td colspan='3'><center><a href='/create/'>Create new!</a></center>")    
    for e in entries:
        etable.append("".join(["<tr><td>", "<td>".join([e[3], e[2], e[1]])]))
    etable.append("</table>")
    return u.html("".join(etable), "Event list")

def cal(mont=2):
    "For a given month, return a calendar as an HTML-formatted table."
    monts = str(mont).zfill(2) # get month as 0 padded string

    # Get the last day of the month... 
    last = calendar.monthrange(year, mont)[1]

    # Find the number of weeks in a month
    d1 = date(year, mont, 1)
    d2 = date(year, mont, last)
    weeks = (d2-d1).days//7
    
    # Get the first and last days of the month's days of the week.
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
    mon.append(f"<tr><th><a href='/calendar/{prev}'>&#171; {prev}</a>")
    mon.append(f"<th colspan='5'>{month_names[mont]} {year}</td>")
    mon.append(f"<th><a href='/calendar/{nex}'>{nex} &#187;</a>")    
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
    # Format the month based on its events:
    month_events(mont)
    return "".join(mon)

@index.route('/calendar/')
def currmonth():
    """Show the current month as a calendar with a list of events.""" 
    month = date.today().month
    return monthview(month)

@index.route('/calendar/<month>/')
def monthview(month):
    """Show a calendar for a given month and an HTML table of its events."""
    table = cal(int(month))
    events = eventdb()
    eventlist = [e[2] for e in events if int(e[1]) == int(month)]
    for e in eventlist:
        table = table.replace(f"<td>{e}",
                              f"<td class='event'>{e}")
    table = table.replace("<td> .", "<td class='null'>")
    table += ("<p><center><a href='/create/'>Create New Event</a></center>")
    elist = month_events(month)
    if "-" in elist:
       table += "<p>" + elist
    return u.html(table, f"Calendar: {year}/{month}")
