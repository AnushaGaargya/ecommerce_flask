from flask import render_template, session,request,redirect,url_for,flash
from store import app,db,bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
import os
from store.products.models import AddProduct,Category


# @app.route('/',  methods=['GET', 'POST'])
# def home():
#     return render_template('admin/index.html',title='Admin Page')

@app.route('/')
def admin():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    products = AddProduct.query.all()
    # if 'email' in session:
    #     email = session['email']
    #     print(email)
    return render_template('admin/index.html', title='Admin Page', products=products)

@app.route('/categories')
def categories():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    categories = Category.query.all()
    return render_template('admin/category.html', title='Category Page', categories=categories)


@app.route('/register', methods=['GET', 'POST'])
def register():  
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data} Thanks for registering', 'success')
        return redirect(url_for('login'))
    # return render_template('register.html', form=form)
    return render_template('admin/register.html', form=form, title="Register User")

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        #checking if the pw entered is same as pw stored in db
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #storing the email in session
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data} You are logged in now', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong password, please try again', 'danger')

    return render_template('admin/login.html', form=form, title='Login Page')