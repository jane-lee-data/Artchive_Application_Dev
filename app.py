import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import apology, login_required
import sqlite3

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure to use SQlite database
db = SQL("sqlite:///project.db")

# Home, Register, Log in and out
@app.route("/")
def index():
    """ Randomly select an image from the collection everytime visited """
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    welcomeimage = cur.execute("SELECT imageurl FROM objects_images ORDER BY RANDOM() LIMIT 1").fetchall()
    conn.commit()
    return render_template("index.html", welcomeimage=welcomeimage)


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register a user with ID and password """
    if (request.method == "GET"):
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Type username")
        if not password:
            return apology("Type password")
        if not confirmation:
            return apology("Type password again for confirmation")
        if confirmation != password:
            return apology("Password not matched. Type again")

        """Store a hash of the user's password"""
        hash = generate_password_hash(password)
        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("Username already exists")
        session["user_id"] = new_user

        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in """

    session.clear()

    # route via POST
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    # route via GET
    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """ Log user out"""
    session.clear()
    return redirect("/")



@app.route("/explore", methods=["GET", "POST"])
@login_required
def explore():
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()

    if request.method == "GET":
        return render_template("explore.html")
    else:
        search = request.form.get("search")
        objectinfo = request.form.get("objectinfo")

        if search:
            rows = cur.execute("SELECT title, attribution, imageurl, objectid FROM objects_images WHERE title LIKE '%' || ? || '%'", [search])
            conn.commit()
            return render_template("searchresult.html", rows=rows)

        if objectinfo:
            infos = cur.execute("SELECT title, attribution, displaydate, medium, dimensions, classification, objectid FROM objects WHERE objectid = ?", [objectinfo]).fetchall()
            images = cur.execute("SELECT imageurl FROM objects_images WHERE objectid = ?", [objectinfo])
            conn.commit()
            return render_template("objectinfo.html", infos=infos, images=images)

        conn.close()



# User's page
@app.route("/mylist", methods=["GET", "POST"])
@login_required
def mylist():
    """ show artworks the user liked """
    user_id = session["user_id"]
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()

    if request.method == "GET":
        likedobjects = cur.execute("SELECT * FROM mylist WHERE user_id = ?", [user_id])
        conn.commit()
        return render_template("mylist.html", likedobjects=likedobjects)

    else:
        saveobject = request.form.get("saveobject")
        if saveobject:
            queryone = cur.execute("SELECT objectid, title, attribution, imageurl FROM objects_images WHERE objectid = ?", [saveobject]).fetchall()
            cur.execute("INSERT OR IGNORE INTO mylist (user_id, objectid, title, attribution, imageurl) VALUES (?, ?, ?, ?, ?)",
                                (user_id, queryone[0][0], queryone[0][1], queryone[0][2], queryone[0][3]))
            likedobjects = cur.execute("SELECT * FROM mylist WHERE user_id = ?", [user_id])
            conn.commit()
            return render_template("mylist.html", likedobjects=likedobjects)

        deleteobject=request.form.get("deleteobject")
        if deleteobject:
            # delete a row from mylist table
            cur.execute("DELETE FROM mylist WHERE objectid = ?", [deleteobject])
            # reload updated list
            likedobjects = cur.execute("SELECT * FROM mylist WHERE user_id = ?", [user_id])
            conn.commit()
            return render_template("mylist.html", likedobjects=likedobjects)

        conn.close()


@app.route("/discover")
def discover():
    """ Randomly select images from the collection"""
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    randomimages = cur.execute("SELECT imageurl, objectid FROM objects_images ORDER BY RANDOM() LIMIT 20").fetchall()
    conn.commit()
    return render_template("discover.html", randomimages=randomimages)


