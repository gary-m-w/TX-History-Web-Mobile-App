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
from api import apisetup
import requests
from flask import render_template, jsonify
from flask_googlemaps import Map

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

#
app.register_blueprint(apisetup, url_prefix='/api')

@app.route('/map', methods=['GET', 'POST'])
def mapview():
    return create_map(db)

@app.route('/signup_form', methods=['GET', 'POST'])
def signup():
    return signup_process(db)

# add homepage/login
# create a post
@app.route('/', methods=['GET', 'POST'])
def index_function():
    return index()


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

        # create a post


@app.route('/post', methods=['GET', 'POST'])
def post_function():
    return create_post(db)


# Take user to profile page where they can see their posts and subscribed themes
@app.route('/user', methods=['GET'])
def user_function():
    return get_user_posts(db)


# send the user to the dashboard with all of the posts ordered from newest to oldest
# post: query of search results from posts
@app.route('/dashboard', methods=['GET', 'POST'])
def dash_function():
    return dashboard(db)


# returns an html page with details from a specified post from dashboard
@app.route('/details/<string:post_id>', methods=['GET'])
def details(post_id):
    post = list(db.post.find({"_id": ObjectId(post_id)}))
    # return render_template('post_details.html', post=post)
    return jsonify(post)


@app.route('/file/<filename>')
def file(filename):
    # return db.post.send_file(filename)
    return jsonify()


# a user can see their created posted and themes they are subscribed to
@app.route('/profile')
def profile():
    # get all created posts from database for the user logged in
    # get all the themes that the user is subscribed to
    # pass these variables to the html file
    # return render_template('profile.html')
    return jsonify()


@app.route('/themes', methods=['GET', 'POST'])
# Theme.show_all_themes
def show_themes():
    return show_all_themes(db)


@app.route('/new_theme', methods=['GET', 'POST'])
def new_theme():
    return create_theme(db)


@app.route('/theme_search', methods=['GET', 'POST'])
def theme_search():
    return search_theme(db)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True, use_reloader=True)