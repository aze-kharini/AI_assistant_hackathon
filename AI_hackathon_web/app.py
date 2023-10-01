from flask import Flask, render_template, session, redirect, url_for, g, request, make_response
from flask_session import Session
from forms import QuestionForm
from database import get_db, close_db


app = Flask(__name__)
# For a session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# For forms
app.config["SECRET_KEY"] = "opaweriycnweuraycsiyomfihvaewiofhvawpo"
Session(app)


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")