from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime

from models import User


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me')
    submit = SubmitField('access')


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    cf = StringField('cf',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('register')

    # When you add any methods that match the pattern validate_<field_name>, WTForms takes those as
    # custom validators and invokes them in addition to the stock validators
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username utilizzato. Riprova')

    def validate_cf(self, cf):
        user = User.query.filter_by(cf=cf.data).first()
        if user is not None or len(cf.data)!=16:
            raise ValidationError('Codice fiscale errato. Riprova')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email già utilizzata. Riprova')

class InsertPositiveForm(FlaskForm):
    cf = StringField('cf',validators=[DataRequired()])
    date = StringField('date', validators=[DataRequired()])
    submit = SubmitField('insert')

    def validate_cf(self, cf):
        user = User.query.filter_by(cf=cf.data).first()
        if user is None:
            raise ValidationError("Codice fiscale non esistente. Utente non registrato")

    def validate_date(self, date):
        insert_date = datetime.strptime(date.data,
                                        '%Y-%m-%dT%H:%M')
        if insert_date >= datetime.now():
            raise ValidationError("Non è possibile inserire una data futura.")

class HealthWorkerRegistrationForm(FlaskForm):
    id = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username utilizzato. Riprova')
