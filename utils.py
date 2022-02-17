with open("html/head.html", "r") as head:
    head = head.read()

def html(body, title="Events"):
    return head.format(body, title)

def locations():
    with open("locations.txt", "r") as locations:
        locations = locations.read().splitlines()
    for n, L in enumerate(locations):
        L = L.split(" ")
        locations[n] = [L[0], " ".join(L[1:])]
    ld = {L[0]: L[1] for L in locations}
    return ld
