from flask import Flask, render_template, redirect, url_for, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, MultipleFileField, validators, BooleanField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
import os
import sqlite3 
from flask_login import LoginManager
from flask_migrate import Migrate
from .models import db
from authlib.integrations.flask_client import OAuth
from .auth import auth_bp, google_bp, github_bp

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
oauth = OAuth()


def create_app():
    app = Flask(__name__) 
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['OAUTH_CREDENTIALS'] = {
        'google': {
            'client_id': 'your-google-client-id',
            'client_secret': 'your-google-client-secret'
        },
        'github': {
            'client_id': 'your-github-client-id',
            'client_secret': 'your-github-client-secret'
        }
    }
    oauth.init_app(app)
    # oauth.init_app(app)



    db.init_app(app)
    migrate.init_app(app, db)
    # login_manager.init_app(app)


    app.register_blueprint(auth_bp, url_prefix = '/auth')
    app.register_blueprint(google_bp, url_prefix='/google')
    app.register_blueprint(github_bp, url_prefix='/github')

    # Definiciones de modelos y formularios 
    # @app.register_blueprint(google, url_prefix ='/login')

    # @app.register_blueprint(github, url_prefix='/login')

    # Crear tablas
    # with app.app_context():
    #     db.create_all()


    @app.route('/')
    def home():
        # if not google.authorized:
        #     return redirect("google.login")
        # resp = google.get("/plus/v1/people/me")
        # assert resp.ok, resp.text
        # return f"You have login as {resp.json()['displayname']}"
        return 'This is the home page!'

    class Contact(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(100), nullable=False)
        message = db.Column(db.Text, nullable=False)

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')

            new_contact = Contact(name=name, email=email, message=message)

            db.session.add(new_contact)
            db.session.commit()

            return "Form submitted successfully!"

        return render_template('contact.html')

    class Translator(FlaskForm):
        text_to_translate = TextAreaField('Text to Translate', validators=[DataRequired()])
        source_language = StringField('Source Language', validators=[DataRequired()])
        destination_language = StringField('Destination Language', validators=[DataRequired()])
        text_translated = TextAreaField('Translated Text', validators=[DataRequired()])
        submit = SubmitField('Submit')

    @app.route('/translator', methods=['GET', 'POST'])
    def translator():
        form = Translator()
        if form.validate_on_submit():
            source_text = form.text_to_translate.data
            source_language = form.source_language.data
            destination_language = form.destination_language.data
            text_translated = form.text_translated.data
            submit = form.submit.data    
            return f"The translation from {source_language} to {destination_language} has been made!"
        return render_template('translator.html', form=form)

    class PhotoForm(FlaskForm):
        photo = MultipleFileField(validators=[DataRequired()])
        submit = SubmitField('Upload')

    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        form = PhotoForm()
        if form.validate_on_submit():
            for f in form.photo.data:
                filename = secure_filename(f.filename)
                f.save(os.path.join(
                    app.instance_path, 'photos', filename
                ))
            return redirect(url_for('index'))
        return render_template('upload.html', form=form)

    @app.route('/about', methods=['POST', 'GET'])
    def about():
        return render_template('index.html')

    return app
