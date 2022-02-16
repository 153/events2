from flask import Blueprint
from flask import request

import settings as s
index = Blueprint("index", __name__)

@index.route('/list/')
def event_index():
    with open("data/list.txt", "r") as entries:
        entries = entries.read().splitlines()
    entries = [e.split(">") for e in entries]
    for n, e in enumerate(entries):
        when = f"{e[0][4:6]}-{e[0][6:8]}"
        entries[n].append(when)
    print(entries)
    etable = ["<table><tr><th>date<th>title<th>guests"]
    for e in entries:
        etable.append("".join(["<tr><td>", "<td>".join([e[3], e[2], e[1]])]))
    return "".join(etable)
