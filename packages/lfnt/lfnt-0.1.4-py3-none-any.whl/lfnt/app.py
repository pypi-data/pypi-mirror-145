import os
from flask import Flask, render_template
import configparser
from .digestion import DigestiveSystem

app = Flask(__name__)
de = DigestiveSystem()


def get_data():
    return de.dump()


@app.route("/")
def index():
    return render_template("home.html", data=get_data())


@app.route("/profile")
def profile():
    return render_template("profile.html", data=get_data())


@app.route("/environment")
def environment():
    return render_template("environment.html", data=get_data())


if __name__ == "__main__":
    app.run()
