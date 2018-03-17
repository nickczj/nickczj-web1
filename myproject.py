from flask import Flask, render_template, send_from_directory, request
import requests
import threading
import logging
import urllib.request
import os
import subprocess
import datetime

app = Flask(__name__, static_folder='static')

logging.basicConfig(level=logging.DEBUG)
file_handler = logging.FileHandler('flask.log')
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)


API_KEY = "37fdVwafhb4HlDIIAgFJ6HbIeEk9qdanfQvxkTnQ"
OLD_API_KEY = "7UoReKEbxnGRMqwkVb9IBvhBmzCtpYdAtPFbnG90"

header, date, explanation, title, url = "", "", "", "", ""
images, max_date = [], ""


def get_apod_pics():
    app.logger.info(datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y") + " getting apod data")
    global header, date, explanation, title, url
    try:
        header = "Take a moment and soak in the wonders of space."
        response = requests.get("https://api.nasa.gov/planetary/apod?api_key={}".format(API_KEY))
        data = response.json()
        date = data['date'] + ": NASA's Astronomy Picture of the Day"
        explanation = data['explanation']
        title = data['title']
        link = data['url']
        urllib.request.urlretrieve(link, "static/images/apod.jpg")
        if 'jpg' in data['url']:
            url = "../static/images/apod.jpg"
        else:
            url = data['url']
        bash_command = "convert ../static/images/apod.jpg -sampling-factor 4:2:0 -strip -quality 85 -interlace JPEG" \
                       " -colorspace RGB ../static/images/apod.jpg"
        if os.name == 'posix':
            app.logger.info("optimizing apod image")
            process = subprocess.Popen(bash_command, shell=True)
            process.kill()
    except requests.exceptions.ConnectionError:
        header, date, explanation, title, url = "", "", "", "", "../static/images/500.jpg"
    threading.Timer(600, get_apod_pics).start()


get_apod_pics()


@app.route("/")
def hello():
    return render_template("main.html", header=header, date=date, explanation=explanation, title=title, url=url)


# TODO: implement save function for existing and new notes; how are new notes created?
# TODO: should the save function save locally first then save to gdrive?
@app.route("/notebook/")
def notebook():
    directory = os.fsencode("./static/notes")
    notes = [os.fsdecode(file) for file in os.listdir(directory)]
    return render_template("notebook.html", notes=notes)


@app.route("/note_upload/<id>", methods=['POST'])
def note_upload(id):
    import json
    note = request.form['note']
    note_body = json.loads(note, strict=False)
    content = note_body['ops'][0]['insert']
    directory = os.fsencode("./static/notes")
    file = open("./static/notes/{}".format(id), 'w')
    file.write(content)
    notes = [os.fsdecode(file) for file in os.listdir(directory)]
    return render_template("notebook.html", notes=notes)


@app.route("/notebook/<id>")
def note(id):
    content = ""
    if id != "new_note":
        note = open("./static/notes/{}".format(id), 'r')
        content = note.read()
    return render_template("note.html", id=id, content=content)


@app.route("/coolstuff/")
def coolstuff():
    return render_template("coolstuff.html")


@app.route("/projects/")
def projects():
    return render_template("projects.html")


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/test")
def home():
    return render_template("test.html")


@app.route("/purple_rain")
def purple_rain():
    return render_template("purple_rain.html")


@app.route("/keybase.txt")
def keybase():
    return send_from_directory(app.static_folder, 'keybase.txt')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
