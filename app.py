from flask import Flask,render_template, jsonify
from database import engine, load_prods_from_db,load_prod_from_db


app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
