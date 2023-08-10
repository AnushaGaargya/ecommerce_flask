from flask import redirect,render_template,url_for,flash,request,session, current_app
from store import db, app, bcrypt
from .models import Category, AddProduct
from .forms import Addproducts
from werkzeug.utils import secure_filename
import os
import uuid as uuid

UPLOAD_FOLDER = '/users/anusha/Desktop/Flask Projects/Final_Project/store/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# @app.route('/addbrand', methods=['GET', 'POST'])
# def addbrand():
#     if request.method == 'POST':
#         getbrand = request.form.get('brand')
#         brand = Brand(name=getbrand)
#         db.session.add(brand)
#         flash(f'The Brand {getbrand} was added to your database', 'success')
#         db.session.commit()
#         return redirect(url_for('addbrand'))
#     return render_template('products/addbrand.html',brands='brands')


@app.route('/proddisplay')
def home():
    products = AddProduct.query.filter(AddProduct.stock > 0)
    # categories = Category.query.all()
    categories = Category.query.join(AddProduct,(Category.id == AddProduct.category_id)).all()
    return render_template('products/index.html', products=products, categories=categories)

@app.route('/product/<int:id>')
def single_page(id):
    product = AddProduct.query.get_or_404(id)
    categories = Category.query.join(AddProduct,(Category.id == AddProduct.category_id)).all()
    return render_template('products/single_page.html',product=product, categories=categories)




@app.route('/category/<int:id>')
def get_category(id):
    category = AddProduct.query.filter_by(category_id=id)
    categories = Category.query.join(AddProduct,(Category.id == AddProduct.category_id)).all()
    return render_template('products/index.html', category=category, categories=categories)


@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        getcat = request.form.get('category')
        cat = Category(name=getcat)
        db.session.add(cat)
        flash(f'The Category {getcat} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')


@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecat.name = category
        flash(f'Category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/updatebrand.html',title='Update Category Page', updatecat=updatecat)
    

@app.route('/deletecat/<int:id>', methods=['POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        db.session.commit()
        flash(f'Category {category.name} has been deleted', 'success')
        return redirect(url_for('admin'))
    flash(f'Category {category.name} cannot be deleted', 'warning')
    return redirect(url_for('admin'))


@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    
    categories = Category.query.all()
    form = Addproducts(request.form)
    # prod_img = request.files('my_image')
    if request.method == 'POST':
     
        name= form.name.data
        price = form.price.data
        stock = form.stock.data
        desc = form.description.data
        mftr_date = form.mftr_date.data
        exp_date = form.exp_date.data
        category = request.form.get('category')
        image_1 = request.files['image_1']
      


        image_name = secure_filename(image_1.filename)
        image_uuid = str(uuid.uuid1()) + "_" + image_name
          #save the image
        image_1.save(os.path.join(app.config['UPLOAD_FOLDER'],image_uuid))
        
        #change it to string to save to db
        image_1 = image_uuid
        addpro = AddProduct(name=name,price=price,stock=stock,desc=desc,mftr_date=mftr_date,exp_date=exp_date,category_id=category,image=image_1)
        db.session.add(addpro)
        flash(f'The product {name} has been added to your db', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', form=form, title='Add Product',
                           categories=categories)
  

@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    categories = Category.query.all()
    product = AddProduct.query.get_or_404(id)
    form = Addproducts(request.form)
    if request.method == 'POST':
        product.name = form.name.data 
        product.price = form.price.data 
        product.stock = form.stock.data 
        product.desc = form.description.data 
        product.mftr_date = form.mftr_date.data 
        product.exp_date = form.exp_date.data 
        # product.image = form.image_1
        if request.files.get('image_1'):
        #     os.unlink(os.path.join(current_app.root_path,"static/images/" + product.image))
            image_1 = request.files['image_1']
            image_name = secure_filename(image_1.filename)
            image_uuid = str(uuid.uuid1()) + "_" + image_name
            #save the image
            image_1.save(os.path.join(app.config['UPLOAD_FOLDER'],image_uuid))
            
            #change it to string to save to db
            image_1 = image_uuid
            product.image = image_1
            print(product.image)                
            
        db.session.commit()
        flash('Product has been updated', 'success')
        return redirect('/')

    form.name.data = product.name
    form.price.data = product.price
    form.stock.data = product.stock
    form.description.data = product.desc
    form.mftr_date.data = product.mftr_date
    form.exp_date.data = product.exp_date
    # form.image_1 = product.image
    
    return render_template('products/updateproduct.html', form=form, categories=categories,product=product)
   
   
@app.route('/deleteproduct/<int:id>', methods=["POST"])
def deleteproduct(id):
    product = AddProduct.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} has been deleted', 'success')
        return redirect(url_for('admin'))
    flash(f'Category {product.name} cannot be deleted', 'warning')
    return redirect(url_for('admin'))

