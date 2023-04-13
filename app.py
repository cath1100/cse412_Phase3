from flask import Flask, render_template, request
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
    return render_template('Home.html')


@app.route('/AccountInfo')
def displayInfo():
    return render_template('account.html')
    
@app.route('/ChangeInfo')
def ChangeInfo():
    return render_template('changeInfo.html')
    
@app.route('/register', methods=['GET','POST'])
def register():

    if classmethod == 'POST':
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

    if classmethod == 'POST':
        email = request.form['loginemail']
        password = request.form['loginpassword']


    return render_template('login.html')





if __name__ == '__main__':
    app.debug = True
    app.run()