import mysql.connector
from Bank_App.com.service.constants import db_host, db_user, db_password, db_name


# Establish database connection
def db_connect():
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        # print("Connection Established")
        return conn

    except mysql.connector.Error as db_error:
        print('Database Connection Error : ', db_error)
        print()


db_connect()


def insert_data(table_name, **kwargs):
    # establishing connection
    conn = db_connect()
    cursor = conn.cursor()

    try:
        # inserting data into users table
        if table_name == 'users':
            sql = (
                "INSERT INTO users (first_name, last_name, email, dob, salt, password)"
                "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(dob)s, %(salt)s, %(password)s)"
            )

        # inserting data into account table
        elif table_name == 'account':
            sql = (
                "INSERT INTO account (user_id, account_number, balance, is_active)"
                "VALUES (%(user_id)s, %(account_number)s, %(balance)s, %(is_active)s)"
            )

        # inserting data into transaction table
        elif table_name == 'transaction':
            sql = (
                "INSERT INTO transaction (user_id, account_id, amount, from_account, to_account, trans_date, trans_type)"
                "VALUES (%(user_id)s,%(account_id)s, %(amount)s, %(from_account)s, %(to_account)s, NOW(), %(trans_type)s)"
            )
        else:
            raise ValueError("Invalid table name")

        # excuting insert query
        cursor.execute(sql, kwargs)
        conn.commit()
        return

    except mysql.connector.Error as err:
        print("Error in inserting data into database : ", err)
        conn.rollback()  # Rollback in case of any error
        return

    finally:
        conn.commit()
        cursor.close()
        conn.close()


# Example usage:
# insert_data('users', first_name='John', last_name='Doe', email='johndoe@example.com', dob='1990-01-01', salt='randomSalt123', password='hashedPassword456')
# insert_data('account', user_id=1, account_number='1234567890', balance=1000.00, is_active=True)
# insert_data('transaction', user_id=1, account_id=1, amount=200.00, from_account='1234567890', to_account='0987654321', data='2023-09-19', trans_type='db')


def fetch_data(table_name, **kwargs):
    # establishing the connection
    conn = db_connect()
    cursor = conn.cursor()

    try:
        base_sql = f"SELECT * FROM {table_name}"

        # Construct WHERE clause based on provided filters
        filters = " AND ".join([f"{key}=%({key})s" for key in kwargs])

        if filters:
            sql = f"{base_sql} WHERE {filters}"
        else:
            sql = base_sql

        cursor.execute(sql, kwargs)

        # fetching all data based on where clause
        results = cursor.fetchall()

        # print(type(results))
        return results

    except mysql.connector.Error as err:
        print("Error: ", err)
        return []

    finally:
        cursor.close()
        conn.close()


# Example usage:
# users = fetch_data('users', email='johndoe@example.com')
# accounts = fetch_data('account', user_id=1)
# transactions = fetch_data('transaction', user_id=1, account_id=1)
# print(users, accounts, transactions)


def fetch_column_data(table_name, column_name):
    # establishing the connection
    conn = db_connect()
    cursor = conn.cursor()

    try:
        sql = f"SELECT {column_name} FROM {table_name}"
        cursor.execute(sql)
        results = cursor.fetchall()
        return [row[0] for row in results]  # Extracting column values from the result rows

    except mysql.connector.Error as err:
        print("Error : ", err)
        return False

    finally:
        cursor.close()
        conn.close()


# EXAMPLE USAGE
# user_emails = fetch_column_data('account', 'account_number')
# print("User Emails:", user_emails)


def update_data(table_name, values, conditions):
    # establishing the connection
    conn = db_connect()
    cursor = conn.cursor()

    try:
        # construct the SET clause for the UPDATE statement
        set_clause = ", ".join([f"{key}=%({key})s" for key in values])

        # construct the WHERE clause for the UPDATE statement
        where_clause = " AND ".join([f"{key}=%({key})s" for key in conditions])

        sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

        # merge the values and conditions dictionaries for parameter substitution
        params = {**values, **conditions}

        cursor.execute(sql, params)
        conn.commit()

    except mysql.connector.Error as err:
        print('Error : ', err)
        conn.rollback()  # Rollback in case of any error

    finally:
        conn.commit()
        cursor.close()
        conn.close()


# Example usage:
# update_data('users', values={'last_name': 'Smith'}, conditions={'email': 'johndoe@example.com'})
# update_data('accounts', values={'balance': 1200.00}, conditions={'account_number': '1234567890'})
# update_data('transactions', values={'amount': 250.00}, conditions={'trans_id': 1})


def delete_data(table_name, conditions):
    # establish the connection

    conn = db_connect()
    cursor = conn.cursor()

    try:
        # construct the WHERE clause for the DELETE statement
        where_clause = " AND ".join([f"{key}=%({key})s" for key in conditions])

        sql = f"DELETE FROM {table_name} WHERE {where_clause}"

        cursor.execute(sql, conditions)
        conn.commit()

    except mysql.connector.Error as err:
        print("Error : ", err)
        conn.rollback()  # Rollback in case of any error

    finally:
        cursor.close()
        conn.close()


# Example usage:
# delete_data('users', conditions={'email': 'johndoe@example.com'})
# delete_data('account', conditions={'account_number': '1234567890'})
# delete_data('transaction', conditions={'trans_id': 1})


def update_last_login_by_email(user_mail):
    try:
        # connect to the MySQL database
        conn = db_connect()

        # create a cursor to execute SQL queries
        cursor = conn.cursor()

        # update the last_login_date for the user with the given user_id
        update_query = """
            UPDATE users
            SET last_login_date = NOW()
            WHERE email = %s
        """
        cursor.execute(update_query, (user_mail,))

        # commit the changes to the database
        conn.commit()

        # close the cursor and the database connection
        cursor.close()
        conn.close()
        return

    except mysql.connector.Error as err:
        print("Error in updating last login time : ", err)
        return

# insert_data('users', first_name='John', last_name='Doe', email='johndoe@example.com', dob='1990-01-01', salt='randomSalt123', password='hashedPassword456')
# insert_data('account', user_id=1, account_number='1234567890', balance=1000.00, is_active=True)
# insert_data('transaction', user_id=1, account_id=1, amount=200.00, from_account='1234567890', to_account='0987654321', date='2023-09-19', trans_type='db')
# accounts = fetch_data('account', user_id=1)
# users = fetch_column_data('users','email')
# accounts = fetch_data('users', email='example@gmail.com')
# transactions = fetch_data('transaction', user_id=1, account_id=1)
# print(accounts)
# print(accounts[0][8])
# print(type(accounts[0][8]))
# users = fetch_data('users', email='johndoe@example.com')
# print(users)
# print(users[0][4])
# print(accounts)
# print(transactions)


# update_data('users', values={'last_name': 'Smith'}, conditions={'email': 'johndoe@example.com'})
# update_data('account', values={'balance': 1200.00}, conditions={'account_number': '1234567890'})
# update_data('transaction', values={'amount': 250.00}, conditions={'trans_id': 1})
