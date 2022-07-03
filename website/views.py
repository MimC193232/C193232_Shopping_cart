from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
# from flask_login import login_required, current_user
from flask_login import login_user, login_required, logout_user, current_user
from .models import  Product, Order
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    products = Product.query.all()
    orders = Order.query.filter_by(user_id=current_user.id).all()
    orders_by_user = []
    for o in orders:
        p = Product.query.get(o.product_id)
        orderdetail = OrderDetail(order_id=o.id, product_name=p.name,
                                  order_qty=o.order_qty, price=p.price, order_date=o.created_on)
        orders_by_user.append(orderdetail)
    return render_template("products.html", user=current_user, products=products, orders=orders_by_user)



@views.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        rating = request.form.get('rating')
        price = request.form.get('price')
        qty = request.form.get('qty')

        product = Product.query.filter_by(name=name).first()
        if product:
            flash('Product already exists.', category='error')
        else:
            new_product = Product(name=name, category=category,
                                  rating=rating, price=price, qty=qty, user_id=current_user.id)
            db.session.add(new_product)
            db.session.commit()
            login_user(current_user, remember=True)
            flash('Product created!', category='success')
            return redirect(url_for('views.add_product'))
    products = Product.query.all()
    return render_template("add_product.html", user=current_user, products=products)



@views.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    products = Product.query.all()
    orders = Order.query.filter_by(user_id=current_user.id).all()
    orders_by_user = []
    for o in orders:
        p = Product.query.get(o.product_id)
        orderdetail = OrderDetail(order_id=o.id, product_name=p.name,
                                  order_qty=o.order_qty, price=p.price, order_date=o.created_on)
        orders_by_user.append(orderdetail)

    return render_template("products.html", user=current_user, products=products, orders=orders_by_user)



@views.route('/order', methods=['POST'])
@login_required
def order():
    product_id = request.form.get('product_id')
    product_id = int(product_id)
    #product = Product.query.filter_by(id=product_id).first()
    product = Product.query.get(product_id)
    if product:
        order_qty = int(request.form.get('order_qty'))
        if order_qty < product.qty:
            amount = order_qty * product.price
            new_order = Order(user_id=current_user.id, product_id=product_id, order_qty=order_qty)

            db.session.add(new_order)
            db.session.commit()
            db.session.refresh(new_order)
            rem_qty = product.qty - order_qty
            product.qty = rem_qty
            db.session.commit()
            db.session.refresh(product)

            login_user(current_user, remember=True)
            flash('Order has been placed successfully!', category='success')
        else:
            flash('order quantity must be smaller than stock quantity ', category='error')
    else:
        flash(f'Products with id = {product_id} Does not exist', category='error')
    return redirect(url_for('views.products'))


@views.route('/delete-order', methods=['POST'])
def delete_order():
    order = json.loads(request.data)
    orderId = order['orderId']
    order = Order.query.get(orderId)
    if order:
        if order.user_id == current_user.id:
            db.session.delete(order)
            db.session.commit()

    return jsonify({})


class OrderDetail:
    def __init__(self, order_id, product_name, order_qty, price, order_date):
        self.order_id = order_id
        self.product_name = product_name
        self.order_qty = order_qty
        self.price = price
        self.order_date =order_date

