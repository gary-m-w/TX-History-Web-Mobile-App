import pymongo
from flask import render_template, request, redirect, session, jsonify


def show_all_themes(db):
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
        all_themes = db.theme.find().sort('label', pymongo.ASCENDING)
        A= db['theme']
        theme = list(A.find({}))
        print(theme)
        # query all posts
        # return render_template('theme.html', all_themes=all_themes, cover='cover',admin_access=admin_access,theme=theme)
        return jsonify(all_themes, admin_access, theme)


def search_theme(db):
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
        A= db['theme']
        theme = list(A.find({}))
        print(theme)
        if search_theme != "all":
            filtered_posts = db.post.find({"theme": search_theme})
        else:
            filtered_posts = db.post.find()
        # return render_template('theme_search.html', all_posts=filtered_posts, search_theme=search_theme, theme=theme, already_sub=already_sub)
        return jsonify(filtered_posts, search_theme, theme, already_sub)
    else:
        # get all posts from database'
        all_posts = db.post.find().sort('date', pymongo.DESCENDING)
        # return render_template('theme_search.html', all_posts=all_posts)
        return jsonify(all_posts)
    

def create_theme(db):
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

def unsubscribe(db):
    if request.method == 'POST':
        search_theme = request.form.get("search_theme")
        if "user" in session:
            user = session["user"]
            db.user.update({"email": user}, {"$pull": {"themes": search_theme}})
    # return redirect('/themes')
    return jsonify()