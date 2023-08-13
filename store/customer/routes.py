from flask import render_template,request,redirect,url_for,flash, session
from flask_login import login_required, current_user, logout_user,login_user
from store import db, app, bcrypt, login_manager
from .forms import CustomerRegisterForm, CustomerLoginForm
from .model import Register, CustomerOrder
from ..products.models import AddProduct
import secrets
import os

@app.route('/customer/register', methods=['GET','POST'])
def customer_register():  
    form = CustomerRegisterForm()
    # if request.method == 'POST' and form.validate():
    if form.validate_on_submit():
        print("form ok")
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password, state=form.state.data, city=form.city.data, address=form.address.data,zipcode=form.zipcode.data)
       
        db.session.add(register)
        # flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit() 
        return redirect(url_for('customerLogin'))  
    else:
        print('form not ok')
        print(form.errors)
          
    return render_template('customer/register.html', form=form)


@app.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    # if request.method == 'POST':
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        session['email'] = user.email
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next = request.args.get('next')
            flash('You are logged in now', 'success')
            return redirect(next or url_for('home'))
        
        flash('incorrect email/password')
        return redirect(url_for('customerLogin'))

    return render_template('customer/login.html', form=form)


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('customerLogin'))


@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            for key, item in session['Shoppingcart'].items():
                # item['stock'] = item['stock'] - item['quantity']
                product = AddProduct.query.get(int(key))
                print(product)
                print(product.stock)
                product.stock = int(product.stock) - int(item['quantity'])
                print(product.stock)
                # flash('Items checked out. Continue Shopping...')
                # return redirect(url_for('clearcart'))
            order = CustomerOrder(invoice=invoice, customer_id=customer_id,orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart', None)
            flash('Order received')
            return redirect(url_for('orders',invoice=invoice))
        except Exception as e:
            print(e)
            flash('Something went wrong')
            return redirect(url_for('getCart'))


@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id 
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            subTotal = float(product['price']) * int(product['quantity'])
            grandTotal = subTotal
    
    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', invoice=invoice, subTotal=subTotal, grandTotal=grandTotal, customer=customer,orders=orders)


@app.route('/allorders')
@login_required
def allorders():
    if current_user.is_authenticated:
        customer = current_user.id 
        orders = CustomerOrder.query.filter_by(customer_id=customer).all()
        return render_template('customer/allorders.html',orders=orders)
    else:
        return redirect(url_for('customerLogin'))




