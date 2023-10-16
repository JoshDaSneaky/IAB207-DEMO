from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm

from flask_login import login_user, logout_user, login_required
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db

authbp = Blueprint('auth', __name__)

@authbp.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    error = None
    if loginForm.validate_on_submit():

        username = loginForm.username.data
        password = loginForm.password.data

        user = db.session.scalar(db.select(User).where(User.name == username))


        if user is None:
            error = 'Incorrect Username'

        elif not check_password_hash(user.password_hash, password):
            error = 'Incorrect Password'
        
        print(error)

        if error == None:
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('user.html', form=loginForm, heading='Login')

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data

        user = db.session.scalar(db.select(User).where(User.name == username))

        if user:
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        
        pass_hash = generate_password_hash(password)

        new_user = User(name=username, email=email, password_hash=pass_hash)

        db.session.add(new_user)
        db.session.commit()

        print('Successfully registered')
        return redirect(url_for('main.index'))
    return render_template('user.html', form=form, heading='Register')

@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('main.index'))