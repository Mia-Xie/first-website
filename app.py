from flask import Flask,render_template, jsonify
from database import engine, load_prod_from_db

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
    products = load_prod_from_db()
    return render_template('home.html',
                           products=products,
                           company_name='AuroraOrnaments')

@app.route('/api/products')
def list_products():
    products = load_prod_from_db()
    return jsonify(products)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
