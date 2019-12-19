from flask import Flask, request, Markup, render_template, flash, url_for
import os
import json

app = Flask(__name__)

with open('police_shootings.json') as shootings_data:
    shootings = json.load(shootings_data)
    
"""Gets the victims names and if multiple of same name add a num ex.) TK TK(1), TK TK(2)..."""
def get_victim_names():
    listOfNames = []
    for key in shootings:
        listOfNames.append(key['Person']['Name'])
    options = ""
    for name in listOfNames:
        options = options + Markup("<option value=\"" + name + "\">" + name + "</option>")
    return options
"""Gets the date of the incident"""
def get_date(name):
    date = shootings[0]['Incident']['Date']['Full']
    for key in shootings:
        if key['Person']['Name'] == name:
            date = key['Incident']['Date']['Full']
    return date
"""Compiles the functions into one fact"""
def get_shooting_facts():
    name = request.args['name']
    fact = ""
    fact = fact + Markup(
    "<h3>" + "ABOUT THE VICTIM" + "</h3>" + "<p>" + "Name: " + name + "<br>" + "Age: " + "AGE" + "<br>" +"Gender: " + "GENDER" + "<br>" +"Race: " + "RACE" + "<br>" + "</p>"
    "<h3>" + "WHERE IT HAPPENED" + "</h3>" + "<p>" + "This victim was " + "MANNER" + " in " + "CITY" + " " + "STATE" + " on " + get_date(name) + "</p>")
    return fact

@app.route("/")
def render_main():
    return render_template('home.html')
    
@app.route("/p2")
def render_page2():
    return render_template('page2.html', options = get_victim_names())

@app.route("/response")
def render_response():
    return render_template('page2.html', options = get_victim_names(), shootingFact = get_shooting_facts())
    
@app.route("/p3")
def render_page3():
    return render_template('page3.html')

if __name__== "__main__":
    app.run(debug=True)