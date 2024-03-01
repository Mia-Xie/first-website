import sqlalchemy
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

