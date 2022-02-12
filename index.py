from flask import Blueprint
from flask import request

import settings as s
index = Blueprint("index", __name__)

@index.route('/list/')
def event_index():
    return ("hello :)")
