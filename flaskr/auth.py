from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from .models import db, User
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github
from flask_login import login_user
from authlib.integrations.flask_client import OAuth
auth_bp = Blueprint('auth', __name__)

oauth = OAuth()

google_bp = make_google_blueprint(
    # name ='google',
    client_id='',
    client_secret='',
    # authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    # authrozize_params =None,
    # access_token_url='https://accounts.google.com/o/oauth2/token',
    # access_token_params=None,
    # client_kwargs={'scope':'openid profile email'}
    redirect_to='google_login'
)

github_bp = make_github_blueprint(
    # name='github',
    client_id='',
    client_secret='',
    # authorize_url='https://github.com/login/oauth/authorize',
    # access_token_url='https://github.com/login/oauth/access_token',
    # access_token_params=None,
    # client_kwargs={'scope': 'user:email'}
    redirect_url='github_login'
)

@auth_bp.route('/google.login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    user_info = resp.json()
    
    email = user_info['email']

    user = User.query.filter_by(email=email).first()

    if user is None:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()

    login_user(user)

    #     return f"Welcome {resp.json()['displayname']}!"
    return redirect(url_for('dashboard'))



@auth_bp.route('/github.login')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    
    resp = github.get('/user')
    assert resp.ok, resp.text
    user_info = resp.json()
    username = user_info['login']

    email_resp = github.get('/user/emails')
    if email_resp.ok:
        emails = email_resp.json()
        email = next((e['email'] for e in emails if e['primary']), None)
    else:
        email = None
    
    user = User.query.filter_by(username=username).first()

    if user is None:
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('dashboard'))



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
