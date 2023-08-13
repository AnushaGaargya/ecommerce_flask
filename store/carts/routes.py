from flask import redirect,render_template,url_for,flash,request,session
from store import db, app
from store.products.models import AddProduct, Category


#to combine the existing shopping cart items(if there are any) with the newly added ones
def MergeDict(dict1, dict2):
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/addcart', methods=["POST"])
def AddCart():
    try:
        #get all the details on the request posted by the user for adding a product to the cart
        product_id = request.form.get('product_id')
        check_route = request.form.get('check_route')
        product_stock = request.form.get('stock')
        quantity = request.form.get('quantity')
        products = AddProduct.query.all()
        product = AddProduct.query.filter_by(id=product_id).first()
        # print(products)
        # print(quantity)
        if request.method == "POST":
            DictItems = {product_id:{'name':product.name, 'price': product.price, 'quantity': quantity, 'image': product.image, 'stock':product.stock}}
            # print(DictItems)
            #check if there are products already added in the cart
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                #check if a particular product being added is in the cart already
                if product_id in session['Shoppingcart']:
                    for key,item in session['Shoppingcart'].items():
                        #if so update the quantity accordingly
                        if int(key) == int(product_id):
                            #check if req is coming from details page
                            if check_route:
                                # print(product_stock)
                                #if it is from the details page, add whatever quantity is provided there to the existing quantity in the cart
                                session.modified = True
                                x = int(item['quantity'])
                                x += int(quantity)
                                #update the quantity only if the total quantity added is available in the stock
                                if x <= int(product_stock):                
                                    item['quantity'] = int(x)    
                            #if req is from the index page, add 1 to the existing quantity of that product in the cart.
                            # this takes care of updating the quantity each time 'Add Cart' is clicked in the home page.    
                            else:
                                session.modified = True
                                x = int( item['quantity'])
                                x += 1
                                item['quantity'] = int(x) 
                #if product being added is not in the cart, add it to the cart by merging the existing cart and the details of the product being added
                else:
                    session['Shoppingcart'] = MergeDict(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            #if there is no product added to the cart, create a session variable(Shoppingcart) with the details of the product added
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
    #if the cart is empty, take the user to the home page(upon clicking 'cart' in navbar)
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
        return redirect(url_for('home'))
    #calculate the subtotal for each product, multiplying the quantity with price(per unit)
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
                #check the product that needs to be updated in the cart, and update its quantity to the quantity entered on the req form
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
            #check the product that needs to be deleted and remove it from the cart by popping it out from the session
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))


@app.route('/clearcart')
def clearcart():
    try:
        #this just clears the cart but the user session will be available(user will still be logged in)
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
    


@app.route('/empty')
def empty_cart():
    try:
        #this clears the cart and logs out the user
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)


# @app.route('/checkout')
# def checkout():
#     #check if the customer is logged in(when the customer is logged in, the session will have a variable 'email')
#     #if customer has not logged in, redirect to the login page
#     if 'email' not in session:
#         print("not in session")
#         flash('Please login first', 'danger')
#         return redirect(url_for('customerLogin'))
#     #if customer has logged in, update the stock in the db, by subtracting the quantity of each product checked out.    
#     else:
#         print("in session")
#         try:
#             # session.modified = True
#             for key, item in session['Shoppingcart'].items():
#                 # item['stock'] = item['stock'] - item['quantity']
#                 product = AddProduct.query.get(int(key))
#                 print(product)
#                 print(product.stock)
#                 product.stock = int(product.stock) - int(item['quantity'])
#                 print(product.stock)
#                 db.session.commit()
#                 flash('Items checked out. Continue Shopping...')
#                 return redirect(url_for('clearcart'))
            
#         except Exception as e:
#             print(e)


