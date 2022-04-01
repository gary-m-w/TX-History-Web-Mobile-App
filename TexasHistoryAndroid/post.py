from datetime import datetime
from flask import render_template, request, redirect, session, jsonify
import os
from google.cloud import storage
import time

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "apad_account.json"

storage_client = storage.Client()


def create_post(db):
    # get all posts
    if request.method == 'GET':
        A= db['theme']
        theme = list(A.find({}))
        print(theme)
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
            new_post = db.post.find_one({"title": title, "description": description, "theme": theme, "tag": array_tag, "date": date,
                            "user": user, "address": address, "city": city, "state": state})
            print(new_post)
            time.sleep(1)
            upload_file_to_bucket(str(new_post.get('_id')), file)

            bucket_link = "https://storage.cloud.google.com/texas_history_apad/" +str(new_post.get('_id'))
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
        print("BIG ERROR",e)
        return False
