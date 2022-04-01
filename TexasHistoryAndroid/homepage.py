import pymongo
from flask import render_template, request, redirect, jsonify


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