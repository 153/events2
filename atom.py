from datetime import datetime
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
        # filename, guests, title
        # -> fn, datetime, guests, title
        e = e.split(">")
        e.insert(1, e[0][:-7] + "00")
        e[1] = datetime.strptime(e[1], "%Y%m%d%H%M")
        entries[n] = e
    return entries

print(feed())
