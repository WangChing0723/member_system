from flask import Flask
from flask import request
from flask import redirect
from flask import session
from flask import render_template

app = Flask(__name__)

app.secret_key = b'\xe0\xab/0\xd04\xa7l\xf95\xd0\xdc="\x14\xa7'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signin/", methods=["POST"])
def signin():
    account = request.form["account"]
    password = request.form["password"]

    if account=="test" and password=="test":
        session["account"] = account
        return redirect("/member/")
    else:
        return redirect("/error/")

@app.route("/signout")
def signout():
    session.pop("account", None)
    return redirect("/")

@app.route("/member/")
def member_info():
    if 'account' in session:
        return render_template("member.html")
    else:
        return redirect("/")

@app.route("/error/")
def error():
    return render_template("error.html")

app.run(port=3000)