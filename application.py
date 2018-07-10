import os

from flask import Flask, session, render_template, request, redirect, url_for, \
    escape, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests
import json
import datetime

app = Flask(__name__)
app.secret_key = "AYU9n36P&99amJDcyCQYT4Q3"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    """User Login"""

    # if a user is already logged in, redirect them to the search page
    if "username" in session:
        return redirect(url_for("search"))
    # else, render the login form
    else:
        return render_template("login_register.html")


@app.route("/register")
def register():
    """User Registration"""

    return render_template("login_register.html")


@app.route("/returninguser", methods=["POST"])
def returning_user():
    """Returning User Authentication"""

    # get information from form
    username = request.form.get("username")
    password = request.form.get("password")

    # check to see if the user exists, if not refresh page with failure message
    if db.execute("SELECT * FROM users WHERE username = :username",
                  {"username": username}).rowcount == False:
        flash("ERROR: User does not exist.", "danger")
        return redirect(url_for("index"))

    # verify the user's password
    if db.execute("SELECT username FROM users WHERE password = :password",
                  {"username": username, "password": password}).rowcount == True:
        # add username to session and redirect to search page
        session["username"] = username
        return redirect(url_for("search"))
    # if the password doesn't match, refresh the page with failure message
    else:
        flash("ERROR: Password does not match.", "danger")
        return redirect(url_for("index"))


@app.route("/newuser", methods=["POST"])
def new_user():
    """New User Account Creation"""

    # get input from form
    username = request.form.get("username")
    password = request.form.get("password")

    # check to see if user already exists in database, if so render the failure
    # page
    if db.execute("SELECT * FROM users WHERE username = :username",
                  {"username": username}).rowcount == True:
        flash("ERROR: Username already taken.", "danger")
        return redirect(url_for("register"))

    # add new user to database
    db.execute("INSERT INTO users (username, password) \
    VALUES (:username, :password)",
               {"username": username, "password": password})

    # commit user data to database
    db.commit()

    # return to login page and display success message
    flash("Registration successful.", "success")
    return redirect(url_for("index"))


@app.route("/search")
def search():
    """Search Page Rendering"""

    return render_template("search.html")


@app.route("/search", methods=["POST"])
def search_results():
    """Search Results"""

    # capture search query from form and add placeholders
    search_query = "%" + request.form.get("search_query") + "%"

    # find zipcodes and cities similar to the search query and save them
    locations = db.execute("SELECT * FROM locations WHERE zipcode \
                           LIKE :search_query OR city LIKE UPPER(:search_query)",
                           {"search_query": search_query})

    # render page with location results
    return render_template("search_results.html", locations=locations)


@app.route("/location/<zipcode>")
def location_info(zipcode):
    """Location Information"""

    # find location information in database via zipcode
    location = db.execute("SELECT * FROM locations WHERE zipcode = :zipcode",
                          {"zipcode": zipcode}).fetchone()

    # if no results are returned, return 404
    if location is None:
        return render_template('404.html'), 404

    # save lat and long data as strings
    lat = str(location[4])
    long = str(location[5])

    # construct API call for weather
    api_call = "https://api.darksky.net/forecast/8744aa1238d1ffb8b86d1083af591f40/" \
        + lat + "," + long

    # fetch API weather data, format it, and save it
    weather = requests.get(api_call).json()
    weather = json.dumps(weather["currently"])
    weather = json.loads(weather)

    # convert epoch time to datetime
    time = int(json.dumps(weather["time"]))
    time = datetime.datetime.fromtimestamp(time).strftime('%I:%M:%S %p')

    # save the zipcode, to be utilized for check ins
    session["zipcode"] = zipcode

    # save session zipcode and username as variables
    zipcode = session.get("zipcode", None)
    username = session.get("username", None)

    # fetch comments for the location
    comments = db.execute("SELECT * FROM check_ins WHERE zipcode = :zipcode",
                          {"zipcode": zipcode})

    # check to see if user has already commented, if so, set variable to disable
    # comment field
    if db.execute("SELECT * FROM check_ins WHERE zipcode = :zipcode \
                  AND username = :username",
                  {"zipcode": zipcode, "username": username}).rowcount == True:
        commented = True
    else:
        commented = False

    # render page with location information
    return render_template("location_info.html", location=location,
                           weather=weather, time=time, comments=comments,
                           commented=commented)


@app.route("/checkin", methods=["POST"])
def check_in():
    """Check In"""

    # capture comment from form
    comment = request.form.get("comment")

    # save session zipcode and username as variables
    zipcode = session.get("zipcode", None)
    username = session.get("username", None)

    # add comment to database
    db.execute("INSERT INTO check_ins(zipcode, username, comment) \
               VALUES(:zipcode, :username, :comment)",
               {"zipcode": zipcode, "comment": comment, "username": username})

    # commit comment to database
    db.commit()

    # notify user of success and reload page
    flash("Comment successfully submitted.", "success")
    return redirect(url_for("location_info", zipcode=zipcode))


@app.route("/logout")
def logout():
    """User Logout"""

    # remove user from session and return to login page
    session.pop("username", None)
    return redirect("/")
