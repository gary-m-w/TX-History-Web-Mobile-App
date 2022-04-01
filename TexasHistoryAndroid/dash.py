import pymongo
from flask import render_template, request, jsonify
import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "apad_account.json"

storage_client = storage.Client()


def dashboard(db):
    if request.method == 'POST':
        # query all posts for the tag
        search_tag = request.form.get("search_tag")
        filtered_posts = db.post.find({"tag": search_tag})
        # filtered_posts = db.post.find({"tag": [search_tag]}).sort('date', pymongo.DESCENDING)
        #return render_template('dashboard.html', all_posts=filtered_posts)
        return jsonify(filtered_posts)

    else:

        # get all posts from database'

        all_posts = db.post.find().sort('date', pymongo.DESCENDING)
        # # dirname = os.path.dirname(__file__)
        # # client = storage.Client.from_service_account_json(
        # #     json_credentials_path=os.path.join(dirname, 'gcp_credentials/apad-dev-ce318926e02e.json'))
        # # updated_posts = []
        # for post in all_posts:
        #     # bucket_link = "https://storage.cloud.google.com/texas_history_apad/"+post.get('_id')
        #     # imgRef = post['image']
        #     # bucket = client.get_bucket('apad_group_project')
        #     # # Create a blob object from the filepath
        #     # blob = bucket.blob(imgRef)
        #     # # Download the file to a destination
        #     # blob.download_to_filename(os.path.join(dirname, 'static/read_data/' + imgRef + '.jpeg'))
        #     # post['image'] = 'static/read_data/' + imgRef + '.jpeg'
        #     # updated_posts.append(post)
        #return render_template('dashboard.html', all_posts=all_posts)
        return jsonify(all_posts)