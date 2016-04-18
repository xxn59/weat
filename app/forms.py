from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired,Length


class LoginForm(Form):
    #openid = StringField('openid', validators=[DataRequired()])
    nickname = StringField('nickname', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class SignupForm(Form):
    group_code = StringField('group_code', validators=[Length(min=4, max=10)])
    nickname = StringField('nickname', validators=[DataRequired()])
    floor = IntegerField('floor', validators=[DataRequired()])

class FoodForm(Form):
    name = StringField('name', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
