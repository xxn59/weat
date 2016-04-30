from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Required, EqualTo


class LoginForm(Form):
    # openid = StringField('openid', validators=[DataRequired()])
    nickname = StringField('nickname', validators=[DataRequired()])
    password = PasswordField('password')
    remember_me = BooleanField('remember_me', default=False)


class SignupForm(Form):
    group = SelectField(choices=[('dji', 'DJI skyworth'), ('other', 'Other')])
    nickname = StringField('nickname', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    floor = IntegerField('floor', validators=[DataRequired()])


class FoodForm(Form):
    name = StringField('name', validators=[DataRequired()])
    price = IntegerField('price')
    cat = SelectField()


class AddFoodForm(Form):
    remove_id = IntegerField('remove_id')



class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password', default=9999)

class EditForm(Form):
    group = SelectField(choices=[('dji', 'DJI skyworth'), ('other', 'Other')])
    # nickname = StringField('nickname', validators=[DataRequired()])
    floor = IntegerField('floor', validators=[DataRequired()])
    submit = SubmitField('submit')