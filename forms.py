from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from models import User


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me')
    submit = SubmitField('access')


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    cf = StringField('cf')
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('register')

    # When you add any methods that match the pattern validate_<field_name>, WTForms takes those as
    # custom validators and invokes them in addition to the stock validators
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            print('Username utilizzato')
            raise ValidationError('Username utilizzato. Riprova')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email già utilizzata. Riprova')

    '''def validate_cf(self, cf):
        cf = User.query.filter_by(cf=cf.data).first()
        if cf is not None:
            raise ValidationError('Codice fiscale precedentemente inserito. Controlla e riprova!')'''


