from datetime import datetime

def feed():
    return None

def entry():
    # input: fn, datetime, guests, title
    # title, url, datetime, location, text, site_url 
    return None

def ld():
    with open("data/list.txt", "r") as entries:
        entries = entries.read().splitlines()
    for n, e in enumerate(entries):
        # filename, guests, title
        # -> fn, datetime, guests, title
        e = e.split(">")
        e.insert(1, e[0][:-7] + "00")
        e[1] = datetime.strptime(e[1], "%Y%m%d%H%M")
        entries[n] = e
    return entries

print(ld())
