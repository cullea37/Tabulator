# app.py
# Required Imports
import os, sys
from flask import Flask, render_template, send_from_directory, request, url_for, redirect, flash, session, send_from_directory, send_file
import random
import pyrebase
import logging
import string
import magic
import re, time
# Initialize Flask App
app = Flask(__name__,static_url_path='', 
            static_folder='static',
            template_folder='templates')
# Initialize Firestore DB
config = {
    "apiKey": "AIzaSyBzd9SYf4VdRFuNZvAPc_f-Y6NQ1mOGu0Y",
    "authDomain": "tabulator-emckac.firebaseapp.com",
    "databaseURL": "https://tabulator-emckac-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "tabulator-emckac",
    "storageBucket": "tabulator-emckac.appspot.com",
    "messagingSenderId": "865324926937",
    "appId": "1:865324926937:web:aa625c7d2e63bfe2a23bc8"
  }
ALLOWED_EXTENSIONS = {'mp4'}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

path = app.root_path
sys.path.append(path + "/scripts/")
from DriverCode import DriverCode

def allowedFile(filename):
    try:
        if filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS:
            return True
    except:
        pass
    return False

@app.route('/')
def index():
    print(app.root_path, flush=False)
    return render_template("index.html")

@app.route('/', methods=['POST', 'GET'])
def uploadVideo():
    ######## Check Video is Valid and Upload to DB and Send to DriverCode #######
    file = request.files['video']
    if file != "" and allowedFile(file.filename) and file.content_type == "video/mp4":
        fileName = "".join(random.choice(string.ascii_letters) for _ in range(20))
        storage.child(fileName).put(file)
        DriverCode(file)
        with open(path+"/tab.txt", "r") as f: 
            content = f.read()
        video_filename = path + '/scripts/'
        print(video_filename, flush=False)

        return render_template("done.html", content=content)
    return render_template("index.html")

@app.route('/downloadTab', methods=['POST', 'GET'])
def downloadTabs():
    path = app.root_path
    with open(path+"/tab.txt", "w") as f: 
        tabs = str(request.form.get('tabs'))
        f.write(tabs)

    return send_file(path+"/tab.txt" , as_attachment=True)


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True, host='0.0.0.0', port=port)
