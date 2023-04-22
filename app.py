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
        friendrecommendationlist = friendrecommendationsQuery(session.get('user_id'))
        feed = photofeed()
        print("Feed: "+ str(feed))
        print(friendrecommendationlist)

        return render_template('Home.html', friendlist=friendslist,friendrecommendationlist=friendrecommendationlist, feed=feed)



@app.route('/AccountInfo')
def displayInfo():
    results = get_user_info(session.get('user_id'))
    print(results)

    return render_template('account.html',userid=session.get('user_id'),firstname=results[0][1],lastname=results[0][2],email=results[0][3],dateofbirth=results[0][5],hometown=results[0][4],gender=results[0][7])
    
@app.route('/ChangeInfo', methods=['GET','POST'])
def ChangeInfo():

    if request.method == 'POST':
        option = request.form['Options']
        answer = request.form['info']

        if option == '1':
            update_first_name(answer,session.get('user_id'))
        if option == '2':
            update_last_name(answer,session.get('user_id'))
        if option == '4':
            update_hometown(answer,session.get('user_id'))
        if option == '5':
            update_date_of_birth(answer,session.get('user_id'))
        if option == '7':
            update_gender(answer,session.get('user_id'))
        return redirect(url_for("displayInfo"))
    if request.method == "GET":
        return render_template('changeInfo.html')
    
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
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
    
    return render_template('searches/UserSearch.html')

@app.route('/PhotoSearch', methods=['GET','POST'])
def Search():
    if request.method == 'POST':
        photoSearch = request.form['searchphoto']
        return redirect(url_for('searchPhoto'))
    
    return render_template('searches/PhotoSearch.html')
@app.route('/SearchUser')
def searchUser():
    return render_template('searches/SearchUser.html', value="useremail@example.com")

@app.route('/SearchPhoto')
def searchPhoto():
    return render_template('searches/SearchPhotos.html')

@app.route('/TopUsers')
def listUsers():
    #results = user_contribution_score()
    #print(results)
    return render_template('topUsers.html', user1 ="user1", user2 = "user2", user3="user3", user4="user4", user5 ="user5")


@app.route('/postphoto',methods=["POST","GET"])
def postphoto():
    if request.method == "GET":
        albums = get_albums_for_user(session.get('user_id'))
        return render_template('postphoto.html', albums=albums)
    if request.method == "POST":
        caption = request.form['caption']
        data = request.files['photodata'].stream
        print(data)
       # databin = convertToBinaryData(data)
        album_id = request.form['album_id']
        #results = upload_photo(caption, data, album_id)
        return redirect(url_for('home'))


@app.route('/addalbum', methods=["POST"])
def addalbums():

    if request.method == "POST":
        albumname = request.form['albumname']

        addalbumQuery(albumname,session.get('user_id'))
        return redirect(url_for('postphoto'))
    else:
        return redirect((url_for('postphoto')))





def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

if __name__ == '__main__':
    app.debug = True
    app.run()