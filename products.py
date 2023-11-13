import mysql.connector
from database_config import get_database_config

def get_all_products():
    with mysql.connector.connect(**get_database_config()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM product")
            return cursor.fetchall()
