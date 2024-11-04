from flask import Flask, render_template, request, jsonify
import requests
import json
import speech_recognition as sr
import threading
from flask_cors import CORS
import pyrebase
from config import config

app = Flask(__name__)
CORS(app)

firebase = pyrebase.initialize_app(config)
db = firebase.database()


command = None

def voice():
    global command
    r = sr.Recognizer()
    # while True:
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-us")
            command = query.lower()
            print(command)
        except Exception as e:
            command = None

@app.route("/", methods= ["GET","POST"])
def map_view():
    global command
    if request.method == "POST":
        if request.form['microphone'] == 'on':
            print("clicked")
            voice()
            
    return render_template(template_name_or_list="mappls_map.html",command=command)

    # 16.62662018, 49.2125578
@app.route("/getSavedLoc", methods = ["GET"])
def getSavedLoc():
    count = 1
    data = db.child("savedLoc/").get().val()
    data.pop(0)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True,port=3000)