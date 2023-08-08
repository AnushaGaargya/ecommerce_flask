from flask import redirect,render_template,url_for,flash,request,session, current_app
from store import db, app
from store.products.models import AddProduct, Category

def MergeDict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/addcart', methods=["POST"])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        products = AddProduct.query.all()
        product = AddProduct.query.filter_by(id=product_id).first()
        # if product_id not in products:
        #     DictItems = {{}}
        # else:

        if request.method == "POST":
            DictItems = {product_id:{'name':product.name, 'price': product.price, 'quantity': quantity, 'image': product.image}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key,item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MergeDict(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)
    

@app.route('/carts')
def getCart():
    categories = Category.query.all()
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key,product in session['Shoppingcart'].items():
        subtotal += float(product['price']) * int(product['quantity'])
        grandtotal = subtotal 

    return render_template('products/carts.html', grandtotal=grandtotal, categories=categories)



@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0: 
        return redirect(url_for('home'))
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash('Item is updated')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))


@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
    


@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)



