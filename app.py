from flask import Flask, request
from index import index
import settings as s

_port = s._port

# configure Flask
app = Flask(__name__,
            static_url_path = "",
            static_folder = "static",)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# register blueprints 
app.register_blueprint(index)

# start the application 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=_port)
    print(request)

app.run()    
