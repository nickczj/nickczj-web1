from flask import Flask, render_template, send_from_directory
app = Flask(__name__, static_folder='static')

OLD_API_KEY = "37fdVwafhb4HlDIIAgFJ6HbIeEk9qdanfQvxkTnQ"
API_KEY = "7UoReKEbxnGRMqwkVb9IBvhBmzCtpYdAtPFbnG90"

@app.route("/")
def hello():
    import requests
    import json

    response = requests.get("https://api.nasa.gov/planetary/apod?api_key={}".format(API_KEY))
    data = response.json()

    date = data['date']
    while True:
        try:
            response = requests.get("https://api.nasa.gov/planetary/apod?api_key=37fdVwafhb4HlDIIAgFJ6HbIeEk9qdanfQvxkTnQ")
            data = response.json()
		
        except requests.exceptions.ConnectionError:
            return render_template("main.html", header="", date="", explanation="", title="", url="static/images/500.jpg")

    date = data['date'] + ": NASA's Astronomy Picture of the Day"
    explanation = data['explanation']
    title = data['title']
    url = data['url']

    return render_template("main.html", header="Take a moment and soak in the wonders of space.", date=date, explanation=explanation, title=title, url=url)

@app.route("/notepad/")
def notepad():
    return render_template("notepad.html")

@app.route("/coolstuff/")
def coolstuff():
	return render_template("coolstuff.html")

@app.route("/projects/")
def projects():
    import requests
    import json

    response = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date=2017-05-24&api_key={}".format(API_KEY))
    info = response.json()
    max_sol = info['photos'][0]['rover']['max_sol']
    max_date = info['photos'][0]['rover']['max_date']
    response = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={}&api_key={}".format(max_sol, API_KEY))
    data = response.json()

    d = data['photos']
    ld = len(d)
    e = [d[i]['img_src'][:4] + 's' + d[i]['img_src'][4:] for i in range(len(d))]
    while True:
        try:
            response = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date=2017-05-24&api_key=37fdVwafhb4HlDIIAgFJ6HbIeEk9qdanfQvxkTnQ")
            info = response.json()
            max_sol = info['photos'][0]['rover']['max_sol']
            max_date = info['photos'][0]['rover']['max_date']
            response = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={}&api_key=37fdVwafhb4HlDIIAgFJ6HbIeEk9qdanfQvxkTnQ".format(max_sol))
            data = response.json()

            d = data['photos']
            ld = len(d)
            e = [d[i]['img_src'][:4] + 's' + d[i]['img_src'][4:] for i in range(len(d))]

        except requests.exceptions.ConnectionError:
            return render_template("main.html", header="", date="", explanation="", title="", url="../static/images/500.jpg")

    return render_template("projects.html", images=e, ld=ld, date=max_date)

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
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    s=datetime.datetime(2017,1,1)
    e=datetime.datetime.now()
    df=data.DataReader(name="GOOGL",data_source="google",start=s,end=e)

    def id(c, o):
        if c>o:
            value="Increase"
        elif c<o:
            value="Decrease"
        else:
            value="Equal"
        return value

    df["Status"]=[id(c,o) for c,o in zip(df.Close,df.Open)]
    df["Middle"]=(df.Open+df.Close)/2
    df["Height"]=abs(df.Close-df.Open)

    p=figure(x_axis_type="datetime",y_axis_label="USD",height=300,responsive=True,
			 toolbar_location="below",toolbar_sticky=False)
    p.title.text="Candlestick Chart (GOOGL, 01 Jan 2017 - present)"
    p.grid.grid_line_alpha=0.3

    hours_12=12*60*60*1000

    p.segment(df.index,df.High,df.index,df.Low,color="Black")

    p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"],
           hours_12, df.Height[df.Status=="Increase"], fill_color="#0000FF", line_color="black")

    p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"],
           hours_12, df.Height[df.Status=="Decrease"], fill_color="#DC413C", line_color="black")

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template("googl.html", script1=script1, div1=div1, cdn_css=cdn_css, cdn_js=cdn_js)

@app.route("/aapl/")
def aapl():
    import datetime
    from pandas_datareader import data
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    s=datetime.datetime(2017,1,1)
    e=datetime.datetime.now()
    df=data.DataReader(name="AAPL",data_source="google",start=s,end=e)

    def id(c, o):
        if c>o:
            value="Increase"
        elif c<o:
            value="Decrease"
        else:
            value="Equal"
        return value

    df["Status"]=[id(c,o) for c,o in zip(df.Close,df.Open)]
    df["Middle"]=(df.Open+df.Close)/2
    df["Height"]=abs(df.Close-df.Open)

    p=figure(x_axis_type="datetime",y_axis_label="USD",height=300,responsive=True,
			 toolbar_location="below",toolbar_sticky=False)
    p.title.text="Candlestick Chart (AAPL, 01 Jan 2017 - present)"
    p.grid.grid_line_alpha=0.3

    hours_12=12*60*60*1000

    p.segment(df.index,df.High,df.index,df.Low,color="Black")

    p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"],
           hours_12, df.Height[df.Status=="Increase"], fill_color="#0000FF", line_color="black")

    p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"],
           hours_12, df.Height[df.Status=="Decrease"], fill_color="#DC413C", line_color="black")

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
