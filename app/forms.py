# coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Required, EqualTo


class LoginForm(Form):
    # openid = StringField('openid', validators=[DataRequired()])
    nickname = StringField('nickname', validators=[DataRequired()])
    password = PasswordField('New password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class SignupForm(Form):
    group = SelectField(choices=[('DJI skyworth', 'DJI skyworth'), ('other', 'Other')])
    nickname = StringField('nickname', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    floor = SelectField(choices=[('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'),
                                 ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24')],
                        validators=[DataRequired()])
    gender = SelectField(choices=[('female', u'妹子'), ('male', u'汉子'), ('malegirl', u'男妹子'), ('femaleboy', u'女汉子')])


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