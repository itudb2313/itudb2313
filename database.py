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

            customers = []

            column_names = [column[0] for column in cursor.description]

            # iterate over the cursor object to get each row
            for row in cursor:
                # create a dictionary using the column names and row values
                row_dict = dict(zip(column_names, row))

                # add the dictionary to the dict_array
                customers.append(row_dict)

            return customers
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def get_customer_by_id(self, customer_id):
        query = """SELECT * FROM customer WHERE customer_id=%s"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (customer_id,))
            customer = []

            column_names = [column[0] for column in cursor.description]

            # iterate over the cursor object to get each row
            for row in cursor:
                # create a dictionary using the column names and row values
                row_dict = dict(zip(column_names, row))

                # add the dictionary to the dict_array
                customer.append(row_dict)

            return customer
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

    def update_customer_by_id(
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
        query = """UPDATE customer SET employee_id = %s, firstname = %s, lastname = %s, dob = %s, email = %s, city = %s, country = %s
        WHERE customer_id = %s"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                query,
                (
                    employee_id,
                    firstname,
                    lastname,
                    dob,
                    email,
                    city,
                    country,
                    customer_id,
                ),
            )
            self.connection.commit()
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def delete_customer_by_id(self, customer_id):
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

    def update_store(self, store_id, employee_id, store_name, phone, street, city, country, email, post_code):
        query = """UPDATE test.store SET employee_id=%s, store_name=%s, phone=%s, street=%s, city=%s, country=%s, email=%s, post_code=%s WHERE store_id=%s;"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                query,
                (
                    employee_id,
                    store_name,
                    phone,
                    street,
                    city,
                    country,
                    email,
                    post_code,
                    store_id,
                ),
            )
            self.connection.commit()
        except dbapi.DatabaseError:
            print("error")
            self.connection.rollback()
        finally:
            cursor.close()

    def delete_store(self, store_id):
        query = """DELETE FROM store WHERE store_id = %s"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (store_id,))
            self.connection.commit()

        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()


    def get_store_by_name(self, store_name,country,phone,street,city,email,post_code):
        query = """SELECT store_id FROM store WHERE store_name=%s AND phone=%s AND street=%s AND city=%s 
                    AND country=%s  AND email=%s AND post_code=%s"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (store_name,phone,street,city,country,email,post_code))
            store = cursor.fetchall()

            return store
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def insert_store(self, employee_id, store_name, phone, street, city, country, email, post_code):
        query = """INSERT INTO store ( employee_id, store_name, phone, street, city, country, email, post_code)
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                query,
                (
                    employee_id,
                    store_name,
                    phone,
                    street,
                    city,
                    country,
                    email,
                    post_code,
                ),
            )
            self.connection.commit()
        except dbapi.DatabaseError:
            print("error")
            self.connection.rollback()
        finally:
            cursor.close()

    def get_all_stores_table(self,order_opt = "store_id",page_number = 1):
        query = "SELECT * FROM store order by "+ order_opt +" limit 20 offset "+ str((int(page_number)-1)*20)
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                query,
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

            employees = []

            column_names = [column[0] for column in cursor.description]

            # iterate over the cursor object to get each row
            for row in cursor:
                # create a dictionary using the column names and row values
                row_dict = dict(zip(column_names, row))

                # add the dictionary to the dict_array
                employees.append(row_dict)

            return employees
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def get_employee_by_id(self, employee_id):
        query = """SELECT * FROM employee WHERE employee_id=%s"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (employee_id,))
            employee = []

            column_names = [column[0] for column in cursor.description]

            # iterate over the cursor object to get each row
            for row in cursor:
                # create a dictionary using the column names and row values
                row_dict = dict(zip(column_names, row))

                # add the dictionary to the dict_array
                employee.append(row_dict)

            return employee
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
        query = """UPDATE employee SET store_id=%s, firstname=%s,
        lastname=%s, dob=%s, email=%s, status=%s, salary=%s, city=%s, country=%s
        WHERE employee_id=%s
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                query,
                (
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
            print(dbapi.DatabaseError)
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

    def delete_employee_by_id(self, employee_id):
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
            rises = []

            column_names = [column[0] for column in cursor.description]

            # iterate over the cursor object to get each row
            for row in cursor:
                # create a dictionary using the column names and row values
                row_dict = dict(zip(column_names, row))

                # add the dictionary to the dict_array
                rises.append(row_dict)

            return rises
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def get_rise_by_id(self, rise_id):
        query = """SELECT * FROM rise_archive WHERE rise_id=%s"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (rise_id,))
            rise = []

            column_names = [column[0] for column in cursor.description]

            # iterate over the cursor object to get each row
            for row in cursor:
                # create a dictionary using the column names and row values
                row_dict = dict(zip(column_names, row))

                # add the dictionary to the dict_array
                rise.append(row_dict)

            return rise
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
        query = """UPDATE rise_archive SET amount_by_percent=%s,
        rise_date=%s, rise_state=%s
        WHERE rise_id=%s
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (amount_by_percent, rise_date, rise_state, rise_id))
            self.connection.commit()
        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def delete_rise_by_id(self, rise_id):
        query = """DELETE FROM rise_archive WHERE rise_id = %s"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (rise_id,))
            self.connection.commit()

        except dbapi.DatabaseError:
            self.connection.rollback()
        finally:
            cursor.close()

    def get_product(self, product_id):
        query = """SELECT * FROM product WHERE product_id = %s"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, (product_id,))
            product = cursor.fetchone()
            return product

    def get_products(
        self,
        search="%%",
        lowest_price=0,
        highest_price=1000000000,
        lowest_km=0,
        highest_km=1000000000,
        color="%%",
        lowest_year=0,
        highest_year=3000,
        page=0,
        order="product_id",
    ):
        select_clause = """SELECT product_id, product_name, model, category_name, year, color, km, price FROM product """
        join_category = """INNER JOIN category USING (category_id) """
        price_filters = """WHERE (price > %s AND price < %s) AND """
        search_filters = (
            """(product_name LIKE %s OR model LIKE %s OR category_name LIKE %s) """
        )
        color_filters = """AND color LIKE %s """
        km_filters = """AND (km > %s AND km < %s) """
        year_filters = """AND (year > %s AND year < %s) """
        order_by = """ORDER BY """ + order + """ LIMIT 10 OFFSET %s"""
        query = (
            select_clause
            + join_category
            + price_filters
            + search_filters
            + color_filters
            + km_filters
            + year_filters
            + order_by
        )
        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    lowest_price,
                    highest_price,
                    search,
                    search,
                    search,
                    color,
                    lowest_km,
                    highest_km,
                    lowest_year,
                    highest_year,
                    page * 10,
                ),
            )
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

    def update_product(
        self,
        product_id,
        product_name,
        model,
        year,
        color,
        price,
        km,
        category_id,
        provider_id,
    ):
        query = """UPDATE product SET product_name=%s, model=%s, year=%s, color=%s, price=%s, km=%s, category_id=%s, provider_id=%s WHERE product_id=%s"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    product_name,
                    model,
                    year,
                    color,
                    price,
                    km,
                    category_id,
                    provider_id,
                    product_id,
                ),
            )
            self.connection.commit()
            return True

    def get_colors(self):
        query = """SELECT DISTINCT(color) FROM product"""
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            unique_colors = cursor.fetchall()
            return unique_colors

    def get_provider_countries(self):
        query = """SELECT DISTINCT(country) FROM provider ORDER BY country"""
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            unique_countries = cursor.fetchall()
            return unique_countries

    def get_provider_cities(self):
        query = """SELECT DISTINCT(city) FROM provider ORDER BY city"""
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            unique_cities = cursor.fetchall()
            return unique_cities

    def get_providers(self, search="%%", start=0, to=999999, country="%%", city="%%"):
        query = """SELECT provider_id, provider_name, email, country, city, debt from provider """
        search_filters = """WHERE (provider_name LIKE %s OR email LIKE %s) """
        debt_filters = """AND (debt > %s AND debt < %s) """
        country_city_filters = """AND country LIKE %s AND city LIKE %s """

        limit = """ORDER BY provider_id DESC LIMIT 10"""
        query += search_filters + debt_filters + country_city_filters + limit
        with self.connection.cursor() as cursor:
            cursor.execute(query, (search, search, start, to, country, city))
            providers = cursor.fetchall()
            return providers

    def get_provider(self, provider_id):
        query = """SELECT provider_id, provider_name, email, country, city, debt FROM provider WHERE provider_id = %s"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, (provider_id,))
            provider = cursor.fetchone()
            return provider

    def update_provider(self, provider_id, provider_name, email, country, city, debt):
        query = """UPDATE provider SET provider_name=%s, email=%s, country=%s, city=%s, debt=%s WHERE provider_id=%s"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                query, (provider_name, email, country, city, debt, provider_id)
            )
            self.connection.commit()
            return True

    def insert_provider(self, provider_name, email, country, city, debt):
        query = """INSERT INTO provider (provider_name, email, country, city, debt) VALUES (%s, %s, %s, %s, %s)"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, (provider_name, email, country, city, debt))
            self.connection.commit()
            return True

    def delete_provider(self, provider_id):
        query = """DELETE FROM provider WHERE provider_id = %s"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, (provider_id,))
            self.connection.commit()
            return True

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
                    """select orders.*, customer.firstname, customer.lastname, product.product_name, product.model, store.store_name, employee.firstname, employee.lastname from orders inner join customer using(customer_id) inner join product using(product_id) inner join store using(store_id) inner join employee on orders.employee_id=employee.employee_id  ORDER BY """
                    + "orders."
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

    def special_queries(self):
        query_monthly = """
                SELECT count(*), MONTH(order_date), YEAR(order_date)  FROM orders 
                GROUP BY MONTH(order_date), YEAR(order_date) ORDER BY YEAR(order_date), MONTH(order_date) ASC
                """

        query_day_of_week = """
                SELECT count(*) FROM orders 
                GROUP BY DAYOFWEEK(order_date)
                """

        query_best_selling = """
                SELECT product.product_name, product.model, SUM(orders.quantity) FROM orders
                INNER JOIN product USING(product_id)
                GROUP BY product.product_name, product.model
                ORDER BY SUM(orders.quantity) DESC
                LIMIT 10
                """

        query_best_grossing = """
                SELECT product.product_name, product.model, SUM(orders.quantity * product.price) FROM orders
                INNER JOIN product USING(product_id)
                GROUP BY product.product_name, product.model
                ORDER BY SUM(orders.quantity * product.price) DESC
                LIMIT 10
                """

        query_best_stores = """
                SELECT store.store_name, SUM(orders.quantity * product.price) FROM orders
                INNER JOIN product USING(product_id)
                INNER JOIN store USING(store_id)
                GROUP BY store.store_name
                ORDER BY SUM(orders.quantity * product.price) DESC
                LIMIT 20
                """

        query_total_sales = """
                SELECT SUM(orders.quantity * product.price) FROM orders
                INNER JOIN product USING(product_id)
                """

        query_total_orders = """
                SELECT COUNT(*) FROM orders
                """

        results = []
        with self.connection.cursor() as cursor:
            cursor.execute(query_monthly)
            data = cursor.fetchall()
            results.append(data)

            cursor.execute(query_day_of_week)
            data = cursor.fetchall()
            results.append(data)

            cursor.execute(query_best_selling)
            data = cursor.fetchall()
            results.append(data)

            cursor.execute(query_best_grossing)
            data = cursor.fetchall()
            results.append(data)

            cursor.execute(query_best_stores)
            data = cursor.fetchall()
            results.append(data)

            cursor.execute(query_total_sales)
            data = cursor.fetchall()
            results.append(data)

            cursor.execute(query_total_orders)
            data = cursor.fetchall()
            results.append(data)

        return results

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

    def get_all_employee_ids_and_names(self, store_id):
        query = """SELECT DISTINCT employee_id, firstname, lastname FROM employee WHERE store_id = %s"""

        with self.connection.cursor() as cursor:
            cursor.execute(query, (store_id,))
            employee_ids = cursor.fetchall()
            return employee_ids

    def get_all_store_ids_and_names(self):
        query = """SELECT store_id, store_name FROM store"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            store_ids = cursor.fetchall()
            return store_ids

    def get_all_product_ids_and_names(self):
        query = """SELECT MIN(product_id), product_name, model FROM product GROUP BY product_name, model"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            product_ids = cursor.fetchall()
            return product_ids

    def get_all_customer_ids_and_names(self):
        query = """SELECT MIN(customer_id), firstname, lastname FROM customer GROUP BY firstname, lastname"""

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            customer_ids = cursor.fetchall()
            return customer_ids
