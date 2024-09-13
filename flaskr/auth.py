from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from .models import db, User

auth_bp = Blueprint('auth', __name__)

class RegistrationForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired(), Length(max=70)])
    lname = StringField('Last Name', validators=[InputRequired(), Length(max=70)])
    birthday = DateField('Your Birthday (YYYY-MM-DD)', format='%Y-%m-%d', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=150)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            new_user = User(
                first_name=form.fname.data,
                last_name=form.lname.data,
                birthday=form.birthday.data,
                email=form.email.data
            )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('The registration has been completed', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('The email is already registered', 'error')
    return render_template('auth/register.html', form=form)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Successful login', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Incorrect email or password', 'error')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You must log in to access the website.', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('auth/dashboard.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You logged out successfully', 'success')
    return redirect(url_for('home_page'))
