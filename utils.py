import time
import flask
from datetime import datetime
from datetime import timedelta

with open("html/head.html", "r") as head:
    head = head.read()

def html(body, title="Events"):
    return head.format(body, title)

def redir(loc, secs=0):
    return f"<meta http-equiv='refresh' content='{secs};url={loc}'>"

def locations():
    with open("locations.txt", "r") as locations:
        locations = locations.read().splitlines()
    for n, L in enumerate(locations):
        L = L.split(" ")
        locations[n] = [L[0], " ".join(L[1:])]
    ld = {L[0]: L[1] for L in locations}
    return ld

def escape(text, maxlen=0, newlines=0):
    text = text.strip()
    keys = {"<": "&lt;", ">": "&gt;",
            "'": "&apos;", "\"": "&quot;"}
    for key in keys:
        if key in text:
            text = text.replace(key, keys[key])
#    text = flask.escape(text)
    if not newlines:
        text = text.replace("\r\n", "")
    else:
        text = text.replace("\r\n", "<br>")
    if maxlen:
        text = text[:maxlen]
    return text

def offset(ymdh, tz, dst=0):
    dformat = "%Y%m%d%H%M"
    event_dt = datetime.strptime(ymdh, dformat)
    tz = tz[:3]
    if tz[0] not in ["+", "-"]:
        return False
    
    tz = int(tz)
    tz += int(dst)
    adjust = event_dt - timedelta(hours=int(tz))
    adjust = adjust.strftime("%Y%m%d%H%M")
    return adjust

def logger(event, ip, fn, content):
    now = str(int(time.time()))
    entry = " ".join([now, event, ip, fn, content])
    with open("log.txt", "a") as log:
        log.write(entry + "\n")
    
if __name__ == "__main__":
    tests = ["<test", "'test\r\n<"]
    for t in tests:
        print(escape(t, 20, 1))
