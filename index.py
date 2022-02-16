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
    print(entries)
    for n, e in enumerate(entries):
        when = f"{e[0][4:6]}-{e[0][6:8]}"
        entries[n].append(when)
    etable = ["<table><tr><th>date<th>title<th>guests"]
    for e in entries:
        etable.append("".join(["<tr><td>", "<td>".join([e[3], e[2], e[1]])]))
    return "".join(etable)


@index.route('/calendar')
def cal(mon=7):
    year = 2022
    last = calendar.monthrange(year, mon)[1]
    d1 = date(year, mon, 1)
    d2 = date(year, mon, last)
    weeks = (d2-d1).days//7
    start = pd.Timestamp('2022-07-01').dayofweek
    end = pd.Timestamp('2022-07-' + \
                      str(calendar.monthrange(2022, 7)[1]) ).dayofweek
    print(start, end, weeks)
#    weeks 
#    end += 1
    extra = 6 - end
    cnt = 0
    pos = [0,0]
    while pos != [weeks, 6]:
        if pos[1] == 0:
            print(pos[0]+1)
        if pos[0] == 0:
            if pos[1] < start:
                print(".")
            else:
                cnt += 1
                print(cnt)
        elif pos[0] == weeks and pos[1] > end:
            print(".")
        else:
            cnt += 1
            print(cnt)            
        pos = [pos[0], pos[1]+1]
        if pos[1] == 7:
            pos = [pos[0]+1, 0]
    if extra != 0:
        print(".")
    else:
        print("-")
    print(extra)

if __name__ == "__main__":
    cal()
