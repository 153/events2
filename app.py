from flask import Flask, request
from index import index
from create import create
import settings as s

_port = s._port

# configure Flask
app = Flask(__name__,
            static_url_path = "",
            static_folder = "static",)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# register blueprints 
app.register_blueprint(index)
app.register_blueprint(create)

@app.route("/")
def hello():
    ret = ["<h1>Gikopoi events! in dev!!</h1>"]
    ret.append("source: <a href='//github.com/153/events2'>github/153/events2</a>")
    ret.append("<ul><li>")
    ret.append("<li>".join(["<a href='create'>create</a>",
                            "<a href='list'>list</a>",
                            "<a href='calendar'>calendar</a>"]))
    return "".join(ret)

# start the application 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=_port)
    print(request)

app.run(debug=True)    
