from flask import Flask, render_template, redirect, url_for
import psutil
import datetime
import os
import Controller

app = Flask(__name__)
ctrl = Controller.Controller('/dev/ttyS0', 9600)

def template(title = "Farmatron", text = ""):
    now = datetime.datetime.now()
    timeString = now
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : text
        }
    return templateDate

@app.route("/")
def hello():
    templateData = template()
    return render_template('main.html', **templateData)

@app.route("/humidity")
def humidity():
    data = ctrl.get_humidity()
    data = data.decode('ascii')
    data = data.strip('\n')
    data = data.split(' ')
    
    msg = ""
    for i in range(0, len(data)):
        datum = str(int(data[i]))
        msg += datum + ' '

    templateData = template(text = msg)
    return render_template('main.html', **templateData)

@app.route("/data_log")
def data_log():
    msg = ""
    with open('/home/pi/Desktop/AutomatedGarden/Software/data.csv', 'r') as f:
        msg += f.read()
    templateData = template(text = msg)
    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='192.168.0.173', port=5000, debug=True)
    # app.run()
