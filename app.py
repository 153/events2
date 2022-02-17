from flask import Flask, request
from index import index
from create import create
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

@app.route("/")
def hello():
    ret = []
    ret.append("source: <a href='//github.com/153/events2'>github/153/events2</a><p>")
    ret.append("<center><table><tr>")
    ret.append("<td><a href='/calendar'><img src='/cal.png'></a>")    
    ret.append("<td><a href='/create'><img src='/create.png'></a>")
    ret.append("<td><a href='/list'><img src='/view.png'></a>")
    ret.append("<tr><th><a href='/calendar'>calendar</a>")
    ret.append("<th><a href='/create'>create</a>")
    ret.append("<th><a href='/list'>index</a>")
    ret.append("</table></center>")
    return u.html("".join(ret), "gikopoi events")

# start the application 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=_port)
    print(request)

app.run(debug=True)    
