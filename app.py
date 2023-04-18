from flask import Flask, redirect, render_template, request, url_for
import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(host=host_name,user=user_name,password=user_password)
        print("Connection to MYSQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


connection= create_connection('http://127.0.0.1', 'root', 'secret')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config

@app.route('/')
def hello():
    # return '<h1>testing</h1>'
    friendslist = ["betty","chris","paul","josh"]
    friendrecommendationlist = ["ryan","spencer","mia","alex"]

    return render_template('Home.html', friendlist=friendslist,friendrecommendationlist=friendrecommendationlist)


@app.route('/AccountInfo')
def displayInfo():
    return render_template('account.html',userid='userid',firstname='firstname',lastname='lastname',email='email',dateofbirth='dateofbirth',hometown='hometown',gender='gender')
    
@app.route('/ChangeInfo', methods=['GET','POST'])
def ChangeInfo():

    if classmethod == 'POST':
        value = request.form['Options']
        text = request.form['info']
    return render_template('changeInfo.html')
    
@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':
        firstname = request.form['registerFirstName']
        lastname = request.form['registerLastName']
        email = request.form['registeremail']
        hometown = request.form['registerHometown']
        dob = request.form['registerDOB']
        password = request.form['registerPassword']
        password_confirm = request.form['registerConfirmPasswordPassword']
        gender = request.form['registerGender']

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['loginemail']
        password = request.form['loginpassword']


    return render_template('login.html')

@app.route('/Search', methods=['GET','POST'])
def Search():
    if request.method == 'POST':
        userSearch = request.form['searchuser']
        photoSearch= request.form['searchphoto']

        return redirect(url_for('searchUser'))
    
    return render_template('Search.html')

@app.route('/SearchUser')
def searchUser():
    return render_template('SearchUser.html', value="useremail@example.com")

@app.route('/SearchPhoto')
def searchPhoto():
    return render_template('SearchPhotos.html')

@app.route('/TopUsers')
def listUsers():
    return render_template('topUsers.html', user1 ="user1", user2 = "user2", user3="user3", user4="user4", user5 ="user5")


if __name__ == '__main__':
    app.debug = True
    app.run()