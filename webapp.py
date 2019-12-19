from flask import Flask, request, Markup, render_template, flash, url_for
import os
import json

app = Flask(__name__)

with open('police_shootings.json') as shootings_data:
    shootings = json.load(shootings_data)
    
"""Gets the victims names and if there is the name TK TK, don't include"""
def get_victim_names():
    listOfNames = []
    for key in shootings:
        if key['Person']['Name'] != "TK TK":
            listOfNames.append(key['Person']['Name'])
    options = ""
    for name in listOfNames:
        options = options + Markup("<option value=\"" + name + "\">" + name + "</option>")
    return options
"""Gets the DATE of the incident"""
def get_date(name):
    date = shootings[0]['Incident']['Date']['Full']
    for key in shootings:
        if key['Person']['Name'] == name:
            date = key['Incident']['Date']['Full']
    return date
"""Gets the AGE of the victim"""
def get_age(name):
    age = shootings[0]['Person']['Age']
    for key in shootings:
        if key['Person']['Name'] == name:
            age = key['Person']['Age']
    return age
"""Gets the GENDER of the victim"""
def get_gender(name):
    gender = shootings[0]['Person']['Gender']
    for key in shootings:
        if key['Person']['Name'] == name:
            gender = key['Person']['Gender']
    return gender
"""Gets the RACE of the victim"""
def get_race(name):
    race = shootings[0]['Person']['Race']
    for key in shootings:
        if key['Person']['Name'] == name:
            race = key['Person']['Race']
    return race
"""Gets the CITY of the where the incident took place"""
def get_city(name):
    city = shootings[0]['Incident']['Location']['City']
    for key in shootings:
        if key['Person']['Name'] == name:
            city = key['Incident']['Location']['City']
    return city
"""Gets the STATE of the where the incident took place"""
def get_state(name):
    state = shootings[0]['Incident']['Location']['State']
    for key in shootings:
        if key['Person']['Name'] == name:
            state = key['Incident']['Location']['State']
    return state
"""Gets the MANNER of the how the victim was taken down"""
def get_manner(name):
    manner = shootings[0]['Shooting']['Manner']
    for key in shootings:
        if key['Person']['Name'] == name:
            manner = key['Shooting']['Manner']
    return manner
"""Gets whether victim was armed or not"""
def get_armed(name):
    armed = shootings[0]['Factors']['Armed']
    for key in shootings:
        if key['Person']['Name'] == name:
            if key['Factors']['Armed'] == "unarmed":
                armed = "The victim was " + key['Factors']['Armed']
            elif key['Factors']['Armed'] == "unknown":
                armed = "Whether the victim was carrying a weapon is " + key['Factors']['Armed']
            else:
                armed = "The victim carried a " + key['Factors']['Armed']
    return armed
"""Compiles the functions into one fact"""
def get_shooting_facts():
    name = request.args['name']
    fact = ""
    fact = fact + Markup(
    "<h3>" + "ABOUT THE VICTIM" + "</h3>" + "<p>" + "Name: " + name + "<br>" + "Age: " + str(get_age(name)) + "<br>" +"Gender: " + get_gender(name) + "<br>" +"Race: " + get_race(name) + "<br>" + "</p>"
    "<h3>" + "WHERE IT HAPPENED" + "</h3>" + "<p>" + "This victim was " + get_manner(name) + " in " + get_city(name) + " " + get_state(name) + " on " + get_date(name) + "</p>" + 
    "<h3>" + "ADDITIONAL FACTORS" + "</h3>" + "<p>" + get_armed(name) + "</p>")
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