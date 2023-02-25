from flask import Blueprint, redirect, url_for, render_template, request, flash, session
from forms import LoginForm, RegisterForm
from models import User

from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        print("yoo!")
        user = User.query.filter_by(email = form.email.data).first()
        print("hello", user)
        if user:
            if check_password_hash(user.password, form.password.data):
                flash('You have successfully logged in.', "success")  
                session['logged_in'] = True
                session['email'] = user.email 
                session['username'] = "Admin"

                return redirect(url_for('home2'))

            else:
                flash('Username or Password Incorrect', "Danger")

            return redirect(url_for('auth_bp.login'))
    return render_template("login_alter.html", form=form)


from app import db
@auth_bp.route('/register/', methods = ['GET', 'POST'])
def register():
    
    form = RegisterForm(request.form)
    
    if request.method == 'POST':
        print("yoooo!")
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        print(form.email.data, hashed_password)
    
        new_user = User(
            email = form.email.data, 
            password = hashed_password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            print(e)
    
        flash('You have successfully registered', 'success')
    
        return redirect(url_for('auth_bp.login'))
    
    else:
        return render_template('register_alter.html', form = form)
    

@auth_bp.route('/logout/')
def logout():
    session['logged_in'] = False
    return redirect(url_for('auth_bp.login'))
