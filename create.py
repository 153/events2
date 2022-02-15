from flask import Blueprint
from flask import request

import settings as s
create = Blueprint("create", __name__)

# locations.txt -> locations [[code, name]]
with open("locations.txt", "r") as locations:
    locations = locations.read().splitlines()
for n, L in enumerate(locations):
    L = L.split(" ")
    locations[n] = [L[0], " ".join(L[1:])]
ld = {L[0]: L[1] for L in locations}

def mkmenu():
    template = "<select name='loc'>\n"
    item = " <option value='{0}'>{1}</option>\n"
    for L in locations:
        template += item.format(L[0], L[1])
    template += "\n</select>"
    return template

@create.route('/create/')
def page1():
    with open("html/create1.html", "r") as create1:
        create1 = create1.read()
    create1 = create1.format(mkmenu())
    
    return create1

@create.route('/create/next', methods=['POST'])
def page2():
    event_d = [request.form[n] for n in ["year", "month", "day", "hour"]]
    print(request.form["title"])
    print("{0}-{1}-{2} @ {3}".format(*event_d))
    print("http://", request.form["loc"], "/////", ld[request.form["loc"]])
    return request.form


# row 1: title
# row 2: host, guest1, guest2
# row 3: giko location name
# row 4: description (<br> allowed)
# row 5-: name, comment
