from flask import Flask, json
from flask import request
from flask import redirect
from flask import session
from flask import render_template
from flask import jsonify
import mysql.connector

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

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

    query_get_userinfo = "SELECT * FROM website.user WHERE username = (%s);"
    mycursor.execute(query_get_userinfo, (account,))
    user_info = mycursor.fetchall()

    if user_info != []:
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

    query_get_userinfo = "SELECT name,username,password FROM website.user WHERE username=(%s) AND password=(%s);"
    mycursor.execute(query_get_userinfo, (account, password))
    user_info = mycursor.fetchall()

    if user_info != []:
        session["account"] = account
        return redirect(f"/member/?name={user_info[0][0]}")
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

@app.route("/api/users")
def api_users():
    username = request.args.get("username", None)
    query_get_userinfo = "SELECT * FROM website.user WHERE username = (%s);"
    mycursor.execute(query_get_userinfo, (username,))
    user_info = mycursor.fetchall()

    if user_info != []:
        return jsonify({"data": {
                                    "id": user_info[0][0],
                                    "name": user_info[0][1],
                                    "username": user_info[0][2]
                                }
                        })
    else:
        return jsonify({"data": None})

@app.route("/api/user", methods=["POST"])
def api_user():
    current_user = session["account"]
    request_name = request.get_json()["name"]
    
    query_modify_name = "UPDATE website.user SET name = (%s) WHERE username = (%s);"
    mycursor.execute(query_modify_name, (request_name, current_user))
    sysdb.commit()

    query_check = "SELECT * FROM website.user WHERE name = (%s) AND username = (%s);"
    try:
        mycursor.execute(query_check, (request_name, current_user))
        check = mycursor.fetchall()
        if check != []:
            return jsonify({"ok": True})
        else:
            return jsonify({"error": False})
    except:
        return jsonify({"error": True})

app.run(port=3000)