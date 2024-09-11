from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField
from wtforms.validators import InputRequired, Length, Email, EqualTo


auth = Blueprint('auth', __name__)

db = SQLAlchemy(__name__)

class User(db.Model):
    id = db.column(db.Integer, primary_key=True)
    email = db.column(db.String(50), unique=True, nullable=False)
    password_hash = db.column(db.String(128), nullable=False)
    first_name = db.column(db.String(50), nullable=False)
    last_name = db.column(db.String(50), nullabe=False)
    birthday = db.column(db.Date, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Registrationform(FlaskForm):
    fname = StringField('Your name and surname', validators=[InputRequired(), Length(max=70)])
    lname = StringField('Your last name', validators=[InputRequired(), Length(max=70)])
    Birthday = DateTimeField('Your birthday', format='%Y-%m-%d' validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=150)])
    password = PasswordField('Password', validators=[InputRequired(), Length(max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register account')


@auth.route('/register', methods=['GET','POST'])
def register():
    form = Registrationform()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            new_user = User(
            first_name = form.fname.data,
            last_name = form.lname.data,
            birthday = form.birthday.data,
            email = form.email.data
            )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('The registration has been completed', 'success')
            return redirect(url_for('login'))
        else:
            flash('The email is already registered')
    return render_template('register.html', form=form)



class Login(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')


@auth.route('/login', methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.order_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Succesfull login', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect email or password', 'error')
    return render_template('login.html', form=form)

@auth.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You must login to access the website.')
        return redirect(url_for('login'))
    return render_template('dashboard.html')


def logout():
    session.pop('user_id', None)
    flash('You logout successfully', 'success')
    return redirect(url_for('home'))




# flask db migrate -m "Added first name, last name, and birthday fields to User model"
# flask db upgrade






