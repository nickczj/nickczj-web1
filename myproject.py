from flask import Flask, render_template, send_from_directory, request
import requests
import threading
import logging
import urllib.request
import os
import subprocess
import datetime
import notebook

app = Flask(__name__, static_folder='static')

logging.basicConfig(level=logging.DEBUG)
log = app.logger

if not app.debug:
    import logging

    file_handler = logging.FileHandler('flask.log')
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)

API_KEY = "37fdVwafhb4HlDIIAgFJ6HbIeEk9qdanfQvxkTnQ"
OLD_API_KEY = "7UoReKEbxnGRMqwkVb9IBvhBmzCtpYdAtPFbnG90"

header, date, explanation, title, url = "", "", "", "", ""
images, max_date = [], ""


# def get_apod_pics():
#     log.info(datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y") + " getting apod data")
#     global header, date, explanation, title, url
#     try:
#         header = "Take a moment and soak in the wonders of space."
#         response = requests.get("https://api.nasa.gov/planetary/apod?api_key={}".format(API_KEY))
#         data = response.json()
#         date = data['date'] + ": NASA's Astronomy Picture of the Day"
#         explanation = data['explanation']
#         title = data['title']
#         link = data['url']
#         urllib.request.urlretrieve(link, "static/images/apod.jpg")
#         if 'jpg' in data['url']:
#             url = "../static/images/apod.jpg"
#         else:
#             url = data['url']
#         bash_command = "convert ../static/images/apod.jpg -sampling-factor 4:2:0 -strip -quality 85 -interlace JPEG" \
#                        " -colorspace RGB ../static/images/apod.jpg"
#         if os.name == 'posix':
#             log.info("optimizing apod image")
#             process = subprocess.Popen(bash_command, shell=True)
#             process.kill()
#     except requests.exceptions.ConnectionError:
#         header, date, explanation, title, url = "", "", "", "", "../static/images/500.jpg"
#     threading.Timer(600, get_apod_pics).start()


# get_apod_pics()


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


@app.route("/googl/")
def googl():
    import datetime
    from pandas_datareader import data
    from bokeh.plotting import figure
    from bokeh.embed import components
    from bokeh.resources import CDN

    s = datetime.datetime(2017, 1, 1)
    e = datetime.datetime.now()
    df = data.DataReader(name="GOOGL", data_source="google", start=s, end=e)

    def identification(c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value

    df["Status"] = [identification(c, o) for c, o in zip(df.Close, df.Open)]
    df["Middle"] = (df.Open + df.Close) / 2
    df["Height"] = abs(df.Close - df.Open)

    p = figure(x_axis_type="datetime", y_axis_label="USD", height=300, responsive=True,
               toolbar_location="below", toolbar_sticky=False)
    p.title.text = "Candlestick Chart (GOOGL, 01 Jan 2017 - present)"
    p.grid.grid_line_alpha = 0.3

    hours_12 = 12 * 60 * 60 * 1000

    p.segment(df.index, df.High, df.index, df.Low, color="Black")

    p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"],
           hours_12, df.Height[df.Status == "Increase"], fill_color="#0000FF", line_color="black")

    p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"],
           hours_12, df.Height[df.Status == "Decrease"], fill_color="#DC413C", line_color="black")

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template("googl.html", script1=script1, div1=div1, cdn_css=cdn_css, cdn_js=cdn_js)


@app.route("/aapl/")
def aapl():
    import datetime
    from pandas_datareader import data
    from bokeh.plotting import figure
    from bokeh.embed import components
    from bokeh.resources import CDN

    s = datetime.datetime(2017, 1, 1)
    e = datetime.datetime.now()
    df = data.DataReader(name="AAPL", data_source="google", start=s, end=e)

    def identification(c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value

    df["Status"] = [identification(c, o) for c, o in zip(df.Close, df.Open)]
    df["Middle"] = (df.Open + df.Close) / 2
    df["Height"] = abs(df.Close - df.Open)

    p = figure(x_axis_type="datetime", y_axis_label="USD", height=300, responsive=True,
               toolbar_location="below", toolbar_sticky=False)
    p.title.text = "Candlestick Chart (AAPL, 01 Jan 2017 - present)"
    p.grid.grid_line_alpha = 0.3

    hours_12 = 12 * 60 * 60 * 1000

    p.segment(df.index, df.High, df.index, df.Low, color="Black")

    p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"],
           hours_12, df.Height[df.Status == "Increase"], fill_color="#0000FF", line_color="black")

    p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"],
           hours_12, df.Height[df.Status == "Decrease"], fill_color="#DC413C", line_color="black")

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template("aapl.html", script1=script1, div1=div1, cdn_css=cdn_css, cdn_js=cdn_js)


@app.route("/purple_rain")
def purple_rain():
    return render_template("purple_rain.html")


@app.route("/keybase.txt")
def keybase():
    return send_from_directory(app.static_folder, 'keybase.txt')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
