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

def add_orders_to_db(user_id, checkout_info,total_price,cart_items):
    with engine.connect() as conn:
        # ## check coupon
        # result = conn.execute(
        #     text("select * from inventory where best_seller_flag = 'y'")
        #
        query = text("insert into Orders (Customer_ID,	Total_Amount,	Status,	Used_Coupon,	Coupon_ID) values (:Customer_ID,	:Total_Amount,	:Status,	:Used_Coupon,	:Coupon_ID)")

        promo_code = None
        coupon_status = 0
        if promo_code:
            coupon_status = 1

        result = conn.execute(
            query,
            {
                        'Customer_ID':user_id,
                        'Total_Amount':total_price,
                        'Status':1,
                        'Used_Coupon':coupon_status,
                        'Coupon_ID':promo_code
            }
        )

        order_id = int(result.lastrowid)



        for k,v in cart_items.items():
            prod = conn.execute(
                text("select * from inventory where product_id = :val"),
                {"val": k}
            )
            prods = prod.all()

            prods_dicts = [r._asdict() for r in prods]

            conn.execute(
                text("INSERT INTO OrderItems (Order_ID,Product_ID,Quantity,Unit_Price,Total_Price) VALUES (:Order_ID,:Product_ID,:Quantity,:Unit_Price,:Total_Price)"),
                {"Order_ID": order_id,
                 "Product_ID": k,
                 "Quantity": v,
                 "Unit_Price": prods_dicts[0]['price'],
                 "Total_Price":round(prods_dicts[0]['price']*v,2)
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


    # Query to check if the product is already in the wishlist
def wishlist_exist_item(user_id, product_id):
    with engine.connect() as conn:
        result = conn.execute(
                text("SELECT 1 FROM WishlistItems a left join Wishlists b using(Wishlist_ID) WHERE b.Customer_ID = :val1 AND a.Product_ID = :val2"),
            {"val1": user_id,
                        "val2": product_id}
                )

        rows = result.all()
        return rows

def wishlist_items(user_id):
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "select * from inventory where Product_ID in (SELECT Product_ID FROM WishlistItems where Wishlist_ID in (select Wishlist_ID from Wishlists where Customer_ID = :val1 ))"),
            {"val1": user_id}
        )

        rows = result.all()
        wishlist_dicts = [r._asdict() for r in rows]

        return wishlist_dicts

    # Insert the product into the WishlistItems table
def wishlist_insert_itme(user_id, product_id):
    with engine.connect() as conn:
        wishlist_check = conn.execute(
                text("SELECT * FROM Wishlists WHERE Customer_ID = :val1"),
            {"val1": user_id}
                )
        rows = wishlist_check.all()
        if rows:
            wishlist_check_dicts = [r._asdict() for r in rows]
            wishlist_id = wishlist_check_dicts[0]["Wishlist_ID"]

            conn.execute(
                    text("INSERT INTO WishlistItems (Wishlist_ID,Product_ID) VALUES (:wishlist_id,:prod_id)"),
                {"wishlist_id": wishlist_id,
                            "prod_id":product_id}
                    )
        else:
            conn.execute(
                    text("INSERT INTO Wishlists (Customer_ID) VALUES (:val1)"),
                {"val1": user_id}
                    )

            wishlist_check = conn.execute(
                text("SELECT * FROM Wishlists WHERE Customer_ID = :val1"),
                {"val1": user_id}
            )

            rows = wishlist_check.all()

            wishlist_check_dicts = [r._asdict() for r in rows]
            wishlist_id = wishlist_check_dicts[0]["Wishlist_ID"]
            conn.execute(
                    text("INSERT INTO WishlistItems (Wishlist_ID,Product_ID) VALUES (:wishlist_id,:prod_id)"),
                {"wishlist_id": wishlist_id,
                            "prod_id":product_id}
                    )

# def user_loader_by_id(user_id):
#     with engine.connect() as conn:
#         user = conn.execute(
#                 text("SELECT * FROM Customer WHERE Customer_ID = :val1"),
#             {"val1": user_id}
#         )
#         if user.all():
#             rows = user.all()
#             user_info = [r._asdict() for r in rows]
#             return user_info

def user_loader_by_name(username):
    with engine.connect() as conn:
        user = conn.execute(
                text("SELECT * FROM Customer WHERE User_Name = :val"),
            {"val": username}
        )
        # print(user.all())
        # print(len(user.all()))
        users = user.all()
        if users:
            user_info = [r._asdict() for r in users]
            return user_info

def insert_new_user(username, password_hash, email,phone):
    with engine.connect() as conn:
            conn.execute(
                    text("INSERT INTO Customer (User_Name,Password,Email,Phone) VALUES (:username, :password_hash, :email,:phone)"),
                {"username": username,
                            "password_hash": password_hash,
                            "email": email,
                            "phone": phone}
                    )