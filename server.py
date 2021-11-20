# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH||
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = "Content-Type"

@app.route("/")
@cross_origin()
def hello_world():
  return "Hello, World!"


# #### EVENTS ####
# @app.route("/events", methods=["POST"])
# @cross_origin()
# def events():
#   if request.method != "POST": return "Bad Request", 400
#   try: