from flask import Flask, url_for, render_template, request, redirect
import pandas
import csv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///entries.db"

with app.app_context():
	db = SQLAlchemy(app)


class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Task %r>' % self.id


class Entry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	owner = db.Column(db.Integer)
	borrower = db.Column(db.Integer)
	book_name = db.Column(db.String(200), nullable=False)
	due_date = db.Column(db.DateTime, default=datetime.utcnow)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Entry %r>' % self.id


#frontend routes

@app.route("/")
def landing_page():
	# welcome message
	# login button
	# new user button
	# what is this? text to describe
	# check if user is logged in (cookies yum), if so, take to home page
	return render_template("landing.html")

@app.route("/login")
def login():
	# username field
	# password field
	# submit button
	# forgot password
	return render_template("login.html")

@app.route("/new_user")
def new_user():
	# username field - verify that it is not taken in database
	# password field
	# password verification field
	# email address - optional but needed for PW resets and reminders
	return render_template("new_user.html")

@app.route("/forgot_password")
def forgot_password():
	# enter email or username
	# if email does not exist in db, do nothing, else send password
	return render_template("forgot_password.html")

@app.route("/home/user=<username>")
def home(username):
	# tasks = Todo.query.order_by(Todo.date_created).all() # delete later

	entries = Entry.query.order_by(Entry.date_created).all()
	return render_template("homepage.html", entries=entries, username=username)

@app.route("/add_entry")
def add_entry():
	# Form
		# Name of item (book title) / description - REQUIRED
		# Return by date - if left blank, default to indefinite 
			# Decide how dates are displayed - DD/MM/YYYY, calendar drop-down?
			# Has to be in the future from today’s date
		# Other party - REQUIRED
	# Press “Confirm” / “Save” / whatever button to save the entry
	return "<p> add a new loan or borrowing entry </p>" 


#api routes
logged_in_user = None

@app.route("/api/login", methods=["GET", "POST"])
def login_verification():
	username = request.form.get("username", "unknown")
	password = request.form.get("password", "unknownpass")
	
	# if username is not in csv, "user not found or password incorrect" error
	# if username and password don't match, "user not found or password incorrect" error

	df = pandas.read_csv("users.csv")
	df2 = df[df["username"].str.fullmatch(username)]
	df_pass = 0

	if df2["username"].empty:
		print("user not found")
		access_granted = False
	else:
		if password == df2["password"].to_string(index=False):
			print("password correct")
			access_granted = True
		else:
			print("password incorrect")
			access_granted = False


	#check if user is OK from the database
	if access_granted == False:
		print("access not granted")
		return render_template("login.html")
	else:
		global logged_in_user
		logged_in_user = username
		print(f"access granted {logged_in_user}")
		return redirect(f"/home/user={username}")

@app.route("/api/new_user", methods=["GET", "POST"])
def new_user_creation():
	# verify if username is available
	# verify if PW meets qualifications
		# enter password again, must match
	# creates the new user and password combination
	# redirect to login page - but autofill the username
	new_username = request.form.get("username", "unknown")
	password = request.form.get("password","pass")
	email = request.form.get("email","a@a.com")
	
	df = pandas.read_csv('users.csv')
	
	df2 = df[df['username'].str.fullmatch(new_username)]
	
	if not (df2["username"].empty):
		#username taken already
		print(new_username + " is already taken")
		return render_template("new_user.html")

	else: 
		#username available so you're good to go
		row = [new_username,password,email]
		with open('users.csv','a') as f:
			writer = csv.writer(f)
			writer.writerow(row)
	
		return  render_template("homepage.html")

@app.route("/api/create_new", methods=["GET", "POST"])
def create_new():
	print(logged_in_user)

	if request.method == "POST":
		owner = request.form["owner"]
		borrower = request.form["borrower"]
		book_name = request.form["bookname"]
		# due_date = request.form["duedate"]
		

		new_entry = Entry(owner=owner, borrower=borrower, book_name=book_name) #, due_date=due_date)

		try:
			db.session.add(new_entry)
			db.session.commit()
			return redirect(f"/home/user={logged_in_user}")
			#return "ok"
		except:
			return "there was an issue adding your entry"

	else:
		entries = Entry.query.order_by(Entry.date_created).all()
		return render_template("homepage.html", entries=entries)



# NOTE - not sure what this is for. do we need it? 
# if __name__=="__main__":
#	 app.run(debug=True)
