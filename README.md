# bookproject
Personal tracking of items (borrowing and lending) between friends.

## How to run on MacOS & Linux
- Open terminal
- Navigate to correct folder
- To set the environment variable, run `export FLASK_APP=main.py`
- Run `flask run`
- Alternatively, run `flask run --debug` to see the HTTPS request on the console and automatically have the server restart if the file has changed
- Run `flask run --host=0.0.0.0` to make it visible to all public IPs. Note that these are actual zeros, not placeholders. Will only work if on the same network. 


## Technologies

- HTML
- CSS
- Javascript
- mySQL
- Python


## How to create database in Python 3
- Open terminal and run `python3` to open interactive Python
- Run `from main import app, db`
- Run `app.app_context().push()`
- Run `db.create_all()`

