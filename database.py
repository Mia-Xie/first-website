from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STR']
engine = create_engine(db_connection_string,
                       connect_args={
                           "ssl": {
                               "ca": "/etc/ssl/cert.pem"
                           }
                       }
                       )


def load_prods_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from inventory"))
        result_dicts = [r._asdict() for r in result.all()]
        return result_dicts

def load_prod_from_db(product_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("select * from inventory where product_id = :val"),
            {"val": product_id}
        )

        rows = result.all()
        if len(rows)==0:
            return None
        else:
            return rows[0]._asdict()

def load_category_from_db(category):
    with engine.connect() as conn:
        result = conn.execute(
            text("select * from inventory where category = :val"),
            {"val": category}
        )

        rows = result.all()
        if len(rows)==0:
            return None
        else:
            category_dicts = [r._asdict() for r in rows]
            return category_dicts
def load_special_from_db(prod_type):
    with engine.connect() as conn:
        if prod_type == 'Best-Sellers':
            result = conn.execute(
                text("select * from inventory where best_seller_flag = 'y'")
        )
        elif prod_type == 'Sales':
            result = conn.execute(
                text("select * from inventory where on_sale_flag = 'y'")
            )
        else:
            return None

        rows = result.all()

        special_items_dicts = [r._asdict() for r in rows]
        return special_items_dicts

def load_special_from_db(prod_type):
    with engine.connect() as conn:
        if prod_type == 'Best-Sellers':
            result = conn.execute(
                text("select * from inventory where best_seller_flag = 'y'")
        )
        elif prod_type == 'Sales':
            result = conn.execute(
                text("select * from inventory where on_sale_flag = 'y'")
            )
        else:
            return None

        rows = result.all()

        special_items_dicts = [r._asdict() for r in rows]
        return special_items_dicts

def add_orders_to_db(checkout_info):
    with engine.connect() as conn:
        query = text("insert into orders_details_raw (first_name,	last_name,	email,	address1,	address2,	state,	zip_code,	country,	same_address,	save_info,	payment_method,	promo_code) values (:first_name,	:last_name,	:email,	:address1,	:address2,	:state,	:zip_code,	:country,	:same_address,	:save_info,	:payment_method, 'na')")

        conn.execute(
            query,
            {
                        'first_name':checkout_info['firstName'],
                        'last_name':checkout_info['lastName'],
                        'email':checkout_info['email'],
                        'address1':checkout_info['address1'],
                        'address2':checkout_info['address2'],
                        'state':checkout_info['state'],
                        'zip_code':checkout_info['zip_code'],
                        'country':checkout_info['country'],
                        'same_address':checkout_info['same_address'],
                        'save_info':checkout_info['save_info'],
                        'payment_method':checkout_info['paymentMethod']
                        # 'promo_code':checkout_info['promo_code']
            }
        )

def search_product(search_term):
    with engine.connect() as conn:
        result = conn.execute(
                text("select * from inventory where product_name LIKE :val OR description LIKE :val"),
            {"val": "%{}%".format(search_term)}
                )

        rows = result.all()
        searched_items_dicts = [r._asdict() for r in rows]

        return searched_items_dicts