from flask import render_template, url_for, flash, redirect, Blueprint, request, jsonify
from app import db
from app.models import Product, User, Cart
from app.forms import LoginForm, SignupForm, ProfileForm, PasswordForm
from flask_login import login_user, logout_user, login_required, current_user, user_logged_in
from sqlalchemy import func

bp = Blueprint('main', __name__)


@bp.route("/")
def index():
    list = Product.query.all()
    return render_template('index.html', list=list, title='Homepage', user=current_user)


@bp.route("/cart")
def cart():
    list = db.session.query(Cart, Product, func.count(Cart.id)).filter_by(user_id=current_user.id).join(
        Product, Cart.product_id == Product.id).group_by(Cart.product_id).all()
    return render_template('cart.html', list=list, user=current_user)


@bp.route("/checkout")
def checkout():
    db.session.query(Cart).filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('checkout successed!', 'success')
    return redirect(url_for('main.index'))


@bp.route("/addtocart")
@login_required
def addtocart():
    product_id = request.args.get('product_id')
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"error": 'product not exist!'})

    if product.inventory <= 0:
        return jsonify({"error": 'product is sold out!'})

    cart = Cart(
        product_id=product.id,
        user_id=current_user.id,
    )

    product.inventory -= 1

    db.session.add(cart)
    db.session.commit()
    return jsonify({"msg": 'product added to cart!'})


@bp.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('user not exist!', 'danger')
        elif user.password != form.password.data:
            flash('password incorrect!', 'danger')
        else:
            login_user(user)
            return redirect(url_for('main.index'))
    return render_template('form.html', form=form, title='Login', user=current_user)


@bp.route("/signup", methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('user with this email is already existed', 'warning')
        else:
            user = User(
                email=form.email.data,
                nickname=form.nickname.data,
                password=form.password.data,
            )
            db.session.add(user)
            db.session.commit()
            flash('Signup success!', 'success')
            login_user(user)
            return redirect(url_for('main.index'))
    return render_template('form.html', form=form, title='Signup', user=current_user)


@bp.route("/profile", methods=['POST', 'GET'])
@login_required
def profile():
    form = ProfileForm(data={
        "email": current_user.email,
        "nickname": current_user.nickname,
    })
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        db.session.commit()
        flash('Profile update success!', 'success')
        return redirect(url_for('main.index'))
    return render_template('form.html', form=form, title='Profile', user=current_user)


@bp.route("/password", methods=['POST', 'GET'])
@login_required
def password():
    form = PasswordForm()
    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.commit()
        flash('Password update success!', 'success')
        return redirect(url_for('main.index'))
    return render_template('form.html', form=form, title='Profile', user=current_user)


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))
