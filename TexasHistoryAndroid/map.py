import requests
from flask import render_template, jsonify
from flask_googlemaps import Map


def create_map(db):
    post_array = []
    all_posts = list(db['post'].find({}))
    for one_post in all_posts:
        # make dict
        # convert address to lat lng
        address_post = one_post['address'] + ", " + one_post['city'] + ", " + one_post['state']
        address_format = address_post.replace(" ", "+")

        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + address_format +
                                ',+CA&key=AIzaSyCAjrVBxmhis9XRZ4f3fspvlOCKeKt6dIk')

        resp_json_payload = response.json()

        # get coordinates
        lat = resp_json_payload['results'][0]['geometry']['location']['lat']
        lng = resp_json_payload['results'][0]['geometry']['location']['lng']

        post_id = str(one_post['_id'])
        img_link = "<a href = '/details/" + post_id + "'> <img src='" + one_post['image'] + "'> </a>"
        post_dict = {'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png', 'lat': lat, 'lng': lng,
                     'infobox': img_link}
        # <a href = "/details/{{one_post._id}}" ><img src="#"</a>
        # append dict to post_array
        post_array.append(post_dict)

    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=30.2672,
        lng=-97.7431,
        style="height:550px;width:800px;margin:0;",
        # Markers array of tuples having (lat, lng, infobox, icon)
        markers=post_array
    )

    # return render_template('map.html', mymap=mymap)
    return jsonify(mymap)