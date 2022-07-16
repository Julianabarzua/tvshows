from flask import flash, render_template, request, redirect, session
from flask_app import app
from flask_app.models.tvshow_mod import Tvshow
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/tvshows")
def logedin():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":session['user_id']
    }
    tvshows = Tvshow.get_all()
    usuarioLogeado = User.logedUser(data)
    shows_liked = Tvshow.shows_liked_by_id(session['user_id'])
    return render_template("tvshows.html", usuarioLogeado = usuarioLogeado, tvshows=tvshows, shows_liked = shows_liked)


@app.route("/tvshows/new")
def new_tv_show():
    print(session['user_id'])

    return render_template("new_tvshow.html")

@app.route("/add_tvshow", methods=['POST'])
def add_tvshow():

    if not Tvshow.validate_tvshow(request.form):
        return redirect("/tvshows/new")
    data = {
        "title" : request.form["title"],
        "network" : request.form["network"],
        "release_date" : request.form["release_date"],
        "description" : request.form["description"],
        "posted_by" : session['user_id']
    }
    Tvshow.save(data)
    return redirect("/tvshows")

@app.route("/delete_tvshow/<tvshow_id>")
def delete_tvshow(tvshow_id):
    Tvshow.delete(id=tvshow_id)
    return redirect("/tvshows")

@app.route("/tvshows/<tvshow_id>")
def show_tvshow(tvshow_id):
    
    tvshow=Tvshow.getonebyid(tvshow_id)
    print(tvshow)
    
    data = {
        "id":session['user_id']
    }
    usuarioLogeado = User.logedUser(data)
    likes_count = Tvshow.likes_count(tvshow_id)

    return render_template("show.html", tvshow=tvshow, usuarioLogeado = usuarioLogeado, likes_count = likes_count)

@app.route("/tvshows/edit/<tvshow_id>")
def edit_tvshow(tvshow_id):
    tvshow=Tvshow.getonebyid(tvshow_id)
    return render_template("edit.html", tvshow=tvshow)

@app.route("/tvshows/update/<tvshow_id>", methods=['POST'])
def update_tvshow(tvshow_id):

    if not Tvshow.validate_tvshow(request.form):
        return redirect("/tvshows/edit/"+tvshow_id)


    data = {
        "title" : request.form["title"],
        "network" : request.form["network"],
        "release_date" : request.form["release_date"],
        "description" : request.form["description"],
    }
    Tvshow.update_tvshow(data, tvshow_id)
    return redirect("/tvshows")


@app.route("/add_like/<tvshow_id>")
def add_like(tvshow_id):
    data = {
        "show_liked_id" : tvshow_id,
        "user_likes_id" : session['user_id']
    }
    Tvshow.save_like(data)
    return redirect("/tvshows")


@app.route("/delete_like/<tvshow_id>")
def del_like(tvshow_id):
    data = {
        "show_liked_id" : tvshow_id,
        "user_likes_id" : session['user_id']
    }
    Tvshow.del_like(data)
    return redirect("/tvshows")


