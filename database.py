import mysql.connector as dbapi
from flask import current_app


class Database:
    def __init__(self):
        self.connection = dbapi.connect(
            host=current_app.config["DB_HOST"],
            # port = current_app.config["DB_PORT"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            database=current_app.config["DB_DATABASE"],
        )

    def select_all_customers(self):
        query = """SELECT * FROM customer"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            customers = cursor.fetchall()
            return customers
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def insert_customer(
        self,
        customer_id,
        employee_id,
        firstname,
        lastname,
        dof,
        phone,
        email,
        city,
        country,
    ):
        query = """INSERT INTO customer (customer_id,employee_id,firstname,lastname,dof,phone,email,city,country)
        VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s)"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                query,
                (
                    customer_id,
                    employee_id,
                    firstname,
                    lastname,
                    dof,
                    phone,
                    email,
                    city,
                    country,
                ),
            )
            self.connection.commit()
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def select_all_employees(self):
        query = """SELECT * FROM employee"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            employees = cursor.fetchall()
            return employees
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def insert_employee(
        self,
        employee_id,
        store_id,
        firstname,
        lastname,
        dof,
        phone,
        email,
        status,
        salary,
        street,
        city,
        country,
    ):
        query = """INSERT INTO employee (employee_id, store_id, firstname,
        lastname, dof, phone, email, status, salary, street, city, country)
        VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                query,
                (
                    employee_id,
                    store_id,
                    firstname,
                    lastname,
                    dof,
                    phone,
                    email,
                    status,
                    salary,
                    street,
                    city,
                    country,
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
            rises = cursor.fetchall()
            return rises
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def insert_rise(self, rise_id, amount_by_percent, rise_date, rise_state):
        query = """INSERT INTO rise_archive (rise_id, amount_by_percent,
        rise_date, rise_state) VALUES (%s, %s,%s, %s)"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (rise_id, amount_by_percent, rise_date, rise_state))
            self.connection.commit()
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def get_all_products(self, search):
        select_clause = """SELECT product_name, model, category_name, year, color, km, price FROM product """
        join_category = """INNER JOIN category USING (category_id) """
        search_filters = """WHERE product_name LIKE %s OR model LIKE %s OR category_name LIKE %s"""
        query = select_clause + join_category + search_filters

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (search, search, search))

            products = cursor.fetchall()
            return products
        except dbapi.DatabaseError:
            self.connection.rollback()
            return None
        finally:
            cursor.close()
