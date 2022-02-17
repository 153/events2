
with open("html/head.html", "r") as head:
    head = head.read()

def html(body, title="Events"):
    return head.format(body, title)
