import sqlite3
from tkinter import messagebox, Frame, Label


def button_add_employee_clicked():
    with sqlite3.connect("banking.db") as connection:
        cursor = connection.cursor()
        sql = """
        INSERT INTO Employee (
                         first_name,
                         last_name,
                         national_code,
                         sex_id,
                         employee_status_id
                     )
                     VALUES (
                         'first_name',
                         'last_name',
                         'national_code',
                         'sex_id',
                         'employee_status_id'
                     );
"""


def clear_frame(frame):
    for widget in frame.winfo_children()[1:]:
        widget.destroy()


def gender(gender_combobox):
    selected_gender = gender_combobox.get()
    print(f"Selected Gender: {selected_gender}")


def status(status_combobox):
    global selected_status
    selected_status = status_combobox.get()
    print(selected_status)


def btn_login_clicked(username, password, frame):
    if username:
        with sqlite3.connect("banking.db") as connection:
            cursor = connection.cursor()
            sql = f"""
SELECT *
FROM User
WHERE username='{username}'
"""
            login_result = cursor.execute(sql).fetchall()
            if login_result:
                if password == login_result[0][2]:
                    if login_result[0][4] == 1:
                        if login_result[0][1] in ["Admin", "Admin1", "Admin2"]:
                            clear_frame(frame)
                            return "Admin"  # TODO:Admin code
                    else:
                        messagebox.showerror("Error", "User IS Deactivated! Contact Administrator. ")
                # employee_status_id_result = cursor.execute(sql).fetchall()
                # print(employee_status_id_result)
                else:
                    messagebox.showerror("Error", "Invalid username or password")
            else:
                messagebox.showerror("Error", "Invalid username or password")
    else:
        messagebox.showerror("Error", "Please Enter your username!")
