from flask import Flask, redirect, render_template, request, url_for, session
from db import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config

connection = create_connection("localhost", "root", "password", "photoshare")

@app.route('/')
def hello():
    #Session Control:
    session['logged_in'] = False
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('Home.html')

    return render_template('Home.html', friendlist=friendslist,friendrecommendationlist=friendrecommendationlist)

@app.route('/home')
def home():
    if session.get('logged_in') == True:
        friendslist = get_friend_list(session.get('user_id'))
        print(friendslist)
        friendrecommendationlist = ["ryan", "spencer", "mia", "alex"]

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
        register_user(first_name=firstname,last_name=lastname,email=email,hometown=hometown,date_of_birth=dob,password=password,gender=gender)
        return redirect(url_for('login'))
    else:
        redirect(url_for('login'))
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        print("before request")
        email = request.form['loginemail']
        print(email)
        password = request.form['loginpassword']
        try:
            print("In the try")
            loginQuery(email=email,password=password)
            return redirect(url_for('home'))

        except:
            print("Invalid Login")
            return redirect(url_for('login'))


@app.route('/UserSearch', methods=['GET','POST'])
def UserSearch():
    if request.method == 'POST':
        userSearch = request.form['searchuser']
        return redirect(url_for('searchUser'))
    
    return render_template('UserSearch.html')

@app.route('/PhotoSearch', methods=['GET','POST'])
def Search():
    if request.method == 'POST':
        photoSearch = request.form['searchphoto']
        return redirect(url_for('searchPhoto'))
    
    return render_template('PhotoSearch.html')
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