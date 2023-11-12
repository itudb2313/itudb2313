from flask import current_app as app

def get_db_config():
    return {
        'host': app.config["DB_HOST"],
        'user': app.config["DB_USER"],
        'password': app.config["DB_PASSWORD"],
        'database': app.config["DB_DATABASE"],
        'auth_plugin': 'mysql_native_password',
        }
