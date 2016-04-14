from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from . import app,db, lm
from .forms import LoginForm
from .models import User



@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        print 'user valid:',g.user
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        print 'on submit'
        print 'form.nickname:',form.nickname
        user = User.query.filter_by(nickname = form.nickname.data).first()
        if user is None:
            print 'nickname none'
            user = User(nickname=form.nickname.data, floor=form.floor.data)
            db.session.add(user)
            db.session.commit()
        else:
            print 'nickname exist:',user.nickname
            login_user(user, remember=session['remember_me'])
            return redirect(request.args.get('next') or url_for('index'))
        #remember_me = False
        #return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
