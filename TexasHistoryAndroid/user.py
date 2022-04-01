
from flask import render_template, request, session, jsonify

def get_user_posts(db):
    if request.method == 'GET':
        if "user" in session:
            user = session["user"]
        # query all posts
        posts = list(db.post.find({"user": user}))

        # find user in db to display subscribed themes
        find_user = list(db.user.find({"email": user}))

        # return render_template('profile.html', posts=posts, find_user=find_user)
        return jsonify(posts, find_user)
