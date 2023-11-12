import mysql.connector
from database_config import get_db_config

def get_all_products():
    with mysql.connector.connect(get_db_config()) as connection:
        with connection.cursor() as cnx:
            cnx.execute("SELECT * FROM product")
            return cnx.fetchall()
