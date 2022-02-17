import calendar
import pandas as pd
from datetime import date, datetime, timedelta
from flask import Blueprint
from flask import request

import settings as s
index = Blueprint("index", __name__)

@index.route('/list/')
def event_index():
    with open("data/list.txt", "r") as entries:
        entries = entries.read().splitlines()
    entries = [e.split(">") for e in entries]
    entries = sorted(entries, key=lambda x: x[0])

    for n, e in enumerate(entries):
        when = f"{e[0][4:6]}-{e[0][6:8]}"
        entries[n].append(when)
    etable = ["<table><tr><th>date<th>title<th>guests"]
    for e in entries:
        etable.append("".join(["<tr><td>", "<td>".join([e[3], e[2], e[1]])]))
    etable.append("</table>")
    return "".join(etable)

def cal(mont=2):
    names = ["", "January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November",
             "December"]
    monts = str(mont).zfill(2) # get month as 0 padded string
    year = date.today().year
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
    prev = mont - 1
    nex = (mont + 1) % 12
    
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
    return "".join(mon)

@index.route('/calendar')
def currmonth():
    month = date.today().month
    return monthview(month)

@index.route('/calendar/<month>/')
def monthview(month):
    table = cal(int(month))
    return table

if __name__ == "__main__":
    for i in range(12):
        i += 1
        cal(i)
    

