from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, MultipleFileField, validators, BooleanField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
import os
from auth import auth

app = Flask(__name__)

app.config['SECRET_KEY']= 'your_secret_key'

app.config['SQLALCHEMY_DATABASE.URI'] = 'sqlite:///contact.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def home_page():
    return 'Its the home page!'


app.register_blueprint('auth', url_prefix='/auth')



class Contact(db.Model):
    id = db.column(db.Intenger, primary_key = True)
    name = db.column(db.String(100), nullable=False)
    email = db.column(db.String(100), nullable=False)
    message = db.column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/contact', methods=('GET', 'POST'))
def contact_data():
    if request.form == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        new_contact = Contact(name=name, email=email, message=message)

        db.session.add(new_contact)
        db.session.commit()

        return "Form submmited succesfully!"

    return render_template('contact.html')



class Translator(FlaskForm):
    text_to_translate = TextAreaField('name', validators=[DataRequired()])
    source_language = StringField('first_language', validators=[DataRequired()])
    destination_language = StringField('final', validators=[DataRequired()])
    text_translated = TextAreaField('translated', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/translator', methods=['GET', 'POST'])
def translator():
    form = Translator()
    if form.validate_on_submit():
        source_text = form.text_to_translate.data
        source_language = form.source_language.data
        destination_language = form.destination_language
        text_translated = form.text_translated.data
        submit = form.submit.data    
        return f"The translation from {source_language} a {destination_language} has been made!"
    return render_template('translator.html', form=form)


class Myform(FlaskForm):
    name = StringField('name', validators=[DataRequired()])



class PhotoForm(FlaskForm):
    photo = MultipleFileField(validators=[DataRequired()])

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



        
@app.route('/about', methods=('POST'))
def about():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)