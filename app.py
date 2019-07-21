from flask import Flask, render_template, request
from pymongo import MongoClient

client = MongoClient()
db = client.MyBlogDB

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method == "GET":
        return render_template('index.html',db=db)

@app.route('/register_or_login',methods=['GET','POST'])
def register_or_login():
    if request.method == "GET":
        return render_template('register_login.html',register_or_login_page=True,db=db)



if __name__ == '__main__':
    app.run()
