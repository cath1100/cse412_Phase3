from flask import Flask, redirect, render_template, request, url_for, session
from db import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config

connection = create_connection("localhost", "root", "password", "photoshare")

#global variable declaration
testEmail = "was not"
testUserID = "-1"

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

        # print(friendslist)
        friendrecommendationlist = friendrecommendationsQuery(session.get('user_id'))
        feed = photofeed()
        print(feed[0])
        commentfeed = []
        friendlikes = []
        friendlikesCount = []
        print(commentfeed)
        for photo in feed:
            commentfeed += get_photo_comments(photo[4])
            friendlikesCount += get_photo_like_count(photo[4])

        return render_template('Home.html', friendlist=friendslist, friendrecommendationlist=friendrecommendationlist,
                               feed=feed, commentfeed=commentfeed, friendlikes=friendlikes,
                               friendlikesCount=friendlikesCount)


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
        global testEmail
        global testUserID
        userSearch = request.form['searchuser']
        try:
            results = search_user(userSearch)
            testUserID = results[0][0]
            testEmail = userSearch
            return redirect(url_for('searchUser'))
        except:
            print("user not found")
            return redirect(url_for('UserSearch'))
    
    return render_template('searches/UserSearch.html')

@app.route('/PhotoSearch', methods=['GET','POST'])
def Search():
    if request.method == 'POST':
        photoSearch = request.form['searchphoto']
        return redirect(url_for('searchPhoto'))
    
    return render_template('searches/PhotoSearch.html')

@app.route('/SearchUser')
def searchUser():
    friendID = get_user_info(testUserID)
    print(friendID[0][0])
    userID = get_user_info(session.get('user_id'))
    print(userID[0][0])
    results = add_friend(friendID[0][0],userID[0][0])
    return render_template('searches/SearchUser.html', value=testEmail)

@app.route('/SearchPhoto')
def searchPhoto():
    return render_template('searches/SearchPhotos.html')

@app.route('/TopUsers')
def listUsers():
    results = user_contribution_score()
    print(results)
    return render_template('topUsers.html', user1 =results[0], user2 = results[1], user3=results[2], user4=results[3], user5 =results[4])


@app.route('/postphoto',methods=["POST","GET"])
def postphoto():
    if request.method == "GET":
        albums = get_albums_for_user(session.get('user_id'))
        return render_template('postphoto.html', albums=albums)
    if request.method == "POST":
        caption = request.form['caption']
        data = request.files['photodata'].filename
        print(data)
       # databin = convertToBinaryData(data)
        album_id = request.form['album_id']
        results = upload_photo(caption, data, album_id)
        return redirect(url_for('home'))


@app.route('/addalbum', methods=["POST"])
def addalbums():

    if request.method == "POST":
        albumname = request.form['albumname']

        addalbumQuery(albumname,session.get('user_id'))
        return redirect(url_for('postphoto'))
    else:
        return redirect((url_for('postphoto')))

@app.route('/updatelike',methods=['POST'])
def updateLikes():
    if request.method == "POST":
        photo_id = request.values['photo_id']
        add_like(photo_id,session.get('user_id'))
        return redirect((url_for('home')))




@app.route('/commentsearch', methods=["POST","GET"])
def commentSearch():
    if request.method == "GET":
        return render_template('searches/searchcomment.html')
    if request.method == "POST":
        comment = request.form['searchcomment']
        results = search_comments(comment)
        print(results)
        return render_template('searches/searchcomment.html')


if __name__ == '__main__':
    app.debug = True
    app.run()