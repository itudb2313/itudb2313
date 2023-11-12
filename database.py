import mysql.connector as dbapi


class Database:
    def __init__(self):
        self.connection = dbapi.connect(
            host="localhost",
            port=3306
            user="root", 
            password= "test",
            database="AutomotiveBusiness"
        )

    def selectAllEmployee(self):
        selectAllEmployees = """SELECT * FROM employee"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(selectAllEmployees)
            return cursor
        except: dbapi.DatabaseError:
            connection.rollback()
        finally:
            cursor.close()
            


    def insertEmployee(self, employee):
        insertEmployeeQuery = """INSERT INTO employee (employee_id, store_id, firstname, lastname, dof, phone, email, status, salary, street, city, country) VALUES (%s, %s)"""

        try:
            cursor = self.connection.cursor()
            cursor.execute(insertEmployeeQuery, (employee.employee_id, employee.store_id, employee.firstname, employee.lastname, employee.dof, employee.phone, employee.email, employee.status, employee.salary, employee.street, employee.city, employee.country))
            connection.commit()
        except: dbapi.DatabaseError:
            connection.rollback()
        finally:
            cursor.close()