from flask import Flask, request, Markup, render_template, flash, url_for
import os
import json

app = Flask(__name__)
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
    return render_template('page3.html', data = get_pie_race())

"""Gets race and formats it for the pie chart"""
def get_pie_race():
    asian = 0
    african = 0
    white = 0
    hispanic = 0
    native = 0
    other = 0
    unknown = 0
    
    listOfRaces = []
    for key in shootings:
        if key['Person']['Name'] != "TK TK":
            listOfRaces.append(key['Person']['Race'])
    for race in listOfRaces:
        if race == "Asian":
            asian+=1
        elif race == "African American":
            african+=1
        elif race == "White":
            white+=1
        elif race == "Hispanic":
            hispanic+=1
        elif race == "Native American":
            native+=1
        elif race == "Other":
            other+=1
        else:
            unknown+=1
    data = ""
    data = data + Markup("var data = google.visualization.arrayToDataTable([['Race', 'Number of Victims Shot'],['White', " + str(white) + "],['African American'," + str(african) + "],['Hispanic'," + str(hispanic) + "],['Unknown'," + str(unknown) + "],['Asian'," + str(asian) + "],['Native American'," + str(native) + "],['Other'," + str(other) + "]]);")
    return data

"""Allows the police_shootings.json file to be accessed"""
with open('police_shootings.json') as shootings_data:
    shootings = json.load(shootings_data)
    
"""Gets the victims names and if there is the name, TK TK, don't include"""
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
"""Gets threat level of victim"""
def get_threat_level(name):
    threat_level = shootings[0]['Factors']['Threat-Level']
    for key in shootings:
        if key['Person']['Name'] == name:
            if key['Factors']['Threat-Level'] == "attack":
                threat_level = "The victim was attacking"
            elif key['Factors']['Threat-Level'] == "undetermined":
                threat_level = "Undetermined"
            else:
                threat_level = "Other"
    return threat_level
"""Gets whether the victim has a mental illness"""
def get_mental_illness(name):
    mental_illness = False
    for key in shootings:
        if key['Person']['Name'] == name:
            if key['Factors']['Mental-Illness'] == True:
                mental_illness = "The victim has a mental illness"
            else:
                mental_illness = "The victim did not have a mental illness"
    return mental_illness
"""Gets whether the victim was fleeing"""
def get_fleeing(name):
    fleeing = shootings[0]['Factors']['Fleeing']
    for key in shootings:
        if key['Person']['Name'] == name:
            if key['Factors']['Fleeing'] == "Not fleeing":
                fleeing = "The victim was not fleeing"
            elif key['Factors']['Fleeing'] == "unknown":
                fleeing = "Unknown"
            else:
                fleeing = "The victim was fleeing via " + key['Factors']['Fleeing']
    return fleeing
"""Gets whether the officer had a body-cam"""
def get_bodycam(name):
    bodycam = shootings[0]['Shooting']['Body-Camera']
    for key in shootings:
        if key['Person']['Name'] == name:
            if key['Shooting']['Body-Camera'] == True:
                bodycam = "The victim was not fleeing"
            elif key['Factors']['Fleeing'] == "unknown":
                fleeing = "Unknown"
            else:
                fleeing = "The victim was fleeing via " + key['Factors']['Fleeing']
    return fleeing
"""Compiles the functions into one fact"""
def get_shooting_facts():
    name = request.args['name']
    fact = ""
    fact = fact + Markup(
    "<h3>" + "ABOUT THE VICTIM" + "</h3>" + "<p>" + "Name: " + name + "<br>" + "Age: " + str(get_age(name)) + "<br>" +"Gender: " + get_gender(name) + "<br>" +"Race: " + get_race(name) + "<br>" + "</p>"
    "<h3>" + "WHERE IT HAPPENED" + "</h3>" + "<p>" + "This victim was " + get_manner(name) + " in " + get_city(name) + ", " + get_state(name) + " on " + get_date(name) + "</p>" + 
    "<h3>" + "ADDITIONAL FACTORS" + "</h3>" + "<p>" + "Threat Level: " + get_threat_level(name) + "<br>" + "Is Armed? : " + get_armed(name) + "<br>" + "Has a mental illness? : " + get_mental_illness(name) + "<br>" + "Is fleeing? : "+ get_fleeing(name) + "</p>")
    return fact

if __name__== "__main__":
    app.run(debug=True)