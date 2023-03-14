from flask import Flask
from flask import url_for
from flask import render_template



app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p> Hello, World!</p>"


@app.route("/hello <name>")
def hello(name):
    return f"Hello, {name}!"
  
  
@app.route("/test2")
def test2():
    return url_for("static", filename='test2.html')
    
    



    