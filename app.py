from flask import Flask,render_template, jsonify
app = Flask(__name__)

PROD = [
    {'id':1,
     'title': 'necklace with heart',
     'price': 49.99,
     'in stock':'y'
    },
    {'id': 2,
     'title': 'necklace 2',
     'price': 49.99,
     'in stock':'y'
     },
    {'id': 3,
     'title': 'necklace 3',
     'price': 49.99,
    'in stock':'n'
     }
]
@app.route('/')
def hello_world():
    return render_template('home.html',
                           products=PROD,
                           company_name='AuroraOrnaments')

@app.route('/api/products')
def list_products():
    return jsonify(PROD)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
