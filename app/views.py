from flask import render_template, flash, redirect, session, url_for, request, g, make_response
from flask.ext.login import login_user, logout_user, current_user, login_required
from . import db, lm
from . import app
from .forms import LoginForm, SignupForm, FoodForm, ChangePasswordForm, AddFoodForm, EditForm
from datetime import datetime, date, time, timedelta
from .models import User, Food, Salad, Order


# food_list = []

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
    orders = Order.query.all()
    if request.method == 'POST':
        # print request.form.values
        copy_id = request.form.get('copy', None)
        if copy_id is None:
            pass
        else:
            copy_salad = Salad.query.get(copy_id)
            new_salad = Salad(foods=copy_salad.foods, price=copy_salad.price)
            db.session.add(new_salad)
            new_order = Order(cos_id=user.id, status=9, price=new_salad.price)
            new_order.salads.append(new_salad)

            db.session.add(new_order)
            db.session.commit()
            return redirect(url_for('order_review', source='copy'))


    return render_template('index.html',
                           title='We eat together!',
                           user=user,
                           orders=orders)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # session['remember_me'] = form.remember_me.data
        # print 'on submit'
        # print 'form.nickname:', form1.nickname
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if user is None:
            # print 'new nickname,adding to db'
            user = User(nickname=form.nickname.data, floor=form.floor.data, group=form.group.data)
            db.session.add(user)
            db.session.commit()
            return redirect(request.args.get('next') or url_for('index'))
        else:
            # print 'nickname exist:', user.nickname
            flash('User exists.' % form.nickname.data)
            # return redirect(request.args.get('next') or url_for('index'))

            # remember_me = False
            # return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('signup.html',
                           title='Sign Up for Weat!',
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        # print 'user valid:', g.user
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        # print 'on submit'
        # print 'form.nickname:',form.nickname
        user = User.query.filter_by(nickname=form.nickname.data).first()
        # print 'filtering nickname'
        if user is None:
            # print 'nickname none'
            flash('The nickname is not registered.')
            # return redirect(url_for('signup'))
            # user = User(nickname=form.nickname.data, floor=form.floor.data)
            # db.session.add(user)
            # db.session.commit()
            # return redirect(url_for('signup'))
        else:
            if user.is_admin():
                pass
                # flash('please enter the PASSWORD')
                # return redirect(url_for('login_admin'))
            # print 'nickname exist:', user.nickname
            login_user(user, remember=session['remember_me'])
            return redirect(request.args.get('next') or url_for('index'))

            # remember_me = False
            # return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    form = LoginForm()
    return render_template('login_admin.html',
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
        # print 'user is none in /user/profile'
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    # print 'user:', user.nickname
    return render_template('user.html',
                           user=user)


from models import food_category


@app.route('/food_add', methods=['GET', 'POST'])
@login_required
def food_add():
    user = g.user
    if user.level < 3:
        return redirect(url_for('index'))
    form = FoodForm()
    form.cat.choices = [(f, f) for f in food_category]

    foods = Food.query.all()

    if form.validate_on_submit():
        # print 'food add commit'
        food = Food.query.filter_by(name=form.name.data).first()
        if food is None:
            food = Food(name=form.name.data, price=form.price.data, cat=form.cat.data)
            db.session.add(food)
            db.session.commit()
            flash('add food %s succeed!' % food.name)
            # print 'food added:', food.name
            return redirect(url_for('food_add'))
        else:
            # print 'food exists:', food.name
            flash('this food is already included.')
    return render_template('food_add.html',
                           title='Add new food',
                           form=form,
                           foods=foods)


@app.route('/order_add', methods=['GET', 'POST'])
@login_required
def order_add():
    user = g.user
    form = AddFoodForm()
    foods = Food.query.filter(Food.cat != 'new_arrival').order_by(Food.price)
    foods_new = Food.query.filter(Food.cat == 'new_arrival').order_by(Food.price)

    if request.method == 'POST':
        # print request.form.values
        done = request.form.get('over', None)
        # print done
        if done == "7963":
            # print 'yes,done=7963'
            meal = request.form.get('meal', None)
            if meal is None:
                flash('please choose which meal you want to order')
                return redirect(url_for('order_add'))
            submit_order = Order.query.filter_by(cos_id=user.id, status=1).first()
            if submit_order is None:
                flash('no unconfirmed order to submit ')
                return redirect(url_for('order_add'))
            submit_salad = Salad.query.filter_by(order_id=submit_order.id, status=1).first()
            if submit_salad is None:
                flash('no incomplete salad to submit')
                return redirect(url_for('order_add'))

            for f in submit_salad.foods:
                submit_salad.price = submit_salad.price + f.price
            submit_salad.price += 4
            if submit_salad.price < 25:
                flash('price < 25, please add something more~')
                return redirect(url_for('order_add'))
            for s in submit_order.salads:
                submit_order.price = submit_order.price + s.price

            submit_order.status = 2
            submit_salad.status = 2
            submit_order.meal = meal
            submit_order.timestamp = datetime.utcnow()

            # print 'db commit'
            db.session.commit()
            # user.add_order(new_order)
            return redirect(url_for('orders'))

        click_id = request.form.get('add', None)
        if click_id is None:
            # print 'no click'
            pass

        else:
            # print 'click_id:', click_id
            new_order = Order.query.filter_by(cos_id=user.id, status=1).first()
            if new_order is None:
                new_order = Order(cos_id=user.id, status=1)
                db.session.add(new_order)
                # print 'added new order'

            new_salad = Salad.query.filter_by(order_id=new_order.id, status=1).first()
            if new_salad is None:
                new_salad = Salad(order_id=new_order.id, status=1)
                db.session.add(new_salad)
                # print 'added new salad'
            else:
                pass
                # print 'continue last salad'
            food = Food.query.get(click_id)
            new_salad.foods.append(food)
            # food_list.append(food)
            # food_test1 = Food.query.get(1)
            # food_test2 = Food.query.get(2)
            # new_salad.foods.append(food_test1)
            # new_salad.foods.append(food_test2)
            # print 'foods in new_salad:'
            for f in new_salad.foods:
                pass

                # print f.name
            # for f in food_list:
            #     print 'foods in food_list:', f.name
            db.session.commit()
            # food1 = Food(name='dsfaef')
            # print food.name
            # food_list.append(food)
            # print len(food_list)
            # flash('add food success')
        resp = make_response('', 204)
        return resp
        # db.session.commit()
        # print 'food_list:', food_list
        # new_salad.add_food(food)
        # db.session.commit()

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
        #
    return render_template('order_add.html',
                           title='add new order',
                           form=form,
                           foods=foods,
                           foods_new=foods_new)


@app.route('/order_review/<source>', methods=['GET', 'POST'])
@login_required
def order_review(source):
    user = g.user
    if source == 'copy':
        # new_order = Order(cos_id=user.id)
        # new_salad = Salad(order_id=new_order.id)
        new_order = Order.query.filter_by(status=9).first()
        if new_order is not None:
            foods = new_order.salads[0].foods
    # new_salad.foods =
        if request.method == 'POST':
            confirm = request.form.get('confirm', None)
            if confirm == "7963":
                pass
                # meal = request.form.get('meal', None)
                # if meal is None:
                #     flash('please choose which meal you want to order')
                #     return redirect(url_for('order_add'))
    return render_template('order_add.html',
                           title='add new order',
                           foods=foods)


@app.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    user = g.user
    if user.level < 3:
        orders = Order.query.filter_by(cos_id=user.id)
        o = orders.first()
        if o is None:
            order_len = 0
        else:
            order_len = 1
        print order_len
        if request.method == 'POST':
            btn = request.form.get('remove', None)
            if btn is not None:
                print btn
                del_order = Order.query.get(btn)
                print del_order.cos_id
                user.del_order(del_order)
                # db.session.remove(del_order)
                db.session.commit()
                return redirect(url_for('orders'))
            else:
                print 'btn is none'

        return render_template('orders.html',
                               title='My Orders',
                               user=user,
                               orders=orders,
                               len=order_len)

    return redirect(url_for('orders_all'))


@app.route('/orders_all', methods=['GET', 'POST'])
@login_required
def orders_all():
    user = g.user
    if user.level >= 3:
        dateNow = datetime.utcnow().date()
        # timeNow = datetime.utcnow().time()
        time_z = time(0, 0)
        # dinner_end = time(19, 0)
        query_begin = datetime.combine(dateNow, time_z) - timedelta(days=1)
        # query_end = datetime.combine(dateNow, time_z)
        orders = Order.query.all()
        orders_lunch = Order.query.filter(Order.status == 2, Order.meal == 'lunch')
        orders_dinner = Order.query.filter(Order.timestamp.between(query_begin, datetime.utcnow()), Order.status == 2,
                                         Order.meal == 'dinner')

        return render_template('orders_all.html',
                               title='All Orders',
                               user=user,
                               orders_lunch=orders_lunch,
                               orders_dinner=orders_dinner
                               )
    return redirect(url_for('orders'))


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    return render_template("change_password.html", form=form)


@app.route('/user_edit', methods=['GET', 'POST'])
@login_required
def user_edit():
    user = g.user
    form = EditForm()
    form.floor.data = user.floor
    form.group.data = user.group
    if form.validate_on_submit():
        user.floor = form.floor.data
        user.group = form.group.data
        return redirect(url_for('user'))
    return render_template("user_edit.html", user=user, form=form)


@app.route('/pay', methods=['GET', 'POST'])
def pay():
    return render_template("pay_test.html")


@app.route('/about_me', methods=['GET', 'POST'])
def about_me():
    return render_template("about_me.html")
