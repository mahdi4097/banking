from tkinter import Tk, Label, Entry,Button
from tkinter.ttk import Combobox
import sqlite3
start = Tk()
start.title("Start")

username_label = Label(start, text="User Name")
username_label.grid(row=1, column=0, padx=(0, 10), pady=(0, 10))

password_label = Label(start, text="PassWord")
password_label.grid(row=2, column=0, padx=(0, 10), pady=(0, 10))

username_entry = Entry(start, width=30)
username_entry.grid(row=1, column=1)

password_entry = Entry(start, width=30)
password_entry.grid(row=2, column=1)

error_label = Label(start, text="")
error_label.grid(row=3, column=1, padx=(0, 10), pady=(0, 10))

# ----------------1---------------------------
def enter_button_clicked():
    user = username_entry.get()
    passw = password_entry.get()
    # user = "narges"
    # passw = "123"
    with sqlite3.connect("Bank.db") as connection:
        cursor = connection.cursor()
        execute = cursor.execute("""
        SELECT *
        FROM UserPass
        """)
        data = execute.fetchall()
        # print(data)
        for i in data:
            if i[1] == user and i[2] == passw:
                # print(i[0])
                connection.commit()
                select = Tk()
                select.title("Select")
                start.destroy()
#----------------


# ------------2-----------------------------
                def admin_management_button_clicked():
                    admin = Tk()
                    admin.title("Admin Management")

                    def create_table_header():
                        row_label = Label(admin, text="No")
                        row_label.grid(row=1, column=0, padx=10, pady=(0, 10))

                        user_label = Label(admin, text="User Name")
                        user_label.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))

                        pass_label = Label(admin, text="password")
                        pass_label.grid(row=1, column=2, padx=(0, 10), pady=(0, 10))

                    create_table_header()
                    entry_list = []

                    def create_table_body():
                        for entry in entry_list:
                            entry.destroy()

                            entry_list.clear()
                        with sqlite3.connect("Bank.db") as connection:
                            curses = connection.cursor()
                            execute = curses.execute("""
                                                                           SELECT Id,
                                                                           UserName,
                                                                           PassWord
                                                                           FROM UserPass
                                                                     """)
                        data = execute.fetchall()
                        # print(data)
                        row_number = 1
                        for account in data:
                            row_entry = Entry(admin, width=15)
                            row_entry.insert(0, row_number)
                            row_entry.grid(row=row_number + 1, column=0)
                            entry_list.append(row_entry)

                            user_entry = Entry(admin, width=15)
                            user_entry.insert(0, account[1])
                            user_entry.grid(row=row_number + 1, column=1)
                            entry_list.append(user_entry)

                            pass_entry = Entry(admin, width=15)
                            pass_entry.insert(0, account[2])
                            pass_entry.grid(row=row_number + 1, column=2)
                            entry_list.append(pass_entry)

                            row_number += 1

                    create_table_body()
                    # -----
                    def new_admin_button_clicked():

                        new_admin = Tk()
                        new_admin.title("New Admin")

                        username_label = Label(new_admin, text="User Name")
                        username_label.grid(row=1, column=0, padx=(0, 10), pady=(0, 10))

                        password_label = Label(new_admin, text="PassWord")
                        password_label.grid(row=2, column=0, padx=(0, 10), pady=(0, 10))

                        username_entry = Entry(new_admin, width=30)
                        username_entry.grid(row=1, column=1)

                        password_entry = Entry(new_admin, width=30)
                        password_entry.grid(row=2, column=1)

                        def submit_button_clicked():
                            user_name = username_entry.get()
                            password = password_entry.get()

                            with sqlite3.connect("Bank.db") as connection:
                                cursor = connection.cursor()
                                cursor.execute(f"""
                                                                                              INSERT INTO UserPass (
                                                                                              UserName,
                                                                                              PassWord
                                                                                          )
                                                                                              VALUES (
                                                                                              '{user_name}',
                                                                                              '{password}'
                                                                                       )
                                                                                       """)
                                connection.commit()
                                new_admin.destroy()
                                create_table_body()

                        submit_button = Button(new_admin, text="Submit", width=15, command=submit_button_clicked)
                        submit_button.grid(row=4, column=1, pady=10, padx=(5, 10), sticky="w")

                        # new_admin.mainloop()

                    # admin.mainloop()

                    new_admin_button = Button(admin, text="New Admin",width=15, command=new_admin_button_clicked)
                    new_admin_button.grid(row=0, column=0, pady=10, padx=(5, 10), sticky="w")

                    # select.mainloop()

                # ----------------22
                admin_management_button = Button(select, text="Admin Management", width=30, command = admin_management_button_clicked)
                admin_management_button.grid(row=1, column=1, padx=10, pady=(10, 10), sticky="w")

                def bank_account_management_button_clicked():

                    window = Tk()
                    window.title("Bank")

                    search_entry = Entry(window, width=30)
                    search_entry.grid(row=0, column=3)

                    def search_boutton_clicked():
                        term = search_entry.get()
                        create_table_body(term)

                    search_button = Button(window, text="Search", command=search_boutton_clicked)
                    search_button.grid(row=0, column=4, padx=(5, 10), sticky="w")

                    def show_person_form(id=None, f_name=None, l_name=None, national_code=None, phone=None,
                                         accountNumber=None, balance=None, accountStatus=None):

                        person_form = Tk()
                        if id:
                            person_form.title("update Person")
                        # ----------------------------------------------------
                        else:
                            person_form.title("Creat Person")

                        first_name_label = Label(person_form, text="first name")
                        first_name_label.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))

                        first_name_entry = Entry(person_form)
                        first_name_entry.grid(row=2, column=1, padx=(0, 10), pady=(0, 10))
                        if f_name:
                            first_name_entry.insert(0, f_name)

                        last_name_label = Label(person_form, text="last name")
                        last_name_label.grid(row=1, column=2, padx=(0, 10), pady=(0, 10))

                        last_name_entry = Entry(person_form)
                        last_name_entry.grid(row=2, column=2, padx=(0, 10), pady=(0, 10))
                        if l_name:
                            last_name_entry.insert(0, l_name)

                        national_code_label = Label(person_form, text="national code")
                        national_code_label.grid(row=1, column=3, padx=(0, 10), pady=(0, 10))

                        national_code_entry = Entry(person_form)
                        national_code_entry.grid(row=2, column=3, padx=(0, 10), pady=(0, 10))
                        if national_code:
                            national_code_entry.insert(0, national_code)

                        phone_label = Label(person_form, text="phone")
                        phone_label.grid(row=1, column=4, padx=(0, 10), pady=(0, 10))

                        phone_entry = Entry(person_form)
                        phone_entry.grid(row=2, column=4, padx=(0, 10), pady=(0, 10))
                        if phone:
                            phone_entry.insert(0, phone)

                        account_label = Label(person_form, text="Account Number")
                        account_label.grid(row=1, column=5, padx=(0, 10), pady=(0, 10))

                        account_entry = Entry(person_form)
                        account_entry.grid(row=2, column=5, padx=(0, 10), pady=(0, 10))
                        if accountNumber:
                            account_entry.insert(0, accountNumber)

                        Balance_label = Label(person_form, text="Balance")
                        Balance_label.grid(row=1, column=6, padx=(0, 10), pady=(0, 10))

                        Balance_entry = Entry(person_form)
                        Balance_entry.grid(row=2, column=6, padx=(0, 10), pady=(0, 10))
                        if balance:
                            Balance_entry.insert(0, balance)

                        def get_statuse_list():
                            account_list = []
                            with sqlite3.connect("Bank.db") as connection:
                                cursor = connection.cursor()
                                execute = cursor.execute("""
                                SELECT Id,
                                    Status
                                FROM AccountStatus
                                """)
                                data = execute.fetchall()
                                # print(data)
                                for account in data:
                                    account_list.append(f"{account[0]}-{account[1]}")
                            return account_list

                        accountStatus_Id_label = Label(person_form, text="Account Status")
                        accountStatus_Id_label.grid(row=1, column=7, padx=(0, 10), pady=(0, 10))

                        accountStatus_Id_combobox = Combobox(person_form, values=get_statuse_list())
                        accountStatus_Id_combobox.grid(row=2, column=7, pady=(0, 10), padx=10, sticky="w")
                        if accountStatus:
                            print(accountStatus)
                            # Balance_entry.insert(0, balance)

                            accountStatus_Id_combobox.insert(0, accountStatus)

                        def submit_button_clicked():
                            f_name = first_name_entry.get()
                            l_name = last_name_entry.get()
                            national_code = national_code_entry.get()
                            phone = phone_entry.get()
                            accountNumber = account_entry.get()
                            balance = float(Balance_entry.get())
                            accountStatus = accountStatus_Id_combobox.get().split("-")[0]

                            if id:
                                with sqlite3.connect("Bank.db") as connection:
                                    cursor = connection.cursor()
                                    cursor.execute(f"""
                                    UPDATE Account
                       SET
                           FirstName = '{f_name}',
                           LastName = '{l_name}',
                           NationalCode = '{national_code}',
                           Phone = '{phone}',
                           AccountNumber = '{accountNumber}',
                           Balance = {balance},
                           AccountStatus_Id = '{accountStatus}'
                     WHERE Id = '{id}'
                                    """)

                            else:
                                with sqlite3.connect("Bank.db") as connection:
                                    cursor = connection.cursor()
                                    cursor.execute(f"""
                                    INSERT INTO Account (
                                                FirstName,
                                                LastName,
                                                NationalCode,
                                                Phone,
                                                AccountNumber,
                                                Balance,
                                                AccountStatus_Id
                                            )
                                           VALUES (
                                               '{f_name}',
                                               '{l_name}',
                                               '{national_code}',
                                               '{phone}',
                                               '{accountNumber}',
                                                {balance},
                                               '{accountStatus}'

                                           )
                                    """)
                            connection.commit()
                            person_form.destroy()
                            create_table_body()

                        submit_button = Button(person_form, text="Submit", command=submit_button_clicked)
                        submit_button.grid(row=3, column=2, pady=(0, 10), sticky="w")

                        # person_form.mainloop()

                    new_person_button = Button(window, text="New Account", command=show_person_form)
                    new_person_button.grid(row=0, column=1, pady=10, padx=(0, 10))

                    # window.mainloop()

                    def create_table_header():

                        row_label = Label(window, text="No")
                        row_label.grid(row=1, column=0, padx=10, pady=(0, 10))

                        f_name_label = Label(window, text="first name")
                        f_name_label.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))

                        l_name_label = Label(window, text="last name")
                        l_name_label.grid(row=1, column=2, padx=(0, 10), pady=(0, 10))

                        national_code_label = Label(window, text="national code")
                        national_code_label.grid(row=1, column=3, padx=(0, 10), pady=(0, 10))

                        phone_label = Label(window, text="phone")
                        phone_label.grid(row=1, column=4, padx=(0, 10), pady=(0, 10))

                        account_number_label = Label(window, text="account number")
                        account_number_label.grid(row=1, column=5, padx=(0, 10), pady=(0, 10))

                        balance_label = Label(window, text="balance")
                        balance_label.grid(row=1, column=6, padx=(0, 10), pady=(0, 10))

                        account_status_label = Label(window, text="account status")
                        account_status_label.grid(row=1, column=7, padx=(0, 10), pady=(0, 10))

                    create_table_header()
                    entry_list = []

                    def create_table_body(term=""):
                        for entry in entry_list:
                            entry.destroy()

                        entry_list.clear()

                        with sqlite3.connect("Bank.db") as connection:
                            curses = connection.cursor()
                            execute = curses.execute("""
                    select
                            Account.id as id,
                            FirstName,
                            LastName,
                            NationalCode,
                            phone,
                            AccountNumber,
                            Balance,
                            Status,
                            AccountStatus_Id
                      FROM Account
                      inner join AccountStatus on account.AccountStatus_Id  = AccountStatus.id
                      """)

                        data = execute.fetchall()
                        # print(data)

                        row_number = 1
                        for account in data:
                            if term in (account[3] or account[5]):
                                row_entry = Entry(window, width=5)
                                row_entry.insert(0, row_number)
                                row_entry.grid(row=row_number + 1, column=0)
                                entry_list.append(row_entry)

                                first_name_entry = Entry(window, width=15)
                                first_name_entry.insert(0, account[1])
                                first_name_entry.grid(row=row_number + 1, column=1)
                                entry_list.append(first_name_entry)

                                last_name_entry = Entry(window, width=15)
                                last_name_entry.insert(0, account[2])
                                last_name_entry.grid(row=row_number + 1, column=2)
                                entry_list.append(last_name_entry)

                                national_code_entry = Entry(window, width=15)
                                national_code_entry.insert(0, account[3])
                                national_code_entry.grid(row=row_number + 1, column=3)
                                entry_list.append(national_code_entry)

                                phone_entry = Entry(window, width=15)
                                phone_entry.insert(0, account[4])
                                phone_entry.grid(row=row_number + 1, column=4)
                                entry_list.append(phone_entry)

                                AccountNumber_entry = Entry(window, width=15)
                                AccountNumber_entry.insert(0, account[5])
                                AccountNumber_entry.grid(row=row_number + 1, column=5)
                                entry_list.append(AccountNumber_entry)

                                Balance_entry = Entry(window, width=15)
                                Balance_entry.insert(0, account[6])
                                Balance_entry.grid(row=row_number + 1, column=6)
                                entry_list.append(Balance_entry)

                                Status_entry = Entry(window, width=15)
                                Status_entry.insert(0, (f"{account[8]}-{account[7]}"))
                                Status_entry.grid(row=row_number + 1, column=7)
                                entry_list.append(Status_entry)

                                def update_account(account_id, f_name, l_name, national_code, phone, accountNumber,
                                                   balance, accountStatus):
                                    show_person_form(account_id, f_name, l_name, national_code, phone, accountNumber,
                                                     balance,
                                                     accountStatus)

                                update_button = Button(window, text="Update",
                                                       command=lambda id=account[0],
                                                                      f_name=account[1], l_name=account[2],
                                                                      national_code=account[3],
                                                                      phone=account[4], accountNumber=account[5],
                                                                      balance=account[6],
                                                                      accountStatus=f"{account[8]}-{account[7]}":
                                                       update_account(id, f_name, l_name, national_code, phone,
                                                                      accountNumber, balance,
                                                                      accountStatus))
                                update_button.grid(row=row_number + 1, column=8, padx=(7, 10))
                                entry_list.append(update_button)

                                row_number += 1

                    create_table_body()

                    # window.mainloop()

                bank_account_management_button = Button(select, text="Bank Account Management", width=30, command=bank_account_management_button_clicked)
                bank_account_management_button.grid(row=2, column=1, padx=10, pady=(10, 10), sticky="w")

            else:
                error_label.config(text="Error",fg="red")

enter_button = Button(start, text="enter", width=20, command=enter_button_clicked)
enter_button.grid(row=4, column=1, pady=(0, 10), sticky="w")
start.mainloop()
