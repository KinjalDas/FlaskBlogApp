from flask import Flask, render_template, request
from pymongo import MongoClient

client = MongoClient()
db = client.MyBlogDB
users = db["users"]
posts = db["posts"]

app = Flask(__name__)

def generateErrTemplate(err):
    return render_template('error.html',err=err)

def UserName_or_Email_Exists(username,email):
    if ((username != None) and (users.find({"UserName" : username}).count()) == 0):
        return False
    elif ((email != None) and (users.find({"Email" : email}).count()) == 0):
        return False
    else:
        return True

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method == "GET":
        return render_template('index.html',db=db)
    if request.method == "POST":
        type = request.form["type"]
        if type == "register":
            email = request.form["RegisterEmail"]
            username = request.form["RegisterUserName"]
            password = request.form["RegisterPassword"]
            if (UserName_or_Email_Exists(username,email):
                generateErrTemplate("UserName/Email Already Exists!")

        return render_template('index.html',register_or_login_page=True,db=db,type=type)



if __name__ == '__main__':
    app.run(debug=True)
