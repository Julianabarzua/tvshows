from flask import flash, render_template, request, redirect, session
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.tvshow_mod import Tvshow
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    if 'user_id' in session:
        return redirect('/tvshows')
    return render_template("index.html")

@app.route("/add_user", methods=['POST'])
def add_user():
    
    if not User.validate_user(request.form):
        return redirect("/")
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "firstname" : request.form["fname"],
        "lastname" : request.form["lname"],
        "email" : request.form["email"],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect("/tvshows")


@app.route('/login', methods=['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    usuario = User.getEmail(data)
    if not usuario:
        flash("User not registered")
        return redirect('/')
    
    if not bcrypt.check_password_hash(usuario[0]['password'], request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')

    session['user_id'] = usuario[0]['id']
    return redirect('/tvshows')

@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect('/')