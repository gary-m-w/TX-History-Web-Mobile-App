from flask import render_template, request, redirect, session, jsonify
from passlib.handlers.pbkdf2 import pbkdf2_sha256


def signup_process(db):
    if request.method == 'GET':
        return render_template('home.html')

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
