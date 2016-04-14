from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(Form):
    #openid = StringField('openid', validators=[DataRequired()])
    nickname = StringField('nickname',validators = [DataRequired()])
    floor = IntegerField('floor', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
