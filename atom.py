from datetime import datetime, timedelta
import settings as s
import utils as u
    
with open("templates/atom_entry.txt", "r") as atom_entry:
    atom_entry = atom_entry.read()
with open("templates/atom_feed.txt", "r") as atom_feed:
    atom_feed = atom_feed.read()
with open("locations.txt") as loc:
    loc = [L.split(" ") for L in loc.read().splitlines()]
loc = {L[0]: " ".join(L[1:]) for L in loc}

def feed():
    entries = ld()
    updated = entries[-1][1].strftime("%Y-%m-%dT%H:%M:%SZ")
    feed_head = atom_feed.format(s.self_url, updated)
    feed_out = [feed_head]
    for e in entries:
          feed_out.append(entry(e))
    feed_out.append("</feed>")
    return "\n".join(feed_out)

def entry(event):
    """Generate an Atom feed entry.
Input: filename, guests, title, location, description
Template takes URL, datetime, title, link
"""
    e = []
    desc = u.escape(f"Event at <a href='{s._url}{event[4]}'>" \
                    + f"{loc[event[4]]}</a><br>") + event[5]
    desc = desc.replace("&", "&amp;")
    e.append(s.self_url + "e/" + event[0])
    e.append(event[1].strftime("%Y-%m-%dT%H:%M:%SZ"))
    e.append(event[3])
    e.append(desc)
    return atom_entry.format(*e)

def ld():
    with open("data/list.txt", "r") as entries:
        entries = sorted(entries.read().splitlines())
    for n, e in enumerate(entries):
        e = e.split(">")
        e.insert(1, e[0][:-7] + "00")
        e[1] = datetime.strptime(e[1], "%Y%m%d%H%M")
        entries[n] = e
    return entries

def today():
    return None

def alarm():
    """List all events, beginning with the next [window of time] and
working backwards. Set the upcoming events period in global settings"""
    now = datetime.now()
    entries = ld()
    seconds = 60*60*4
    for e in entries:
        until = e[1] - now
        until = int(until.total_seconds())
        if (0 < until < seconds):
            print("\t!! event happening in the next 4 hours")
            print("\n".join([str(x) for x in e]))
        elif (0 > until):
            print("\t!! event already happened")
        else:
            print("\t!! event happening in more than 4 hours")
            print(e[1] - now, "\n", e)
#    entries = [int(e[0][:-9]) for e in ld()]
#    for e in entries:
#        print(e, now, e - now)
    return None

# 20220405, 20220223

alarm()
#print(feed())
