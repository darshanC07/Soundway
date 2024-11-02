from flask import Flask, render_template, request
import requests
import json
import speech_recognition as sr
import threading

app = Flask(__name__)

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
    
if __name__ == "__main__":
    app.run(debug=True)