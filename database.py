import mysql.connector as dbapi
from flask import current_app

class Database:
    def __init__(self):
        self.connection = dbapi.connect(
            host = current_app.config["DB_HOST"],
            # port = current_app.config["DB_PORT"],
            user = current_app.config["DB_USER"],
            password = current_app.config["DB_PASSWORD"],
            database = current_app.config["DB_DATABASE"],
        )

    def select_all_employees(self):
        query = """SELECT * FROM employee"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            # return cursor
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def insert_employee(self, employee):
        query = """INSERT INTO employee (employee_id, store_id, firstname,
        lastname, dof, phone, email, status, salary, street, city, country)
        VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                query,
                (
                    employee.employee_id,
                    employee.store_id,
                    employee.firstname,
                    employee.lastname,
                    employee.dof,
                    employee.phone,
                    employee.email,
                    employee.status,
                    employee.salary,
                    employee.street,
                    employee.city,
                    employee.country,
                ),
            )
            self.connection.commit()
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def select_all_rises(self):
        query = """SELECT * FROM rise_archive"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            # return cursor
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def insert_rise(self):
        query = """INSERT INTO rise_archive (rise_id, amount_by_percent,
        rise_date, rise_state) VALUES (%s, %s,%s, %s)"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def get_all_products(self):
        query = """SELECT * FROM product"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)

            products = cursor.fetchall()
            return products
        except dbapi.DatabaseError:
            self.connection.rollback()
            return None
        finally:
            cursor.close()


    def get_all_orders(self):
        query = """SELECT * FROM orders"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            orders = cursor.fetchall()
            return orders

    def get_orders_paged(self, limit=10, offset=0):
        query = """SELECT * FROM orders LIMIT %s OFFSET %s"""

        with self.connection.cursor() as cursor:
            cursor.execute(query, (limit, offset))

            orders = cursor.fetchall()
            return orders
