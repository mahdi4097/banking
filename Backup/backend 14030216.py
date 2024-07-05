import sqlite3
from tkinter import messagebox, Frame, Label, Entry, END, ttk


def clear_frame(frame):
    for widget in frame.winfo_children()[1:]:
        widget.destroy()


def clear_entry(widget):
    for entry in widget.winfo_children():
        if isinstance(entry, Entry):
            entry.config(state="normal")
            entry.delete(0, END)
            entry.config(state="disabled")


def get_data(table: str, column: list = None, condition: str = None):
    with sqlite3.connect("banking.db") as connection:
        cursor = connection.cursor()
        column = ', '.join(column) if column is not None else "*"
        sql = f"SELECT {column} FROM {table} WHERE {condition}" if condition is not None else (f"SELECT {column} FROM"
                                                                                               f" {table}")
        data = cursor.execute(sql).fetchall()
        return data


def fill_admin_info(employee_code, admin_tab):
    column = ["username", "first_name", "last_name", "employee_code", "employee_status", "is_admin"]
    data = get_data("Employee", column, f"employee_code='{employee_code}'")
    index = 0
    map_dictionary = {0: "NO", 1: "Yes"}
    for entry in admin_tab.winfo_children():
        if isinstance(entry, Entry):
            entry.config(state='normal')
            value = data[0][index]
            if index in [4, 5]:
                value = map_dictionary.get(value, value)
            entry.insert(0, value)
            if index not in [3, 4, 5]:
                entry.config(state='disabled')
            index += 1


def get_entry_value(widget):
    entry_value = []
    for entry in widget.winfo_children():
        if isinstance(entry, Entry):
            value = entry.get()
            entry_value.append(value)
    return entry_value


def get_combobox_value(widget):
    combobox_value = []
    for combobox in widget.winfo_children():
        if isinstance(combobox, ttk.Combobox):
            value = combobox.get()
            combobox_value.append(value)

    return combobox_value


def submit_admin_button_clicked(admin_tab):
    combobox_value = get_combobox_value(admin_tab)
    employee_code = combobox_value[0]
    column = ["employee_status", "is_admin"]
    data = get_data("Employee", column, f"employee_code='{employee_code}'")
    combobox_value = [1 if item == 'Yes' else 0 for item in combobox_value[1:]]
    if employee_code:
        if combobox_value != list(*data):
            confirmation = messagebox.askyesno("Warning", "Are you sure you want to submit the changes?")
            if confirmation:
                with sqlite3.connect("banking.db") as connection:
                    cursor = connection.cursor()
                    sql = f"""
        UPDATE Employee
        SET employee_status = '{combobox_value[0]}',is_admin = '{combobox_value[1]}'
        WHERE employee_code = '{employee_code}';
        """
                    cursor.execute(sql)
                    connection.commit()
                    messagebox.showinfo("Awareness", "Changes Has Done")
            else:
                return
        else:
            messagebox.showinfo("Awareness", "Nothing Changed")
    else:
        messagebox.showerror("Error", "Please Select An Employee Code")


def reset_password_button_clicked(tab):
    combobox_value = get_combobox_value(tab)
    employee_code = combobox_value[0]
    if employee_code:
        column = ["last_name", "national_code"]
        data = get_data("Employee", column, f"employee_code='{employee_code}'")
        default_password = f"{data[0][0].title()}@{data[0][1]}"
        with sqlite3.connect("banking.db") as connection:
            cursor = connection.cursor()
            sql = f"""
        UPDATE Employee
        SET password = '{default_password}'
        WHERE employee_code = '{employee_code}';
        """
            cursor.execute(sql)
            connection.commit()
    else:
        messagebox.showerror("Error", "Please Select An Employee Code")


def get_list(table: str, column: list = None, condition: str = None):
    list_result = get_data(table, column, condition)
    return list_result


def employee_list():
    data = get_data("Employee", ["employee_code"])
    employee_code_list = []
    for employee in data:
        employee_code_list.append(employee[0])
    return employee_code_list


def add_employee_button_clicked(employee_tab):
    value = get_entry_value(employee_tab)
    value_list = []
    for item in value:
        value_list.append(" ".join(item.split()).title())
    for index, item in enumerate(value_list):
        if index != 3 and len(item) == 0:
            messagebox.showerror("Error", "Please Complete All Entries")
            return
    try:
        with sqlite3.connect("banking.db") as connection:
            map_dictionary = {'Male': 1, 'Female': 2, 'No': 0, 'Yes': 1}
            value_list = [map_dictionary.get(item, item) for item in value_list]
            cursor = connection.cursor()
            sql = f"""
    INSERT INTO Employee (
                             first_name,
                             last_name,
                             national_code,
                             sex_id,
                             employee_status
                         )
    VALUES (
                             '{value_list[0]}',
                             '{value_list[1]}',
                             '{value_list[2]}',
                             '{value_list[4]}',
                             '{value_list[5]}'
                         );
            """
            cursor.execute(sql)
            connection.commit()
            messagebox.showinfo("Awareness", "New Employee Added")
    except Exception as e:
        print(str(e)[25:])
        print(str(e))
        print(getattr(e, 'message', repr(e)))
        error_message = str(e)[25:]
        if error_message == "first_name GLOB '[a-zA-Z]*' AND first_name NOT GLOB '*[0-9]*' AND first_name NOT GLOB '*[!@#$%^&*()_+{}:<>?]*'":
            messagebox.showerror("Error", "Invalid First Name")
        elif error_message == "last_name GLOB '[a-zA-Z]*' AND last_name NOT GLOB '*[0-9]*' AND last_name NOT GLOB '*[!@#$%^&*()_+{}:<>?]*'":
            messagebox.showerror("Error", "Invalid Last Name")
        elif error_message == "LENGTH(national_code) = 10 AND national_code GLOB '[0-9]*' AND national_code NOT GLOB '[a-zA-Z]*' AND national_code NOT GLOB '*[!@#$%^&*()_+{}:<>?]*'":
            messagebox.showerror("Error", "Invalid National Code.")
        elif str(e)=="UNIQUE constraint failed: Employee.national_code":
            messagebox.showerror("Error","The National Code Is Duplicated")



def login_button_clicked(username, password, frame):
    if username:
        data = get_data("Employee", condition=f"username='{username}'")
        if data:
            if password == data[0][9]:
                if data[0][6] == 1:
                    if data[0][8] == 1:
                        clear_frame(frame)
                        return "Admin"
                else:
                    messagebox.showerror("Error", "User IS Deactivated! Contact Administrator. ")
            else:
                messagebox.showerror("Error", "Invalid username or password")
        else:
            messagebox.showerror("Error", "Invalid username or password")
    else:
        messagebox.showerror("Error", "Please Enter your username!")
