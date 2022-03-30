import settings as s
def show_ics(fn):
    with open(f"./data/{fn}", "r") as data:
        data = data.read().splitlines()
    with open("ics.txt", "r") as temp:
        temp = temp.read()
    chars = {"&lt;":"<", "&gt;": ">",
             "&apos;":"'", "&quot;": "\"",
             "<br>": "\\n", ",": "\,"}
    e = {"fn":fn, "iso":0, "title":0,
         "host":0, "desc":0, "loc":0}
    e["iso"] = f"{fn[:8]}T{fn[8:10]}0000Z"
    e["title"] = data[0].replace(",", "\,")
    e["host"] = data[1].split(">")[0].replace(",", "\,")
    e["desc"] = data[4]
    for c in chars:
        if c in e["desc"]:
            e["desc"] = e["desc"].replace(c, chars[c])
    e["loc"] = data[3]
    print(e)
    print(eval(f'f"""{temp}"""'))

show_ics("2022033123.00.txt")
show_ics("2022042018.00.txt")
