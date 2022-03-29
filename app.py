#!/usr/bin/python3
from flask import Flask, request
from index import index
from create import create
from event import event
import settings as s
import utils as u

_port = s._port

# configure Flask
app = Flask(__name__,
            static_url_path = "",
            static_folder = "static",)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# register blueprints 
app.register_blueprint(index)
app.register_blueprint(create)
app.register_blueprint(event)

@app.route("/")
def hello():
    ret = []
    with open("html/index.html", "r") as index:
        index = index.read()
    return u.html(index, "gikopoi events")

# start the application 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=_port)
    print(request)

app.run(debug=True)    
