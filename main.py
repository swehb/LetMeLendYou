from flask import Flask
from flask import url_for, render_template, request

app = Flask(__name__)

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

@app.route("/home")
def home():

    return "<p> your home page </p>"

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

@app.route("/api/login", methods=["GET", "POST"])
def login_verification():
    access_granted = False
    username = request.form.get("username", "unknown")
    password = request.form.get("password", "unknownpass")
    print(username, password)
    print("hello world login")
    #check if user is OK from the database
    if access_granted == False:
        print("access not granted")
        return("access not granted")
        # return main user page
    else:
        print("access granted")
        return("access granted")
        # return login page
    return("success")


@app.route("/api/new_user", methods=["GET", "POST"])
def new_user_creation():
    # verify if username is available
    # verify if PW meets qualifications
        # enter password again, must match
    # creates the new user and password combination
    # verify correct email format (xx@xx.xx)
    # redirect to login page - but autofill the username
    return "<p> new user placeholder </p>"




# NOTE - not sure what this is for. do we need it? 
# if __name__=="__main__":
#     app.run(debug=True)
