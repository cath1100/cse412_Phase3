import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime, date
from flask import session, redirect, url_for
import datetime

# ===============================================================================
# tutorial: https://realpython.com/python-sql-libraries/#mysql
global connection


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name)
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection




def execute_query(connection, query):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


# ===============================================================================
def loginQuery(email, password):
    global connection
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    query = f'SELECT user_id FROM users WHERE email = "{email}" AND hashed_password = "{password}"'
    results = execute_read_query(connection, query)
    if (results):
        print(f'Login for {email} successful.')
        print(results)
        session['user_id'] = results[0][0]
        session['logged_in'] = True
        print(session['user_id'])
        # redirect to homepage
        redirect(url_for('home'))
    else:
        query = f'SELECT user_id FROM users WHERE email = "{email}"'
        results = execute_read_query(connection, query)
        if (results):
            print(results)
            print("Login failed: incorrect password")
        else:
            print(results)
            print("Login failed: incorrect email or account does not exist")


# ===============================================================================
def register_user(first_name, last_name, email, hometown, date_of_birth, password, gender):
    global connection
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    query = f'SELECT * FROM users WHERE email = "{email}"'
    results = execute_read_query(connection, query)
    if (results):
        print("User already registered")
    else:
        query = (f'INSERT INTO users (first_name, last_name, email, hometown, date_of_birth, hashed_password, gender)'
                 f'VALUES ("{first_name}", "{last_name}", "{email}", "{hometown}", "{date_of_birth}", "{password}", "{gender}")')
        results = execute_query(connection, query)
        print(f'User {email} successfully registered')
        return redirect(url_for('login'))
        # redirect


# ===============================================================================
def upload_photo(caption, data, album_id):
    global connection
    query = (f'INSERT INTO photos (caption, data, album_id)'
             f'VALUES ("{caption}", "{data}", "{album_id}")')
    results = execute_query(connection, query)


# ===============================================================================
def load_album(album_id):
    global connection
    query = f'SELECT * FROM albums WHERE album_id = "{album_id}"'
    results = execute_read_query(connection, query)
    name = results[0][1]
    user_id = str(results[0][2])
    date_of_creation = results[0][3]
    query = f'SELECT * FROM photos WHERE album_id = "{album_id}"'
    results = execute_read_query(connection, query)
    for photo in results:
        photo_url = photo[2].decode()
        print(photo_url)


# ===============================================================================
def get_photo_likes(photo_id):
    global connection
    query = f'SELECT * FROM likes WHERE photo_id = "{photo_id}"'
    results = execute_read_query(connection, query)
    count = 0
    for like in results:
        count = count + 1
        liked_by = get_user_info(str(like[0]))[0][1]
        print(liked_by)


# ===============================================================================
def get_photo_like_count(photo_id):
    global connection
    query = f'SELECT COUNT(*) FROM likes WHERE photo_id = {photo_id}'
    results = execute_read_query(connection, query)
    print(results[0][0])


# ===============================================================================
def get_photo_comments(photo_id):
    global connection
    query = f'SELECT * FROM comments WHERE photo_id = "{photo_id}"'
    results = execute_read_query(connection, query)
    for comment in results:
        print("Comment: " + comment[4] + " left by user " + get_user_info(str(comment[2]))[0][1] + " at " + comment[1])


# ===============================================================================
def get_user_info(user_id):
    global connection
    query = f'SELECT * FROM users WHERE user_id = "{user_id}"'
    return execute_read_query(connection, query)


# ===============================================================================
def add_comment(photo_id, user_id, text):
    global connection
    query = f'SELECT * FROM comments WHERE photo_id = "{photo_id}" AND user_id = "{user_id}"'
    results = execute_read_query(connection, query)
    if (results):
        print("user has already commented on this photo")
    else:
        current_time = date.today().strftime("%m/%d/%y") + " " + datetime.now().strftime("%H:%M:%S")
        query = (f'INSERT INTO comments (photo_id, date_of_comment, user_id, text)'
                 f'VALUES ("{photo_id}", "{current_time}", "{user_id}", "{text}")')
        execute_query(connection, query)


# ===============================================================================
def add_like(photo_id, user_id):
    global connection
    query = f'SELECT * FROM likes WHERE photo_id = "{photo_id}" AND user_id = "{user_id}"'
    results = execute_read_query(connection, query)
    if (results):
        print("user has already liked this photo")
    else:
        query = (f'INSERT INTO likes (user_id, photo_id)'
                 f'VALUES ("{user_id}", "{photo_id}")')
        execute_query(connection, query)


# ===============================================================================
def update_first_name(first_name, user_id):
    global connection
    query = f'UPDATE users SET first_name = "{first_name}" WHERE user_id = "{user_id}"'
    execute_query(connection, query)


# ===============================================================================
def update_last_name(last_name, user_id):
    global connection
    query = f'UPDATE users SET last_name = "{last_name}" WHERE user_id = "{user_id}"'
    execute_query(connection, query)


# ===============================================================================
def update_date_of_birth(date_of_birth, user_id):
    global connection
    query = f'UPDATE users SET date_of_birth = "{date_of_birth}" WHERE user_id = "{user_id}"'
    execute_query(connection, query)


# ===============================================================================
def update_hometown(hometown, user_id):
    global connection
    query = f'UPDATE users SET hometown = "{hometown}" WHERE user_id = "{user_id}"'
    execute_query(connection, query)


# ===============================================================================
def update_gender(gender, user_id):
    global connection
    query = f'UPDATE users SET gender = "{gender}" WHERE user_id = "{user_id}"'
    execute_query(connection, query)


# ===============================================================================
def update_password(password, user_id):
    global connection
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    query = f'UPDATE users SET hashed_password = "{password}" WHERE user_id = "{user_id}"'
    execute_query(connection, query)


# ===============================================================================
def get_friend_list(user_id):
    global connection
    query = f'SELECT friend_id,date_of_friendship FROM friends WHERE user_id = "{user_id}"'
    results = execute_read_query(connection, query)
    list = []
    for friend in results:
        list.append(get_user_info(str(friend[0]))[0][1])
    return list


# ===============================================================================
def most_popular_tags():
    global connection
    query = f'SELECT text, COUNT(*) AS c FROM Tags GROUP BY text ORDER BY c DESC'
    results = execute_read_query(connection, query)
    for tag in results:
        print(tag[0] + " has " + str(tag[1]) + " photos")


# ===============================================================================
def get_albums_for_user(user_id):
    global connection
    query = f'SELECT * FROM albums WHERE user_id = "{user_id}"'
    results = execute_read_query(connection, query)
    return results
    for album in results:
        print(album)


# ===============================================================================
def delete_photo(photo_id):
    global connection
    query = f'DELETE FROM Photos WHERE photo_id="{photo_id}"'
    execute_query(connection, query)


# ===============================================================================

def friendrecommendationsQuery(user_id):
    global connection
    query = f'SELECT DISTINCT f2.user_id AS recommended_friend, COUNT(*) AS mutual_friends FROM Friends f1 JOIN Friends f2 ON f1.friend_id = f2.friend_id WHERE f1.user_id = "{user_id}" AND f2.user_id <> "{user_id}" GROUP BY f2.user_id HAVING COUNT(*) > 1 ORDER BY mutual_friends DESC'
    results = execute_query(connection, query)
   # for friend in results:
    #    print(friend)

#================================================================================
def add_friend(user_id,friend_id):
    global connection
    query = f'INSERT INTO Friends(user_id,friend_id,date_of_friendship) VALUES ("{user_id}","{friend_id}",GETDATE())'
    results = execute_query(connection, query)

#================================================================================
def photofeed():
    global connection
    query = f'SELECT data FROM Photos order by photo_id ASC'
    results = execute_query(connection, query)
    print("Photo Feed:"+str(results))
    return results
    print(query)

#================================================================================

def addalbumQuery(name,user):
    global connection
    now = datetime.datetime.now()
    print(user)
    query = f'INSERT INTO Albums (name, user_id, date_of_creation) VALUES ("{name}","{user}","{now.strftime("%Y-%m-%d %H:%M:%S")}")'
    results = execute_query(connection, query)
    print(results)
#================================================================================

#Contribution Score:
def user_contribution_score():
    global connection
    query = ('''SELECT u.user_id, u.first_name, u.last_name, 
                COUNT(DISTINCT p.photo_id) AS photos_uploaded, 
                COUNT(DISTINCT c.comment_id) AS comments_left, 
                COUNT(DISTINCT p.photo_id) + COUNT(DISTINCT c.comment_id) AS total_contribution
                FROM Users u
                LEFT JOIN Albums a ON u.user_id = a.user_id
                LEFT JOIN Photos p ON u.user_id = a.user_id
                LEFT JOIN Comments c ON u.user_id = c.user_id
                GROUP BY u.user_id, u.first_name, u.last_name
                ORDER BY total_contribution DESC
                LIMIT 10; ''')
    results = execute_read_query(connection, query)
    list = []
    for user in results:
        list.append(user[1])
    return list

#================================================================================
def search_user(user):
    global connection
    query = f'SELECT user_id FROM users WHERE email = {user}'
    results = execute_read_query(connection, query)
    return results

#================================================================================
connection = create_connection("localhost", "root", "password", "photoshare")
# login("wilerRockAndRoll@gmail.com", "password10")
# register_user("hari", "ramalingame", "hramali1@asu.edu", "chicago", "05/09/2023", "password", "male")
# upload_photo("test", "https://cdn.discordapp.com/attachments/928074770015207494/1033824377214599178/unknown.png", "6")
# load_album("6")
# get_photo_likes("3")
# print(get_user_info("2")[0][1]) # gets username from id
# get_photo_comments("5")
# add_comment("1", "1", "test")
# add_like("1", "1")
# update_first_name("HARI", 11)
# get_photo_like_count("3")
# get_friend_list("1")
# most_popular_tags()
# get_albums_for_user("1")