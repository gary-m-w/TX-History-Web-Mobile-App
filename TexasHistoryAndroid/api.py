import pymongo
from bson import ObjectId
from flask import Flask, Blueprint, jsonify
from flask_googlemaps import GoogleMaps
from flask import Flask, render_template, request, jsonify, session
import pymongo
from bson import ObjectId
from passlib.hash import pbkdf2_sha256
from dash import dashboard
from post import create_post
from user import get_user_posts
from homepage import index
from themes import show_all_themes
from themes import create_theme
from themes import search_theme
from flask_googlemaps import GoogleMaps
from map import create_map
from signup import signup_process
import requests
from flask import render_template, jsonify
from flask_googlemaps import Map
from datetime import datetime
from flask import render_template, request, redirect, session, jsonify
import os
from google.cloud import storage
import time

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "apad_account.json"

storage_client = storage.Client()

# package
apisetup = Blueprint('api', __name__)

app = Flask(__name__)
app.secret_key = "texasHistoryProject"

cluster = "mongodb+srv://apad:AustinTexas@cluster0.xwix9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(cluster)
db = client.TexasHistory

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyCAjrVBxmhis9XRZ4f3fspvlOCKeKt6dIk"
# Initialize the extension
GoogleMaps(app)
# API Key for Google maps
API_KEY = "AIzaSyCAjrVBxmhis9XRZ4f3fspvlOCKeKt6dIk"


# add homepage/login
# create a post
@apisetup.route('/', methods=['GET', 'POST'])
def index():
    # send user to homepage
    if request.method == 'GET':
        # return render_template('index.html')
        return jsonify()

    else:
        # get long information and send to user to the dashboard
        # verify login information
        # user name password
        # return redirect('dashboard.html')
        return jsonify()

@app.route('/login_form', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    else:
        user = db.user.find_one({"email": request.form.get('email')})
        names = user['name']
        email = request.form.get("email")
        session["user"] = email
        if user and pbkdf2_sha256.verify(request.form.get('pwd'), user['password']):
            # return redirect('/dashboard')
            return jsonify()
        else:
            error = "Invalid login credentials"
            # return render_template('login.html', error=error)
            return jsonify()


@app.route('/signup_form', methods=['GET', 'POST'])
def signup_process():
    if request.method == 'GET':
        return jsonify()
        # return render_template('home.html')

    else:

        # Create the user object
        user = {
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('pwd')
        }
        email = request.form.get("email")
        session["user"] = email
        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Check for existing email address
        if db.user.find_one({"email": user['email']}):
            error = "Email address already in use"
            # return render_template('home.html', error=error)
            return jsonify({'error': "Email address already in use"})

        db.user.insert_one(user)

        # return redirect('/dashboard')
        return jsonify()


@apisetup.route('/post', methods=['GET', 'POST'])
def create_post():
    # get all posts
    if request.method == 'GET':
        A = db['theme']
        theme = list(A.find({}))
        print(theme)
        theme = translate(theme)
        # query all posts
        # return render_template('post.html', themes=theme)
        return jsonify(theme)

    else:
        # bind data from the form into the database
        title = request.form.get("title")
        description = request.form.get("description")
        file = request.files['image']
        theme = request.form.get("theme")
        tag = request.form.get("tag")
        address = request.form.get("location")
        city = request.form.get("locality")
        state = request.form.get("administrative_area_level_1")
        array_tag = tag.split(", ")
        date = datetime.now()
        if "user" in session:
            user = session["user"]

        try:

            save_post = {"title": title, "description": description, "theme": theme, "tag": array_tag, "date": date,
                         "user": user, "address": address, "city": city, "state": state}
            post_db = db.post
            post_db.insert_one(save_post)
            new_post = db.post.find_one(
                {"title": title, "description": description, "theme": theme, "tag": array_tag, "date": date,
                 "user": user, "address": address, "city": city, "state": state})
            print(new_post)
            time.sleep(1)
            upload_file_to_bucket(str(new_post.get('_id')), file)

            bucket_link = "https://storage.cloud.google.com/texas_history_apad/" + str(new_post.get('_id'))
            db.post.update({"_id": new_post.get('_id')}, {"$set": {"image": bucket_link}})

            # return redirect('/dashboard')
            return jsonify()
        except Exception as e:
            print(e)
            # return "Oops, an error has occured! Please try again later"
            return jsonify()


def upload_file_to_bucket(name, file):
    # upload files
    try:
        bucket = storage_client.get_bucket('texas_history_apad')
        blob = bucket.blob(name)
        blob.upload_from_file(file)
    except Exception as e:
        print("BIG ERROR", e)
        return False

# Take user to profile page where they can see their posts and subscribed themes
@apisetup.route('/user', methods=['GET'])
def get_user_posts():
    if request.method == 'GET':
        if "user" in session:
            user = session["user"]
        # query all posts
        posts = list(db.post.find({"user": user}))

        # find user in db to display subscribed themes
        find_user = list(db.user.find({"email": user}))

        find_user = translate(find_user)
        posts = translate(posts)
        # return render_template('profile.html', posts=posts, find_user=find_user)
        return jsonify(posts, find_user)


# send the user to the dashboard with all of the posts ordered from newest to oldest
# post: query of search results from posts
@apisetup.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # query all posts for the tag
        search_tag = request.form.get("search_tag")
        filtered_posts = list(db.post.find({"tag": search_tag}))
        filtered_posts = translate(filtered_posts)
        # filtered_posts = db.post.find({"tag": [search_tag]}).sort('date', pymongo.DESCENDING)
        #return render_template('dashboard.html', all_posts=filtered_posts)
        return jsonify(filtered_posts)

    else:
        # get all posts from database'
        all_posts = list(db.post.find().sort('date', pymongo.DESCENDING))
        all_posts = translate(all_posts)
        #return render_template('dashboard.html', all_posts=all_posts)
        return jsonify(all_posts)


# returns an html page with details from a specified post from dashboard
@apisetup.route('/details/<string:post_id>', methods=['GET'])
def details(post_id):
    post = list(db.post.find({"_id": ObjectId(post_id)}))
    # post[0]["_id"]=str(post[0]["_id"])
    print(post)
    post = translate(post)
    # return render_template('post_details.html', post=post)
    return jsonify(post)

@apisetup.route('/themes', methods=['GET', 'POST'])
# Theme.show_all_themes
def show_all_themes():
    if "user" in session:
        user = session["user"]
    if request.method == 'POST':
        theme_subscribed =  request.form.get("theme")
        user_object = db.user.find({"email": user})
        already_sub = False
        for theme in user_object[0]["themes"]:
            if theme_subscribed == theme:
                already_sub = True
        if not already_sub:
            db.user.update({ "email": user },{ "$push": { "themes": theme_subscribed }})
        # return redirect('/themes')
        return jsonify()
    else:
        admin_access = list(db.user.find({"$and": [{ "email": user }, { "admin": "yes"}]}))
        all_themes = list(db.theme.find().sort('label', pymongo.ASCENDING))
        A= db['theme']
        theme = list(A.find({}))
        print(theme)
        # query all posts
        # return render_template('theme.html', all_themes=all_themes, cover='cover',admin_access=admin_access,theme=theme)
        all_themes = translate(all_themes)
        admin_access = translate(admin_access)
        theme = translate(theme)
        return jsonify(all_themes, admin_access, theme)


@apisetup.route('/new_theme', methods=['GET', 'POST'])
def create_theme():
    if request.method == 'GET':
        # return render_template('new_theme.html')
        return jsonify()
    else:
        label = request.form.get("label")
        cover = request.form.get("cover")
        new_theme = {'label': label, 'cover': cover}
        theme_query = {'label': label}
        result = db.theme.find_one(theme_query)

        if result is None:
            db.theme.insert_one(new_theme)
            # return redirect('/themes')
            return jsonify()
        else:
            # return "Already exists. Reload the page."
            return jsonify({'error': "Already exists. Reload the page."})


@apisetup.route('/theme_search', methods=['GET', 'POST'])
def search_theme():
    if request.method == 'POST':
        # query all posts by theme
        search_theme = request.form.get("search_theme")
        if "user" in session:
            user = session["user"]
            user_object = db.user.find({"email": user})
            already_sub = False
            for theme in user_object[0]["themes"]:
                if search_theme == theme:
                    already_sub = True
        A = db['theme']
        theme = list(A.find({}))
        print(theme)
        if search_theme != "all":
            filtered_posts = list(db.post.find({"theme": search_theme}))
        else:
            filtered_posts = list(db.post.find())
        filtered_posts = translate(filtered_posts)
        theme = translate(theme)
        # return render_template('theme_search.html', all_posts=filtered_posts, search_theme=search_theme, theme=theme, already_sub=already_sub)
        return jsonify(filtered_posts, {'search_theme': search_theme}, theme, {'already_sub': already_sub})
    else:
        # get all posts from database'
        all_posts = list(db.post.find().sort('date', pymongo.DESCENDING))
        all_posts = translate(all_posts)
        # return render_template('theme_search.html', all_posts=all_posts)
        return jsonify(all_posts)


@app.route('/map', methods=['GET', 'POST'])
def mapview():
    return jsonify()

def translate(objects):
    for object in range(0, len(objects)):
        objects[object]["_id"] = str(objects[0]["_id"])
    return objects
