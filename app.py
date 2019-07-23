from flask import Flask, render_template, request, session, redirect, url_for
from binascii import hexlify
import os
from pymongo import MongoClient

client = MongoClient()
db = client.MyBlogDB
users = db["users"]
posts = db["posts"]

app = Flask(__name__)
app.secret_key = hexlify(os.urandom(10))

def generateErrTemplate(err):
    print(err)
    return render_template('error.html',err=err)

def UserName_Exists(username):
    if users.count_documents({"UserName" : username}) == 0:
        return False
    else:
        return True

def Email_Exists(email):
    if users.count_documents({"Email" : email}) == 0:
        return False
    else:
        return True

def loggingin(username,password):
    print(username,password)
    if UserName_Exists(username):
        user = users.find_one({"UserName" : username})
        pw = user["Password"]
        if password == pw:
            session["UserName"] = username
            return (redirect(url_for('index')))
        else:
            return generateErrTemplate("Wrong Password!")
    else:
        return generateErrTemplate("UserName Doesn't Exist!")

def check_logged_in():
    if "UserName" in session:
        return session["UserName"]
    else:
        return False

@app.route('/',methods=['GET','POST'])
def index():
    LoggedIn = check_logged_in()
    if (request.method == "GET") or (request.method == "POST"):
        return render_template('index.html',db=db,LoggedIn=LoggedIn)
    else:
        return generateErrTemplate("Bad Request!")

@app.route('/register',methods=['POST'])
def register():
    if request.method == "POST":
        type = request.form["type"]
        if type == "register":
            email = request.form["RegisterEmail"]
            username = request.form["RegisterUserName"]
            password = request.form["RegisterPassword"]
            if UserName_Exists(username) or Email_Exists(email):
                return generateErrTemplate("UserName/Email Already Exists!")
            userAcc = {"UserName":username, "Email":email, "Password":password}
            users.insert_one(userAcc)
            return loggingin(username,password)
    else:
        return generateErrTemplate("Bad Request!")

@app.route('/login',methods=['POST'])
def login():
    if request.method == "POST":
        type = request.form["type"]
        if type == "login":
            username = request.form["LoginUserName"]
            password = request.form["LoginPassword"]
            return loggingin(username,password)
    else:
        return generateErrTemplate("Bad Request!")

@app.route('/logout',methods=['POST'])
def logout():
    if request.method == "POST":
        type = request.form["type"]
        if type == "logout":
            session.clear()
            return index()
    else:
        return generateErrTemplate("Bad Request!")

if __name__ == '__main__':
    app.run(debug=True)
