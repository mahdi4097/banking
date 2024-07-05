from data import Data
from CTkMessagebox import CTkMessagebox
from pathlib import Path
import hashlib
import sqlite3
import keyring
import os
import re
import random

bank = Data()


# Function to fetch user data from the database
def fetch_user_data():
    bank.data.clear()
    bank.show_data.clear()
    if not os.path.exists("Data/DB/Bank.db"):
        raise ValueError("Database not found.")
    else:
        bank.database_check = True
        with sqlite3.connect("Data/DB/Bank.db") as connection:
            cursor = connection.cursor()
            execute = cursor.execute("""
            SELECT User.id     AS id,
            User.username      AS username,
            User.password      AS password,
            Client.first_name  AS first_name,
            Client.last_name   AS last_name,
            Client.national_id AS national_id,      
            Status.id          AS status,
            Type.id            AS type
            FROM   User
            Inner  Join
            Client
            ON     Client.employee_id = User.username
            Inner  Join
            Status
            ON     Status.id = User.status
            Inner  Join
            Type
            ON     Type.id = User.type""")
            bank.data = execute.fetchall()
            bank.show_data = bank.data.copy()


# Function to add new client data to the database
def add_client_data(new_value):
    with sqlite3.connect("Data/DB/Bank.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO User (username, password, status, type)
            VALUES (?, ?, ?, ?);
        """, (new_value[0], new_value[1], new_value[5], new_value[6]))
        user_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO Client (id, first_name, last_name, national_id, employee_id)
            VALUES (?, ?, ?, ?, ?);
        """, (user_id, new_value[2], new_value[3], new_value[4], new_value[0]))

        connection.commit()


# Function to remove client data from the database
def remove_client_data(client_id):
    with sqlite3.connect("Data/DB/Bank.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM User
            WHERE id = ?;
        """, (client_id,))
        cursor.execute("""
                    DELETE FROM Client
                    WHERE id = ?;
                """, (client_id,))
        connection.commit()


# Function to update client data in the database
def update_client_data(new_value):
    with sqlite3.connect("Data/DB/Bank.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE User
            SET status = ?,
                type = ?
            WHERE id = ?;
        """, (new_value[4], new_value[5], new_value[0]))

        connection.commit()

        cursor.execute("""
            UPDATE Client
            SET first_name = ?,
                last_name = ?,
                national_id = ?
            WHERE id = ?;
        """, (new_value[1], new_value[2], new_value[3], new_value[0]))

        connection.commit()


# Function to update the password for a user
def update_password(username, password):
    password = hash_password(password)
    for item in bank.data:
        if str(item[1]) == username:
            with sqlite3.connect("Data/DB/Bank.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE User
                    SET password = ?
                    WHERE username = ?;
                """, (password, username))

                connection.commit()
            fetch_user_data()


# Function to allow only numbers as input
def only_numbers(char):
    return char.isdigit()


# Function to allow only letters as input
def only_letters(char):
    return char.isalpha() and char.isascii()


# Function to hash a password using MD5
def hash_password(password):
    hash_object = hashlib.md5(password.encode())
    password = hash_object.hexdigest()
    return password


# Function to check the complexity of a password
def check_password_complexity(password):
    pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#()])[A-Za-z\d@$!%*?&#()]{8,}$")
    return bool(pattern.match(password))


# Function to validate the data entered by the user
def data_validation(firstname, lastname, national_id, username, status, user_type):
    if not firstname or not lastname or not national_id:
        raise ValueError("All fields must be filled.")
    elif len(national_id) != 10:
        raise ValueError("National ID must be 10 numbers.")
    elif not status:
        raise ValueError("Please select the user status.")
    elif not user_type:
        raise ValueError("Please select the user type.")
    elif username == "1001":
        if status == 2:
            raise ValueError("The default admin account cannot be inactive.")
        elif user_type == 2:
            raise ValueError("The default admin type cannot be changed.")

    for item in bank.data:
        if str(item[1]) != username:
            if str(item[5]) == national_id:
                raise ValueError("You have already added this national ID.")


# Function to validate the password reset process
def reset_password_validation(password, re_enter_password):
    if password != re_enter_password:
        raise ValueError("Passwords do not match.")
    elif not check_password_complexity(password):
        raise ValueError("Password must be at least 8 characters and complex.")


# Function to add a new user
def add_action(firstname, lastname, national_id, password, status, user_type):
    bank.selected_value = ()
    if len(bank.data) == 0:
        username = 1001
    else:
        last_value = bank.data[-1]
        username = last_value[1] + 1
    password = hash_password(password)
    new_value = (username, password, firstname.capitalize(), lastname.capitalize(), national_id, status, user_type)
    add_client_data(new_value)
    fetch_user_data()
    return username


# Function to update an existing user
def update_action(firstname, lastname, national_id, username, status, user_type):
    for item in bank.show_data:
        if str(item[1]) == username:
            new_value = (item[0], firstname, lastname, national_id, status, user_type)
            update_client_data(new_value)
    fetch_user_data()
    bank.selected_value = ()


# Function to get the value of the selected row
def get_row_value(item_value):
    bank.selected_value = ()
    bank.selected_value = item_value


# Function to ask the user a question before deleting an item
def ask_question():
    msg = CTkMessagebox(title="Delete Item", message="Are you sure you want to delete this item?",
                        icon="warning", option_1="Cancel", option_2="No", option_3="Yes")
    response = msg.get()

    if response == "Yes":
        return True
    else:
        return False


# Function to remove a user
def remove_action():
    if bank.selected_value:

        if ask_question():
            if bank.selected_value[0] == bank.logged_in_user:
                CTkMessagebox(title="Warning",
                              message="You are currently logged in, so you cannot delete this user at the moment.",
                              icon="warning", option_1="OK")
                return False
            elif bank.selected_value[0] == "1001":
                CTkMessagebox(title="Warning",
                              message="You can't delete default admin user.", icon="warning", option_1="OK")
                return False

            for item in bank.show_data:
                if bank.selected_value[0] == str(item[1]):
                    remove_client_data(item[0])
            bank.selected_value = ()
            fetch_user_data()
            return True
    else:
        CTkMessagebox(title="Warning", message="No item is selected!", icon="warning", option_1="OK")
        return False


# Function to search for a user
def search_action(term):
    bank.selected_value = ()
    bank.show_data.clear()
    for item in bank.data:
        if term in str(item[1]) or term in str(item[5]):
            bank.show_data.append(item)
        elif term in str(item[3]) or term in str(item[4]):
            bank.show_data.append(item)


# Function to save credentials using keyring
def save_credentials(srv_name, username, password):
    keyring.set_password(srv_name + "_Username", "username", username)
    keyring.set_password(srv_name + "_Password", username, password)


# Function to load credentials using keyring
def load_credentials():
    username = keyring.get_password(bank.service_name + "_Username", "username")
    password = keyring.get_password(bank.service_name + "_Password", username)
    return username, password


# Function to renew the login credentials
def renew_login(saved_username, saved_password):
    if saved_username:
        keyring.delete_password(bank.service_name + "_Username", "username")
    if saved_password:
        keyring.delete_password(bank.service_name + "_Password", saved_username)


# Function to check the status of the user
def status_check(status):
    if status == 1:
        return True
    else:
        raise ValueError("Login Failed. Your Username is Inactive!")


# Function to validate the login credentials
def login_validation(username, password):
    password = hash_password(password)
    for item in bank.data:
        if username == str(item[1]) and password == item[2]:
            return item[3], item[6], item[7]
    raise ValueError("Login Failed. Check your Username and Password!")


# Function to perform the login action
def login_action(username, password):
    try:
        fetch_user_data()
        login_validation(username, password)
        name, status, user_type = login_validation(username, password)
        permission = status_check(status)
        if not user_type == 1:
            fetch_customer_data()
            bank.user_type = 2
        else:
            bank.user_type = 1
        if permission:
            return name
    except ValueError as error:
        CTkMessagebox(title="Error", message=error.args[0], icon="cancel")


# Function to get the path of the user's avatar
def get_avatar_path(username):
    file_paths = Path("Data/Profile").rglob(f"{username}.*")
    for file_path in file_paths:
        bank.avatar_path = file_path

    if not bank.avatar_path:
        bank.avatar_path = "Data/Profile/default.png"


########################################################################################################################

# Function to fetch customer data from the database
def fetch_customer_data():
    bank.data.clear()
    bank.show_data.clear()
    with sqlite3.connect("Data/DB/Bank.db") as connection:
        cursor = connection.cursor()
        execute = cursor.execute("""
        SELECT id,
        first_name,
        last_name,
        national_id,
        account_number,
        balance,
        status
        FROM Customer;""")
        bank.data = execute.fetchall()
        bank.show_data = bank.data.copy()


# Function to add new customer data to the database
def add_customer_data(new_value):
    with sqlite3.connect("Data/DB/Bank.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Customer (first_name, last_name, national_id, account_number, balance, status)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (new_value[0], new_value[1], new_value[2], new_value[3], new_value[4], new_value[5]))
        connection.commit()


# Function to update existing customer data in the database
def update_customer_data(new_value):
    with sqlite3.connect("Data/DB/Bank.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Customer
            SET first_name = ?,
                last_name = ?,
                national_id = ?,
                status = ?
            WHERE id = ?;
        """, (new_value[1], new_value[2], new_value[3], new_value[4], new_value[0]))

        connection.commit()


# Function to update the balance of a customer's account
def update_customer_balance(account_number, balance):
    with sqlite3.connect("Data/DB/Bank.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Customer
            SET balance = ?
            WHERE account_number = ?;
        """, (balance, account_number))

        connection.commit()


# Function to remove customer data from the database
def remove_customer_data(customer_id):
    with sqlite3.connect("Data/DB/Bank.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM Customer
            WHERE id = ?;
        """, (customer_id,))

        connection.commit()


# Function to generate a unique account number
def generate_account_number():
    account_number = ''.join(["04"]+[str(random.randint(0, 9)) for _ in range(8)])
    for item in bank.data:
        if account_number == item[4]:
            account_number = generate_account_number()
    return account_number


# Function to check the old password against the stored hash
def old_password_check(old_password):
    password = hash_password(old_password)
    for item in bank.data:
        if bank.logged_in_user == str(item[1]):
            if password != item[2]:
                raise ValueError("Please check your old password.")


# Function to search for customers based on a term
def search_customer_action(term):
    bank.selected_value = ()
    bank.show_data.clear()
    for item in bank.data:
        if term in str(item[3]) or term in str(item[4]):
            bank.show_data.append(item)


# Function to add a new customer
def add_customer_action(firstname, lastname, national_id, balance, status):
    bank.selected_value = ()
    account_number = generate_account_number()
    new_value = (firstname.capitalize(), lastname.capitalize(), national_id, account_number, balance, status)
    add_customer_data(new_value)
    fetch_customer_data()
    return account_number


# Function to validate customer data
def customer_data_validation(firstname, lastname, national_id, account_number, balance, status):
    if not firstname or not lastname or not national_id or not balance:
        raise ValueError("All fields must be filled.")
    elif len(national_id) != 10:
        raise ValueError("National ID must be 10 numbers.")
    elif not status:
        raise ValueError("Please select the customer status.")
    for item in bank.data:
        if str(item[4]) != account_number:
            if str(item[3]) == national_id:
                raise ValueError("You have already added this national ID.")


# Function to update an existing customer
def update_customer_action(firstname, lastname, national_id, account_number, status):
    for item in bank.show_data:
        if str(item[4]) == account_number:
            new_value = (item[0], firstname, lastname, national_id, status)
            update_customer_data(new_value)
    fetch_customer_data()
    bank.selected_value = ()


# Function to remove a customer
def remove_customer_action():
    if bank.selected_value:
        if ask_question():
            for item in bank.show_data:
                if bank.selected_value[0] == str(item[3]):
                    remove_customer_data(item[0])
            bank.selected_value = ()
            fetch_customer_data()
            return True
    else:
        CTkMessagebox(title="Warning", message="No item is selected!", icon="warning", option_1="OK")
        return False


# Function to validate a banking operation (withdrawal)
def bank_operation_validation(money, balance):
    if (balance - money) < 0:
        raise ValueError("It is not possible to withdraw more than the balance.")


# Function to check the entries for a banking operation
def check_entries(money, type_variable):
    if not money:
        raise ValueError("Please enter the amount of money.")
    elif not type_variable:
        raise ValueError("Please select one of the Deposit/Withdrawal actions.")


# Function to update the balance of a customer's account
def update_balance_action(account_number, money, balance, type_variable):
    if type_variable == 1:
        balance = balance + money
    else:
        balance = balance - money
    update_customer_balance(account_number, balance)
    fetch_customer_data()
    bank.selected_value = ()
