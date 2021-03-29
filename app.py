from os import name
from flask import Flask
from flask import request
from flask import redirect
from flask import session
from flask import render_template
import mysql.connector

app = Flask(__name__)

app.secret_key = b'\xe0\xab/0\xd04\xa7l\xf95\xd0\xdc="\x14\xa7'

sysdb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root"
)

mycursor = sysdb.cursor()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup/", methods=["POST"])
def signup():
    name = request.form["name"]
    account = request.form["account"]
    password = request.form["password"]
    existed_username = []

    query_get_userinfo = "SELECT * FROM website.user;"
    mycursor.execute(query_get_userinfo)
    user_info = mycursor.fetchall()

    for userinfo in user_info:
        username = userinfo[2]
        if username not in existed_username:
            existed_username.append(username)

    if account in existed_username:
        return redirect("/error/?message=帳號已經被註冊")
    else:
        query_create_user = "INSERT INTO website.user (name, username, password) VALUES (%s,%s,%s)"
        mycursor.execute(query_create_user, (name, account, password))
        sysdb.commit()
        return redirect("/")

@app.route("/signin/", methods=["POST"])
def signin():
    account = request.form["account"]
    password = request.form["password"]

    query_get_userinfo = "SELECT name,username,password FROM website.user;"
    mycursor.execute(query_get_userinfo)
    user_info = mycursor.fetchall()

    for userinfo in user_info:
        if account==userinfo[1] and password==userinfo[2]:
            session["account"] = account
            return redirect(f"/member/?name={userinfo[0]}")
    return redirect("/error/?message=帳號或密碼輸入錯誤")

@app.route("/signout")
def signout():
    session.pop("account", None)
    return redirect("/")

@app.route("/member/")
def member_info():
    if 'account' in session:
        name = request.args.get("name", None)
        return render_template("member.html", name=name)
    else:
        return redirect("/")

@app.route("/error/")
def error():
    message = request.args.get("message", None)
    return render_template("error.html", message=message)

app.run(port=3000)