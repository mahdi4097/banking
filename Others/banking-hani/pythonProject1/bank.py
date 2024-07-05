import sqlite3
import tkinter as tk
from hashlib import sha256
from tkinter import messagebox

# Create a connection to the database
conn = sqlite3.connect('banking.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute("""CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT, is_admin INTEGER)""")
c.execute("""CREATE TABLE IF NOT EXISTS accounts (account_number INTEGER PRIMARY KEY AUTOINCREMENT, owner_name TEXT, 
national_code TEXT, balance REAL DEFAULT 0, is_active INTEGER DEFAULT 1)""")
conn.commit()
conn.close()


def create_user(username, password, is_admin=False):
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute("INSERT INTO users(username, password, is_admin) VALUES(?, ?, ?)",
              (username, sha256(password.encode()).hexdigest(), 1 if is_admin else 0))
    conn.commit()
    conn.close()


def authenticate_user(username, password):
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute("SELECT password, is_admin FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    if user:
        return user[0] == sha256(password.encode()).hexdigest(), user[1]
    return False, False


def get_accounts():
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    accounts = c.fetchall()
    conn.close()
    return accounts


def search_accounts(query):
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute("SELECT * FROM accounts WHERE account_number LIKE ? OR owner_name LIKE ? OR national_code LIKE ?",
              ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    accounts = c.fetchall()
    conn.close()
    return accounts


def create_account(owner_name, national_code):
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute("INSERT INTO accounts(owner_name, national_code) VALUES(?, ?)", (owner_name, national_code))
    conn.commit()
    conn.close()


def deactivate_account(account_number):
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute("UPDATE accounts SET is_active=0 WHERE account_number=?", (account_number,))
    conn.commit()
    conn.close()


def edit_account(account_number, owner_name, national_code):
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute("UPDATE accounts SET owner_name=?, national_code=? WHERE account_number=?",
              (owner_name, national_code, account_number))
    conn.commit()
    conn.close()


def withdraw(account_number, amount):
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM accounts WHERE account_number=?", (account_number,))
    balance = c.fetchone()
    if balance:
        balance = balance[0]
        if balance >= amount:
            c.execute("UPDATE accounts SET balance=balance - ? WHERE account_number=?", (amount, account_number))
            conn.commit()
            messagebox.showinfo("Success", f"Withdrew {amount} from account {account_number}")
        else:
            messagebox.showerror("Error", "Insufficient balance")
    else:
        messagebox.showerror("Error", "Account not found")
    conn.close()


def deposit(account_number, amount):
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute("UPDATE accounts SET balance=balance+? WHERE account_number=?",
              (amount, account_number))
    conn.commit()
    messagebox.showinfo("Success", f"Deposited {amount} to account {account_number}")
    conn.close()


def delete_user(username):
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()


class EditAccountWindow(tk.Toplevel):
    def __init__(self, account_number):
        super().__init__()
        self.title("Edit Account")
        self.account_number = account_number

        self.owner_name_label = tk.Label(self, text="New Owner Name:")
        self.owner_name_label.pack()
        self.new_owner_name_entry = tk.Entry(self)
        self.new_owner_name_entry.pack()

        self.national_code_label = tk.Label(self, text="New National Code:")
        self.national_code_label.pack()
        self.new_national_code_entry = tk.Entry(self)
        self.new_national_code_entry.pack()

        self.confirm_button = tk.Button(self, text="Confirm", command=self.confirm_edit_account, bg="#4CAF50",
                                        fg="white", font=("Helvetica", 12))
        self.confirm_button.pack(pady=10)

    def confirm_edit_account(self):
        new_owner_name = self.new_owner_name_entry.get()
        new_national_code = self.new_national_code_entry.get()
        if new_owner_name and new_national_code:
            edit_account(self.account_number, new_owner_name, new_national_code)
            self.destroy()
