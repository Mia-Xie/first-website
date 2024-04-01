from flask import Flask,render_template, jsonify, request,session,redirect,url_for,flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user
from werkzeug.security import check_password_hash
from database import engine, load_prods_from_db,load_prod_from_db,load_category_from_db,load_special_from_db,add_orders_to_db,search_product, wishlist_exist_item, wishlist_insert_itme,user_loader_by_name,insert_new_user
import os


app = Flask(__name__)
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

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # The name of the login view

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):
    # Your user loading logic here, possibly querying from MySQL database
    user = User()
    user.id = user_id
    return user

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

@app.route('/categories/<category>')
def show_category(category):
    category_prod = load_category_from_db(category)

    if not category_prod:
        # print(f"No products found for category: {category}")
        return f"Not Found Category:{category}", 404
    else:
        return render_template('categorypage.html',
                               category=category,
                               category_prod=category_prod,
                               company_name='AuroraOrnaments')

@app.route('/<prod_type>')
def show_special(prod_type):
    special_prod = load_special_from_db(prod_type)

    if not special_prod:
        # print(f"No products found for category: {category}")
        return f"Not Found Category:{prod_type}", 404
    else:
        return render_template('special_products.html',
                               prod_type=prod_type,
                               special_prod=special_prod,
                               company_name='AuroraOrnaments')



@app.route('/search')
def search():
    search_term = request.args.get('search_term')
    searched_items_dicts = search_product(search_term)

    return render_template('search_results.html',
                           searched_items_dicts=searched_items_dicts,
                           search_term=search_term)

@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello_auroraornaments'))  # or your preferred page

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # MySQL query to find user by username
        user_record = user_loader_by_name(username)
        if user_record:
            print(user_record[0]['Password'])
            if bcrypt.check_password_hash(user_record[0]['Password'], password):
                user_data = User()

                user_data.id = user_record[0]['Customer_ID']
                login_user(user_data)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('hello_auroraornaments'))  # Redirect to the main page after login
            else:
                flash('Invalid username or password')
        else:
            # If no user found, flash a message asking them to register
            flash('No account found with that username. Please register.', 'warning')
            # Optionally, you can redirect them to the registration page
            return redirect(url_for('register'))
    return render_template('login.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello_auroraornaments'))  # or your preferred page

    if request.method == 'POST':
        username = request.form['new_username']
        print(username)
        password = request.form['new_password']
        email = request.form['new_email']  # Assuming you're collecting email addresses
        phone = request.form['new_phone']  # Assuming you're collecting email addresses
        # MySQL query to check if user exists
        user_record = user_loader_by_name(username)
        print(user_record)
        if user_record:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('hello_auroraornaments'))
        else:
            # Hash the password
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

            # Create a new user instance
            new_user = insert_new_user(username=username, password_hash=password_hash, email=email,phone=phone)
    return render_template('register.html')

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

    data = request.form
    add_orders_to_db(data)
    # DISPLAY AN ACKNOWLEDGE
    return render_template('checkout_successfully.html',
                           checkout_info=data)
    # return jsonify(data)


@app.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
def add_to_wishlist(product_id):

    if not current_user.is_authenticated:
        # Handle the case where the user is not logged in
        flash('You need to login first', 'warning')
        return redirect(url_for('login'))

    user_id = current_user.get_id()
    check_result = wishlist_exist_item(user_id, product_id)

    if check_result:
        flash('Item already in wishlist', 'info')
    else:
        wishlist_insert_itme(user_id, product_id)
    return redirect(url_for('hello_auroraornaments'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
