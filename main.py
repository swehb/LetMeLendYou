from flask import Flask, url_for, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import *
import os, sys
import json
import smtplib, ssl
from email.message import EmailMessage


def read_secrets() -> dict:
	filename = os.path.join('secrets.json')
	try:
		with open(filename, mode='r') as f:
			return json.loads(f.read())
	except (FileNotFoundError) as error:
		print(error)

		
secrets = read_secrets()
email_auth = secrets['email_key']

print(email_auth)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///entries.db"
app.secret_key = b'password'

with app.app_context():
	db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(str(user_id))


class User(UserMixin, db.Model):
	__tablename__ = "user"

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(300), nullable=False)

	def __repr__(self):
		return '<User %r>' % self.username


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

@app.route("/home/")
@login_required
def home():
	entries_lending = Entry.query.order_by(Entry.date_created.desc()).filter_by(owner=current_user.username).all()
	entries_borrowing = Entry.query.order_by(Entry.date_created.desc()).filter_by(borrower=current_user.username).all()
	return render_template("homepage.html", entries_borrowing=entries_borrowing, entries_lending=entries_lending, current_user_name=current_user.username, current_email=current_user.email)

@app.route("/add_entry")
def add_entry():
	# OLD WAY This entire section can be deleted probably as it is covered in the create_new route. 
	# Form
		# Name of item (book title) / description - REQUIRED
		# Return by date - if left blank, default to indefinite 
			# Decide how dates are displayed - DD/MM/YYYY, calendar drop-down?
			# Has to be in the future from today’s date
		# Other party - REQUIRED
	# Press “Confirm” / “Save” / whatever button to save the entry
	return "<p> add a new loan or borrowing entry </p>" 


#api routes

@app.route("/api/login", methods=["GET", "POST"])
def login_verification():
	form_username = request.form.get("username", "unknown")
	form_password = request.form.get("password", "unknownpass")

	access_granted = False

	if User.query.filter_by(username=form_username).first() is None:
		access_granted = False
	else:
		db_password = User.query.filter_by(username=form_username).first().password
		if form_password == db_password:
			access_granted = True

	if access_granted == False:
		print("access not granted")
		flash("Check your username and/or password")
		return redirect("/login")
	else:
		user = User.query.filter_by(username=form_username).first()
		login_user(user)
		print(f"access granted {form_username}")
		# OLD return redirect(f"/home/user={form_username}")
		return redirect(url_for("home"))

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

	if User.query.filter_by(username=new_username).first() is None: # this checks to see if username is available
		new_user_entry = User(username=new_username, email=email, password=password)

		try:
			db.session.add(new_user_entry)
			db.session.commit()
			login_user(new_user_entry)
			# OLD return redirect(f"/home/user={new_user_entry.username}")
			return redirect(url_for("home"))
		except:
			return "database addition, login, or redirection failed in try statement"
	else:
		return render_template("new_user.html")


@app.route("/api/create_new", methods=["GET", "POST"])
@login_required
def create_new():
	if request.method == "POST":
		owner = request.form["owner"]
		borrower = request.form["borrower"]
		book_name = request.form["bookname"]
		due_date = request.form["duedate"]
		due_date_year = int(due_date[0:4])
		due_date_month = int(due_date[5:7])
		due_date_day = int(due_date[8:10])
		
		print("I'm trying to add a book with the date of " + due_date)
		print("as a substring " + due_date[0:4]+ " "+ due_date[5:7]+ " "+ due_date[8:10])
		
		#new_entry = Entry(owner=owner, borrower=borrower, book_name=book_name) #, due_date=due_date) #without due dates
		new_entry = Entry(owner=owner, borrower=borrower, book_name=book_name, due_date=datetime(due_date_year,due_date_month,due_date_day)) #with duedates! :)
		
		
		
		try:
			db.session.add(new_entry)
			db.session.commit()
			flash("You added an item!")
			# OLD return redirect(f"/home/user={current_user.username}")
			return redirect(url_for("home"))
		except:
			return "there was an issue adding your entry"

	else:
		entries = Entry.query.order_by(Entry.date_created).all()
		return render_template("homepage.html", current_user_name=current_user.id, entries=entries)



@app.route("/api/forgot_password", methods=["GET", "POST"])
def email_password():
	
		forgotpass_emailaddress = request.form["email"]
		print("the forgotten email is "+forgotpass_emailaddress)
		
		if User.query.filter_by(email = forgotpass_emailaddress).first() is	 not None:
		
			email = EmailMessage()
			email["from"] = "Let Me Lend You App"
			#email["to"] = forgotpass_emailaddress
			email["to"] = "letmelendyouapp@gmail.com"
			email["subject"] = "Let Me Lend You app password and username"
			email.set_content(f"You can send this! This email was sent to {forgotpass_emailaddress}")

			try:
				with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
					smtp.ehlo()
					smtp.starttls()
					smtp.login("letmelendyouapp@gmail.com", email_auth)
					smtp.send_message(email)
					print("It's been sent!")
					return "Email sent"
			except:
					return "Status of send unclear"
		else:
			print("no such email exists in the DB")
			return "that email doesn' exist"

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))


# NOTE - not sure what this is for. do we need it? 
# if __name__=="__main__":
#	 app.run(debug=True)
