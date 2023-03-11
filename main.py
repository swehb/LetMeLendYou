from flask import Flask
from flask import url_for
from flask import render_template



app = Flask(__name__)

@app.route("/")
def landing_page():
    # welcome message
    # login button
    # new user button
    # what is this? text to describe
    # check if user is logged in (cookies yum), if so, take to home page
    return "<p> Landing page!</p>"

@app.route("/login")
def login():
    return "<p> loge into!</p>"

@app.route("/hello <name>")
def hello(name):
    return f"Hello, {name}!"