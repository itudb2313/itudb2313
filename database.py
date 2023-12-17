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

    def select_all_categories(self):
        query = """SELECT * FROM category"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            categories = cursor.fetchall()
            return categories
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

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
        dob,
        email,
        city,
        country,
    ):
        query = """INSERT INTO customer
        (customer_id,employee_id,firstname,lastname,dob,email,city,country)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                query,
                (
                    customer_id,
                    employee_id,
                    firstname,
                    lastname,
                    dob,
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

    def delete_customer(self, customer_id):
        query = """DELETE FROM customer WHERE customer_id = %s"""
        print(customer_id)
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (customer_id,))
            self.connection.commit()

        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def get_stores_columns(self):
        query = """show columns from store"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)

            stores_column_names = cursor.fetchall()
            return stores_column_names
        except dbapi.DatabaseError:
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    def get_stores_count(self):
        query = """select count(*) from store"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)

            store_count = cursor.fetchall()
            return store_count[0][0]
        except dbapi.DatabaseError:
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def get_all_stores(self):
        query = """SELECT * FROM store"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)

            stores = cursor.fetchall()
            return stores
        except dbapi.DatabaseError:
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def get_stores_columns(self):
        query = """show columns from store"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)

            stores_column_names = cursor.fetchall()
            return stores_column_names
        except dbapi.DatabaseError:
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def get_all_stores_table(self,order_opt = "store_id",page_number = 1):
        query = "SELECT * FROM store order by "+ order_opt +" limit 20 offset "+ str((int(page_number)-1)*20)
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, 
                            )

            stores = cursor.fetchall()
            return stores
        except dbapi.DatabaseError:
            self.connection.rollback()
            return None
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

    def update_employee_by_id(
        self,
        employee_id,
        store_id,
        firstname,
        lastname,
        dob,
        email,
        status,
        salary,
        city,
        country,
    ):
        query = """UPDATE employee SET employee_id=%s, store_id=%s, firstname=%s,
        lastname=%s, dob=%s, email=%s, status=%s, salary=%s, city=%s, country=%s
        WHERE employee_id=%s
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                query,
                (
                    employee_id,
                    store_id,
                    firstname,
                    lastname,
                    dob,
                    email,
                    status,
                    salary,
                    city,
                    country,
                    employee_id,
                ),
            )
            self.connection.commit()
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
        dob,
        email,
        status,
        salary,
        city,
        country,
    ):
        query = """INSERT INTO employee (employee_id, store_id, firstname,
        lastname, dob, email, status, salary, city, country)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                query,
                (
                    employee_id,
                    store_id,
                    firstname,
                    lastname,
                    dob,
                    email,
                    status,
                    salary,
                    city,
                    country,
                ),
            )
            self.connection.commit()
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def delete_employee(self, employee_id):
        query = """DELETE FROM employee WHERE employee_id = %s"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (employee_id,))
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

    def update_rise_by_id(self, rise_id, amount_by_percent, rise_date, rise_state):
        query = """UPDATE rise_archive SET rise_id=%s, amount_by_percent=%s,
        rise_date=%s, rise_state=%s
        WHERE rise_id=%s
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                query, (rise_id, amount_by_percent, rise_date, rise_state, rise_id)
            )
            self.connection.commit()
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def delete_rise(self, rise_id):
        query = """DELETE FROM rise_archive WHERE rise_id = %s"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (rise_id,))
            self.connection.commit()

        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def get_products(self, search):
        select_clause = """SELECT product_id, product_name, model, category_name, year, color, km, price FROM product """
        join_category = """INNER JOIN category USING (category_id) """
        search_filters = """WHERE product_name LIKE %s OR model LIKE %s OR category_name LIKE %s ORDER BY product_id DESC LIMIT 10"""
        query = select_clause + join_category + search_filters

        with self.connection.cursor() as cursor:
            cursor.execute(query, (search, search, search))
            products = cursor.fetchall()
            return products

    def insert_product(
        self, product_name, model, year, color, price, km, category_id, provider_id
    ):
        query = """INSERT INTO product (product_name, model, year, color, price, km, category_id, provider_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                (product_name, model, year, color, price, km, category_id, provider_id),
            )
            self.connection.commit()
            return True

    def delete_product(self, product_id):
        query = """DELETE FROM product WHERE product_id = %s"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, (product_id,))
            self.connection.commit()
            return True

    def get_provider_countries(self):
        query = """SELECT DISTINCT(country) FROM provider"""
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            unique_countries = cursor.fetchall()
            return unique_countries

    def get_providers(self, search="%%", start="", to=""):
        query = """SELECT provider_id, provider_name, phone, email, country, city, debt from provider """
        search_filters = (
            """WHERE (provider_name LIKE %s OR country LIKE %s OR city LIKE %s) """
        )
        debt_filters = ""
        if start != "":
            debt_filters = """AND debt > %s """ % (start)
        if to != "":
            debt_filters += """AND debt < %s """ % (to)

        query += search_filters + debt_filters
        with self.connection.cursor() as cursor:
            cursor.execute(query, (search, search, search))
            providers = cursor.fetchall()
            return providers

    def get_all_orders(self):
        query = """SELECT * FROM orders"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            orders = cursor.fetchall()
            return orders

    def get_orders_paged(self, limit=10, offset=0, order_by="order_id", order="ASC"):
        sortable_columns = [
            "order_id",
            "order_date",
            "ship_date",
            "required_date",
            "order_status",
            "quantity",
        ]

        with self.connection.cursor() as cursor:
            # we need to check if the column name is valid since
            # execute() will put single quotes around the column name
            if order_by in sortable_columns and order in ["ASC", "DESC"]:
                cursor.execute(
                    "SELECT * FROM orders ORDER BY "
                    + order_by
                    + " "
                    + order
                    + " LIMIT %s OFFSET %s",
                    (limit, offset),
                )
            else:
                return []

            orders = cursor.fetchall()
            return orders

    def delete_order(self, order_id):
        query = """DELETE FROM orders WHERE order_id = %s"""

        with self.connection.cursor() as cursor:
            cursor.execute(query, (order_id,))
            # self.connection.commit()

    def insert_order(
        self,
        customer_id,
        product_id,
        store_id,
        employee_id,
        order_date,
        ship_date,
        required_date,
        order_status,
        quantity,
    ):
        query = """INSERT INTO orders (customer_id, product_id, store_id,
        employee_id, order_date, ship_date, required_date, order_status, quantity)
        VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s)"""

        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    customer_id,
                    product_id,
                    store_id,
                    employee_id,
                    order_date,
                    ship_date,
                    required_date,
                    order_status,
                    quantity,
                ),
            )
            # self.connection.commit()

    def monthly_order(self):
        query = """
                SELECT count(*), MONTH(order_date), YEAR(order_date)  FROM orders 
                GROUP BY MONTH(order_date), YEAR(order_date) ORDER BY YEAR(order_date), MONTH(order_date) ASC
                """

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            return data

    def update_order(
        self,
        order_id,
        customer_id,
        product_id,
        store_id,
        employee_id,
        order_date,
        ship_date,
        required_date,
        order_status,
        quantity,
    ):
        query = """UPDATE orders SET customer_id=%s, product_id=%s, store_id=%s,
        employee_id=%s, order_date=%s, ship_date=%s, required_date=%s, order_status=%s, quantity=%s WHERE order_id=%s
        """

        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    customer_id,
                    product_id,
                    store_id,
                    employee_id,
                    order_date,
                    ship_date,
                    required_date,
                    order_status,
                    quantity,
                    order_id,
                ),
            )
            # self.connection.commit()
