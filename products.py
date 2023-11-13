import mysql.connector
from database_config import get_database_config

def get_all_products():
    connection = mysql.connector.connect(**get_database_config())
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products
