from flask import Flask, request, Markup, render_template, flash, url_for
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html')
    
@app.route("/p1")
def render_main():
    return render_template('page1.html')

if __name__== "__main__":
    app.run(debug=False)