from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db,User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def show_users():
    users=User.query.order_by(User.last_name.asc()).order_by(User.first_name.asc()).all()

    return render_template("homepage.html",users=users)



@app.route("/user/new")
def show_new_user_addform():

    return render_template("addnewuser.html")


@app.route("/user/new",methods=["POST"])
def add_user():

    first_name=request.form["firstName"].capitalize()
    last_name=request.form["lastName"].capitalize()
    image_url=request.form["imageURL"] or None

    if first_name=="" or last_name=="":

        if first_name=="":
            flash("Invalid Input: First Name is required!","error")
           
        
        if last_name=="":
            flash("Invalid Input: Last Name is required!","error")
            
        return redirect("/user/new")
    

    new_user=User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/user/{new_user.id}")

@app.route("/user/<int:user_id>")
def show_user(user_id):

    user=User.query.get_or_404(user_id)
    return render_template("userinfo.html",user=user)



@app.route("/user/<int:user_id>/delete",methods=["POST"])
def delete_user(user_id):

    deleted_user=User.query.get_or_404(user_id)
    db.session.delete(deleted_user)
    db.session.commit()
    return redirect("/")

@app.route("/user/<int:user_id>/edit")
def show_edit_user_form(user_id):

    user=User.query.get_or_404(user_id)
    return render_template("edit_user.html",user=user)

@app.route("/user/<int:user_id>/edit",methods=["POST"])
def edit_user(user_id):

    defaultURL="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAMAAACahl6sAAAABlBMVEXJycmcnJyshIZ4AAAB7ElEQVR4nO3bUW7DMAwEUfv+ly4SGEXQ2kksk1xqPXMCvj8BIpeFiIiIiIiIiIiIiIiIiKio9TX1MIOt+6nHOtcBYjbMB8YklC8UM1i+ZjSnnHL0lZxkdKUMMFpSBh3tJMOOXpILjFaUi442ksuOJpIARwtJiKOBJMihl7hAwhxiSaBDKgl1KCUukGCHThIOEUniHRpIgkMjcYGkOBQSIM0kWQ4g3RzVEiBApnPUSoAAAaJzVEqAAAECBAgQIECAzCopdAABAkQoKXUAATKfpNjhA7H5Q+RXtx3EZvPBB2KzHeSzr+WzQWez0+gDsdn79dnE9tmN94HY3I/4XPT43Fj5XL353CEuNpehi8+trs/19GJzz74MSNQDH2fCeGTCeGTCeOah2LJA/OZgICIioq35nygOr9+Phhk0JxCNMQOKhpZhRS/LRUYTSoCigyWMoaWEMnSUcIaGksIQUNIcRjvlhZRkR5UknVFEKXHkS4oY6ZRCR6qk1JEoKXakScodSRKBI0MiYSRQZI5gidARK3GBSB2BErEjTKJmrEESNeKZiyNCohZsuTguS9TjvwSkmeOSRD36n4CoB//X3SHqsXe6N0Q99G53hqhHPghIt1wc5yXqeQ+7K0Q97puAdOueEPWwbwPSLSDd2p34B3GsN/j6gvMWAAAAAElFTkSuQmCC"

    edit_user=User.query.get_or_404(user_id)
    edit_user.first_name=request.form["firstName"]
    edit_user.last_name=request.form["lastName"]
    edit_user.image_url=request.form.get("imageURL") or defaultURL

    first_name=edit_user.first_name
    last_name=edit_user.last_name

    if first_name=="" or last_name=="":

        if first_name=="":
            flash("Invalid Input: First Name is required!","error")
           
        if last_name=="":
            flash("Invalid Input: Last Name is required!","error")
            
        return redirect(f"/user/{user_id}/edit")

    db.session.add(edit_user)
    db.session.commit()

    return redirect(f"/user/{edit_user.id}")


