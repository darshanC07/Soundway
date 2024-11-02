from flask import Flask, render_template, request
import requests
import json
import speech_recognition as sr
import threading

app = Flask(__name__)

map_links = {
        "street" : "https://api.maptiler.com/maps/streets-v2/style.json?key=Gn9UKJFHAfBNJFkegmL4",
        "satellite" : "https://api.maptiler.com/maps/satellite/style.json?key=Gn9UKJFHAfBNJFkegmL4",
        "aquarelle" : "https://api.maptiler.com/maps/aquarelle/style.json?key=Gn9UKJFHAfBNJFkegmL4",
        "topography" : "https://api.maptiler.com/maps/topo-v2/style.json?key=Gn9UKJFHAfBNJFkegmL4",
        
}

map_type = "street"

def voice():
    global map_links,map_type
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
            
        if command != None:
            if "satellite" in command:
                map_type = "satellite"
            elif "street" in command:
                map_type = "street"
            elif "aquarelle" in command:
                map_type = "aquarelle"
            elif "topography" in command:
                map_type = "topography"
        else:
            map_type = "street"
            # elif "quit" in command:
            #     break
                
# threading.Thread(target=voice).start()

@app.route("/", methods= ["GET","POST"])
def map_view():
    global map_links,map_type 
    
    if request.method == "POST":
        if request.form['microphone'] == 'on':
            print("clicked")
            voice()
    
    #getting user's location by ip address
    loc = requests.get("https://api.maptiler.com/geolocation/ip.json?key=Gn9UKJFHAfBNJFkegmL4")
    loc_json = json.loads(loc.text)
    lat = loc_json["latitude"]
    long = loc_json["longitude"]
      
    map_link = map_links[map_type]   
    return render_template(template_name_or_list="map.html",lat = lat, long = long, map_link = map_link)

    # 16.62662018, 49.2125578
    
if __name__ == "__main__":
    app.run(debug=True)