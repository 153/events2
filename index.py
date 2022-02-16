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
    etable.append("</table><pre>" + str("="*26) + cal() + "</pre>")
    return "".join(etable)


@index.route('/calendar')
def cal(mont=2):
    monts = str(mont).zfill(2)
    year = 2022
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
    mon = []
    pos = [0,0]
    cnt = 0
    while pos != [weeks, 6]:
        if pos[1] == 0:
            mon.append(f"\n {pos[0]+1} -|")
        if pos[0] == 0:
            if pos[1] < start:
                mon.append(" .")
            else:
                cnt += 1
                mon.append(str(cnt).zfill(2))
        elif pos[0] == weeks and pos[1] > end:
            mon.append(" .")
        else:
            cnt += 1
            mon.append(str(cnt).zfill(2))
        pos = [pos[0], pos[1]+1]
        if pos[1] == 7:
            pos = [pos[0]+1, 0]
    if extra != 0:
        mon.append(" .")
    else:
        mon.append(str(cnt+1))
    print("\n\nmonth: ", mont)
    print("==========================")
    print("W   |  M  T  W  R  F  S  S")
    print(" ".join(mon))
    return " ".join(mon)

if __name__ == "__main__":
    for i in range(12):
        i += 1
        cal(i)
    

