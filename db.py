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
    results1 = execute_read_query(connection, query)
    name = results1[0][1]
    user_id = str(results1[0][2])
    date_of_creation = results1[0][3]
    return results1
    query = f'SELECT * FROM photos WHERE album_id = "{album_id}"'
    results = execute_read_query(connection, query)
    #return results
    for photo in results:
        photo_url = photo[2].decode()
        print(photo_url)


# ===============================================================================
def get_photo_likes(photo_id):
    global connection
    query = f'SELECT * FROM likes WHERE photo_id = "{photo_id}"'
    results = execute_read_query(connection, query)
    return results
    count = 0
    likedby = []
    # for like in results:
    #     count = count + 1
    #     print(like)
    #     likedby += str(get_user_info(str(like[0]))[0] + get_user_info(str(like[0]))[1])
    #     print(likedby)
    #     #print(liked_by)
    #
    # for liked in likedby:
    #     print(liked)
    #
    # return likedby

# ===============================================================================
def get_photo_like_count(photo_id):
    global connection
    query = f'SELECT COUNT(*),likes.photo_id FROM likes WHERE photo_id = {photo_id}'
    results = execute_read_query(connection, query)
    return results
    print(results[0][0])


# ===============================================================================
def get_photo_comments(photo_id):
    global connection
    query = f'SELECT * FROM comments WHERE photo_id = "{photo_id}"'
    results = execute_read_query(connection, query)
    return results
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
    now = datetime.datetime.now()
    query = f'SELECT * FROM comments WHERE photo_id = "{photo_id}" AND user_id = "{user_id}"'
    results = execute_read_query(connection,query)
    if (results):
        print("user has already commented on this photo")
    else:
        query = (f'INSERT INTO comments (photo_id, date_of_comment, user_id, text)'
                 f'VALUES ("{photo_id}", "{now.strftime("%Y-%m-%d %H:%M:%S")}", "{user_id}", "{text}")')
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
    print(list)
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
    query = (f'''SELECT DISTINCT f2.user_id AS recommended_friend, 
    COUNT(*) AS mutual_friends FROM Friends f1 
    JOIN Friends f2 ON f1.friend_id = f2.friend_id WHERE f1.user_id = "{user_id}" AND f2.user_id <> "{user_id}" 
    GROUP BY f2.user_id HAVING COUNT(*) > 1 ORDER BY mutual_friends DESC''')
    results = execute_read_query(connection, query)
    list = []
    for friend in results:
        list.append(get_user_info(str(friend[0]))[0][3])
    return list

#================================================================================
def add_friend(user_id,friend_id):
    global connection
    current_time = date.today().strftime("%m/%d/%y") 
    query = f'INSERT INTO Friends(user_id,friend_id,date_of_friendship) VALUES ("{user_id}","{friend_id}","{current_time}")'
    results = execute_query(connection, query)

#================================================================================
def photofeed():
    global connection
    queryfinal = f'SELECT users.first_name, users.last_name, photos.data, photos.caption, photos.photo_id FROM users JOIN albums ON users.user_id = albums.user_id JOIN photos ON photos.album_id = albums.album_id order by photos.photo_id ASC'
    query = f'SELECT * FROM Photos order by photo_id ASC'
    results = execute_read_query(connection, queryfinal)
    print(results)
    return results
   # print(query)

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
    query = f'SELECT u.user_id, u.first_name, u.last_name, COUNT(p.photo_id) + COUNT(c.comment_id) AS contribution_count FROM Users u LEFT JOIN Photos p ON u.user_id = p.user_id LEFT JOIN Comments c ON u.user_id = c.user_id GROUP BY u.user_id, u.first_name, u.last_name ORDER BY contribution_count DESC LIMIT 10'
    results = execute_query(connection, query)
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
def load_userinfo_from_albumID(album_id):
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
    return results
  
#================================================================================
def search_user(user):
    global connection
    query = f'SELECT user_id FROM users WHERE email = "{user}"'
    results = execute_read_query(connection, query)
    return results


#================================================================================
def search_by_tag(tags):
    global connection
    tag_list = tags.split(" ")
    tag_count = len(tag_list)
    tag_list = tag_list[:5] + [""] * (5 - len(tag_list))
    query = (f'''SELECT u.first_name, u.last_name, p.data, p.caption, p.photo_id
                 FROM Photos p
                 JOIN Tags t ON p.photo_id = t.photo_id
                 JOIN Albums a ON p.album_id = a.album_id
                 JOIN Users u ON u.user_id = a.user_id
                 WHERE t.text IN ('{tag_list[0]}', '{tag_list[1]}' , '{tag_list[2]}' ,'{tag_list[3]}' ,'{tag_list[4]}') 
                 GROUP BY p.photo_id
                 HAVING COUNT(*) = {tag_count} ''')
    results = execute_read_query(connection, query)
    #list = []
    #for photo in results:
    #    list.append(photo[2])
    #print(list)
    return results
#================================================================================
def search_comments(text):
    global connection
    print(text)
    query = f'SELECT c.text, c.photo_id, u.first_name, u.last_name, p.data FROM Comments c JOIN users u ON c.user_id=u.user_id JOIN photos p ON p.photo_id = c.photo_id WHERE c.text="{text}" AND c.photo_id=p.photo_id'
    results = execute_read_query(connection,query)
    print("Results for Comments: "+str(results))
    return results
#================================================================================

def load_photo(album):
    global connection
    query = f'SELECT * FROM photos p WHERE p.album_id = "{album}"'
    results = execute_read_query(connection, query)
    return results
#================================================================================
def search_by_tag_user(tags, user_id):
    global connection
    tag_list = tags.split(" ")
    tag_count = len(tag_list)
    tag_list = tag_list[:5] + [""] * (5 - len(tag_list))
    query = (f'''SELECT u.first_name, u.last_name, p.data, p.caption, p.photo_id
                 FROM Photos p
                 JOIN Tags t ON p.photo_id = t.photo_id
                 JOIN Albums a ON p.album_id = a.album_id
                 JOIN Users u ON u.user_id = a.user_id
                 WHERE t.text IN ('{tag_list[0]}', '{tag_list[1]}' , '{tag_list[2]}' ,'{tag_list[3]}' ,'{tag_list[4]}') 
                 AND a.user_id = "{user_id}"
                 GROUP BY p.photo_id
                 HAVING COUNT(*) = {tag_count} ''')
    results = execute_read_query(connection, query)
    return results

#================================================================================
def top_tags():
    global connection
    query = "SELECT text, COUNT(*) AS tag_count FROM Tags GROUP BY text ORDER BY tag_count DESC;"
    results = execute_read_query(connection, query)
    print(results)
    return results

#================================================================================
def reccomended_photos(user_id):
    global connection
    query = (f'''SELECT u.first_name, u.last_name, p.data, p.caption, p.photo_id, COUNT(*) AS num_tags
                                  FROM Photos p
                                  INNER JOIN Tags t ON p.photo_id = t.photo_id
                                  INNER JOIN Albums a on p.album_id = a.album_id
                                  INNER JOIN Users u on u.user_id = a.user_id
                                  WHERE t.text IN (
                                  SELECT text
                                  FROM Tags
                                  WHERE photo_id IN (
                                  SELECT photo_id
                                  FROM Photos
                                  LEFT JOIN Albums on Albums.album_id = Photos.album_id
                                  WHERE user_id = {user_id}
                                  )
                                  GROUP BY text
                                  ORDER BY COUNT(*) DESC
                                  )
                                  GROUP BY p.photo_id, p.caption
                                  ORDER BY num_tags DESC, COUNT(*) ASC''')
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
#search_by_tag_user("music", "1")
#top_tags()
#friendrecommendationsQuery("1")
#photofeed()