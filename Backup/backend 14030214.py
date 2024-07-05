import sqlite3
from tkinter import messagebox, Frame, Label


def get_data(table_name: str, columns: list = None, condition: str = None):
    with sqlite3.connect("banking.db") as connection:
        cursor = connection.cursor()
        columns = ', '.join(columns) if columns is not None else "*"
        sql = f"SELECT {columns} FROM {table_name} WHERE {condition}" if condition else f"SELECT {columns} FROM {table_name}"

        data = cursor.execute(sql).fetchall()
        return data


def fill_admin_info(employee_code):
    data = get_data("Employee", condition=f"employee_code='{employee_code}'")
    # print(data)


def employee_list():
    with sqlite3.connect("banking.db") as connection:
        cursor = connection.cursor()
        sql = """
SELECT id,
                   first_name,
                   last_name,
                   national_code,
                   employee_code,
                   sex_id,
                   employee_status_id
FROM Employee;
                    """
        data = cursor.execute(sql).fetchall()
        employee_list = []
        for employee in data:
            employee_list.append(employee[4])
    return employee_list


def clear_frame(frame):
    for widget in frame.winfo_children()[1:]:
        widget.destroy()


def add_employee_button_clicked():
    # TODO: Complete code.
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


def gender(gender_combobox):
    selected_gender = gender_combobox.get()
    # print(f"Selected Gender: {selected_gender}")


def status(status_combobox):
    global selected_status
    selected_status = status_combobox.get()
    # print(selected_status)


def login_button_clicked(username, password, frame):
    if username:
        with sqlite3.connect("banking.db") as connection:
            cursor = connection.cursor()
            sql = f"""
SELECT *
FROM Employee
WHERE username='{username}'
"""
            data = cursor.execute(sql).fetchall()
            print(data)
            data=get_data("Employee",condition=f"username='{username}'")
            print(data)
            if data:
                if password == data[0][9]:
                    if data[0][6] == 1:
                        if data[0][8] == 1:
                            clear_frame(frame)
                            return "Admin"
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
