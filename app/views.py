from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from . import db, lm
from . import app
from .forms import LoginForm, SignupForm, FoodForm, ChangePasswordForm, DeleteForm
from .models import User, Food


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index():
    user = g.user
    orders = [
        {
            'name': 'Mango Tofu Salad',
            'price': '27',
            'quant': '1',
            'floor': '23'
        },
        {
            'name': 'Quinoa Okra Beef Salad',
            'price': '35',
            'quant': '1',
            'floor': '23'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           orders=orders)


@app.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    user = g.user
    orders = [
        {
            'name': 'Beautiful day in Portland!',
            'price': '27',
            'quant': '1'
        },
        {
            'name': 'The Avengers movie was so cool!',
            'price': '35',
            'quant': '1'
        }
    ]
    return render_template('orders.html',
                           title='My Orders',
                           user=user,
                           orders=orders)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form1 = SignupForm()
    if form1.validate_on_submit():
        # session['remember_me'] = form.remember_me.data
        print 'on submit'
        print 'form.nickname:', form1.nickname
        user = User.query.filter_by(nickname=form1.nickname.data).first()
        if user is None:
            print 'new nickname,adding to db'
            user = User(nickname=form1.nickname.data, floor=form1.floor.data)
            db.session.add(user)
            db.session.commit()
            return redirect(request.args.get('next') or url_for('index'))
        else:
            print 'nickname exist:', user.nickname
            flash('User exists.' % form1.nickname.data)
            # return redirect(request.args.get('next') or url_for('index'))

            # remember_me = False
            # return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('signup.html',
                           title='Sign Up for Weat!',
                           form=form1)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        print 'user valid:', g.user
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        print 'on submit'
        # print 'form.nickname:',form.nickname
        user = User.query.filter_by(nickname=form.nickname.data).first()
        print 'filtering nickname'
        if user is None:
            print 'nickname none'
            flash('The nickname is not registered.')
            # return redirect(url_for('signup'))
            # user = User(nickname=form.nickname.data, floor=form.floor.data)
            # db.session.add(user)
            # db.session.commit()
            # return redirect(url_for('signup'))
        else:
            print 'nickname exist:', user.nickname
            login_user(user, remember=session['remember_me'])
            return redirect(request.args.get('next') or url_for('index'))

            # remember_me = False
            # return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        print 'user is none in /user/profile'
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    print 'user:', user.nickname
    return render_template('user.html',
                           user=user)


@app.route('/food_add', methods=['GET', 'POST'])
@login_required
def food_add():
    form = FoodForm()

    foods = Food.query.all()

    if form.validate_on_submit():
        print 'food add commit'
        food = Food.query.filter_by(name=form.name.data).first()
        if food is None:
            food = Food(name=form.name.data, price=form.price.data)
            db.session.add(food)
            db.session.commit()
            flash('add food %s succeed!' % food.name)
            # print 'food added:', food.name
            return redirect(url_for('food_add'))
        else:
            print 'food exists:', food.name
            flash('this food is already included.')
    return render_template('food_add.html',
                           title='Add new food',
                           form=form,
                           form_del=form_del,
                           foods=foods)


@app.route('/order_add', methods=['GET', 'POST'])
def order_add():
    form = DeleteForm()

    foods = Food.query.all()

    if request.method == 'POST':
        print request.form.values
        for food in foods:
            click_id = food.id
            if request.form.get('add', None) == "%d" %click_id:
                print 'hahaha', click_id
                # db.session.add

    if form.validate_on_submit():
        print 'here'
        # if form.remove_id.data is not None and form.remove_id.data != 9999:
        #     print 'remove id:', form.remove_id.data
        #     food1 = foods.query.filter_by(id=form.remove_id.data)
        #     if food1 is None:
        #         print 'delete error:', form.remove_id.data
        #     else:
        #         db.delete(food1)
        #         print 'food deleted:', food1.name
        #         db.commit()
    return render_template('order_add.html',
                           title='add new order',
                           form=form,
                           foods=foods)


# @app.route('/foods', methods=['GET', 'POST'])
# @login_required
# def foods():
#     foods = Food.query.all()
#     return render_template('foods.html',
#                            title='foods',
#                            foods=foods)

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    return render_template("change_password.html", form=form)
