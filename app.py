from flask import Flask,render_template, jsonify, request,session,redirect,url_for
from database import engine, load_prods_from_db,load_prod_from_db
import os


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'optional_default_secret_key')
# PROD = [
#     {'id':1,
#      'title': 'necklace with heart',
#      'price': 49.99,
#      'in stock':'y'
#     },
#     {'id': 2,
#      'title': 'necklace 2',
#      'price': 49.99,
#      'in stock':'y'
#      },
#     {'id': 3,
#      'title': 'necklace 3',
#      'price': 49.99,
#     'in stock':'n'
#      }
# ]


@app.route('/')
def hello_auroraornaments():
    products = load_prods_from_db()
    return render_template('home.html',
                           products=products,
                           company_name='AuroraOrnaments')

@app.route('/api/products')
def list_products():
    products = load_prods_from_db()
    return jsonify(products)


@app.route('/products/<product_id>')
def show_products(product_id):
    product = load_prod_from_db(product_id)
    if not product:
        return "Not Found", 404
    else:
        return render_template('productpage.html',
                               prod=product,
                               company_name='AuroraOrnaments')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cart')
def shopping_cart():
    cart_items_list = session.get('cart', [])
    products = load_prods_from_db()

    cart_items = {}
    total_price = 0
    for prod in cart_items_list:
        if prod in cart_items:
            # If the number is already a key in the dictionary, increment its value
            cart_items[prod] += 1
            total_price+=products[prod-1]['price']
        else:
            # Otherwise, add the number as a key with a value of 1
            cart_items[prod] = 1
            total_price+=products[prod - 1]['price']

    return render_template('shopping_cart.html',
                           # cart_items_list=session.get('cart', []),
                           cart_items=cart_items,
                           products=products,
                           total_price=[round(total_price,2),round(10,2),round(total_price*0.06675,2),round(total_price+total_price*0.06675,2),round(total_price+total_price*0.06675,2)+10])


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    # Assuming each product_id is unique
    session['cart'].append(product_id)  # Add product to cart
    session.modified = True  # Notify Flask that the session has been modified

    return redirect(url_for('hello_auroraornaments'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    # Ensure there's a cart in the session
    if 'cart' in session:
        # Remove the item if it's in the cart
        session['cart'] = [item for item in session['cart'] if item != product_id]
        session.modified = True  # Inform Flask that the session has been modified
    return redirect(url_for('shopping_cart'))
@app.route('/checkout')
def checkout():
    cart_items_list = session.get('cart', [])
    products = load_prods_from_db()

    cart_items = {}
    total_price = 0
    for prod in cart_items_list:
        if prod in cart_items:
            # If the number is already a key in the dictionary, increment its value
            cart_items[prod] += 1
            total_price+=products[prod-1]['price']
        else:
            # Otherwise, add the number as a key with a value of 1
            cart_items[prod] = 1
            total_price+=products[prod - 1]['price']

    return render_template('checkout.html',
                           cart_items=cart_items,
                           products=products,
                           total_price=[round(total_price,2),round(10,2),round(total_price*0.06675,2),round(total_price+total_price*0.06675,2),round(total_price+total_price*0.06675,2)+10]
                           )


@app.route('/checkout/status',methods=['post'])
def checkout_status():
    # STORE TO DB
    # DISPLAY AN ACKNOWLEDGE
    data = request.form
    return render_template('checkout_successfully.html',
                           checkout_info=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
