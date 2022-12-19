import os
from flask import Flask, render_template, request, redirect, url_for

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

engine = create_engine("sqlite:///birthdays.db")
db = scoped_session(sessionmaker(bind=engine))

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        if not name or not month or not day:
            return render_template("error.html")

        current_id = db.execute("SELECT id FROM birthdays ORDER BY id DESC LIMIT 1")
        if not current_id:
            current_id = 1
        else:
            current_id = current_id[0]["id"] + 1
        db.execute("INSERT INTO birthdays (id, name, month, day) VALUES (?, ?, ?, ?)", current_id, name, month, day)

        return redirect("/")

    else:

        birthdays = db.execute("SELECT * FROM birthdays")
        print(birthdays)

        return render_template("index.html", birthdays=birthdays)
