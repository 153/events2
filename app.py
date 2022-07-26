#!/usr/bin/python3
from flask import Flask, request
from index import index
from create import create
from event import event
from ical import ical
from atom import atom
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
app.register_blueprint(ical)
app.register_blueprint(atom)

@app.route("/")
def hello():
    ret = []
    with open("html/index.html", "r") as index:
        index = index.read()
    return u.html(index, "gikopoi events")

# start the application 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=_port)
    # request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

app.run(debug=True)    
