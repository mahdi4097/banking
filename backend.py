import sqlite3
from tkinter import messagebox, Frame, Label, Entry, END, ttk, Tk

map_value_text_yes_no = {0: "No", 1: "Yes", "": ""}
map_value_text_gender = {1: 'Male', 2: 'Female', "": ""}
map_text_value = {"Male": 1, "Female": 2, "No": 0, "Yes": 1, "": ""}


def only_numeric_input(P):
    if P.isdigit() or P == "":
        return True
    else:
        return False


def only_alpha_input(P):
    if P.replace(" ", "").isalpha() or P == "":
        return True
    else:
        return False


def clear_frame(frame):
    for widget in frame.winfo_children()[1:]:
        widget.destroy()


def clear_entry(widget):
    widget_name = widget.winfo_name()
    for entry in widget.winfo_children():
        if isinstance(entry, Entry):
            entry.config(state="normal")
            entry.delete(0, END)
            if widget_name == "employee_tab" and entry.winfo_name() in ["!entry4", "!combobox", "!combobox2"]:
                entry.config(state='readonly')
            elif widget_name == "customer_operation_frame" and entry.winfo_name() not in ["!entry", "!entry8"]:
                entry.config(state='readonly')
            elif widget_name == "customer_user_frame" and entry.winfo_name() in ["!combobox", "!combobox2"]:
                entry.config(state='readonly')


def get_data(table: str, column: list = None, condition: str = None, search_parameter: tuple = None):
    with sqlite3.connect("banking.db") as connection:
        cursor = connection.cursor()
        column = ', '.join(column) if column is not None else "*"
        query = f"SELECT {column} FROM {table} WHERE {condition}" if condition is not None else (f"SELECT {column} FROM"
                                                                                                 f" {table}")
        data = cursor.execute(
            query, search_parameter
        ).fetchall() if search_parameter is not None else cursor.execute(
            query
        ).fetchall()
        return data


def fill_admin_info(employee_code, admin_tab):
    column = ["username", "first_name", "last_name", "employee_code", "employee_status", "is_admin"]
    data = get_data("Employee", column, f"employee_code='{employee_code}'")
    index = 0
    for entry in admin_tab.winfo_children():
        if isinstance(entry, Entry):
            entry.config(state='normal')
            value = data[0][index]
            if index in [4, 5]:
                value = map_value_text_yes_no.get(value, value)
            entry.insert(0, value)
            entry.config(state="readonly")
            index += 1


def get_entry_value(widget):
    entry_value = []
    for entry in widget.winfo_children():
        if isinstance(entry, Entry):
            value = entry.get()
            entry_value.append(value)
    value_list = []
    for item in entry_value:
        value_list.append(" ".join(item.split()).title())
    return value_list


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
            confirmation = messagebox.askyesno(
                "Warning", "Are you sure you want to submit the changes?", parent=admin_tab
            )
            if confirmation:
                with sqlite3.connect("banking.db") as connection:
                    cursor = connection.cursor()
                    query = f"""
        UPDATE Employee
        SET employee_status = '{combobox_value[0]}',is_admin = '{combobox_value[1]}'
        WHERE employee_code = '{employee_code}';
        """
                    cursor.execute(query)
                    connection.commit()
                    messagebox.showinfo("Awareness", "Changes Has Done.", parent=admin_tab)
            else:
                return
        else:
            messagebox.showinfo("Awareness", "Nothing Changed!", parent=admin_tab)
    else:
        messagebox.showerror("Error", "Please Select An Employee Code.", parent=admin_tab)


def reset_password_button_clicked(tab):
    combobox_value = get_combobox_value(tab)
    employee_code = combobox_value[0]
    if employee_code:
        column = ["last_name", "national_code"]
        data = get_data("Employee", column, f"employee_code='{employee_code}'")
        default_password = f"{data[0][0].title()}@{data[0][1]}"
        with sqlite3.connect("banking.db") as connection:
            cursor = connection.cursor()
            query = f"""
        UPDATE Employee
        SET password = '{default_password}'
        WHERE employee_code = '{employee_code}';
        """
            cursor.execute(query)
            connection.commit()
    else:
        messagebox.showerror("Error", "Please Select An Employee Code.", parent=tab)
        return
    messagebox.showinfo("Awareness", "Password Changed To Default Value.", parent=tab)


def employee_list():
    data = get_data("Employee", ["employee_code"])
    employee_code_list = []
    for employee in data:
        employee_code_list.append(employee[0])
    return employee_code_list


def add_person_button_clicked(widget):
    entry_value = get_entry_value(widget)
    if widget.winfo_name() == "customer_user_frame":
        entry_value.insert(3, "")
        status = "customer_status"
        table = "Customer"
        column = ["first_name", "last_name", "account_number", "national_code"]
        text_message1 = "National Code:"
        text_message2 = "Account Number: "
    else:
        status = "employee_status"
        table = "Employee"
        column = ["first_name", "last_name", "employee_code", "username"]
        text_message1 = "username: "
        text_message2 = "Code: "

    for index, item in enumerate(entry_value):
        if index != 3 and len(item) == 0:
            messagebox.showerror("Error", "Please Complete All Entries.", parent=widget)
            return
    value_list = [map_text_value.get(item, item) for item in entry_value]
    try:
        with sqlite3.connect("banking.db") as connection:
            cursor = connection.cursor()
            query = f"""
    INSERT INTO {table} (
                             first_name,
                             last_name,
                             national_code,
                             sex_id,
                             {status}
                         )
    VALUES (
                             '{value_list[0]}',
                             '{value_list[1]}',
                             '{value_list[2]}',
                             '{value_list[4]}',
                             '{value_list[5]}'
                         );
            """
            cursor.execute(query)
            connection.commit()

            data = get_data(table, column, f"national_code='{value_list[2]}'")
        messagebox.showinfo(
            "Awareness", f""
                         f"{data[0][0]} {data[0][1]} Added As New {table} \n\n {text_message1}: "
                         f"{data[0][3]}\n {table} {text_message2}: "
                         f"{data[0][2]}", parent=widget
        )
        clear_entry(widget)
    except Exception as e:
        error_message = str(e)[25:]
        if error_message == "first_name GLOB '[a-zA-Z]*' AND first_name NOT GLOB '*[0-9]*' AND first_name NOT GLOB '*[!@#$%^&*()_+{}:<>?]*'":
            messagebox.showerror("Error", "Invalid First Name!", parent=widget)
        elif error_message == "last_name GLOB '[a-zA-Z]*' AND last_name NOT GLOB '*[0-9]*' AND last_name NOT GLOB '*[!@#$%^&*()_+{}:<>?]*'":
            messagebox.showerror("Error", "Invalid Last Name!", parent=widget)
        elif error_message == "LENGTH(national_code) = 10 AND national_code GLOB '[0-9]*' AND national_code NOT GLOB '[a-zA-Z]*' AND national_code NOT GLOB '*[!@#$%^&*()_+{}:<>?]*'":
            messagebox.showerror("Error", "Invalid National Code.", parent=widget)
        elif str(e) == "UNIQUE constraint failed: Employee.national_code":
            messagebox.showerror("Error", "The National Code Is Duplicated!", parent=widget)
        else:
            messagebox.showerror("Error", "An Unknown Error Occurred!\n Contact Administrator.", parent=widget)
            print(str(e))
        return


def show_list(
        widget: str = None, table: str = None, column: list = None, condition: str = None,
        search_parameter: tuple = None
):
    column = column
    data = get_data(table=table, column=column, condition=condition, search_parameter=search_parameter)

    list_view = Tk()
    if "is_admin" in column:
        title = "List of Employees"
    elif "customer_status" in column:
        title = "List of Customers"
    else:
        title = "List oF Administrators"
    list_view.title(title)
    screen_width = list_view.winfo_screenwidth()
    screen_height = list_view.winfo_screenheight()
    list_view.geometry(f"1000x500+{int(screen_width / 2) - 500}+{int(screen_height / 2) - 250}")
    list_view.minsize(600, 400)
    list_view.call("wm", "attributes", ".", "-topmost", "1")
    list_view.focus_force()
    widget.wm_state('iconic')

    def close_button_clicked():
        widget.deiconify()
        widget.attributes('-disabled', 0)
        list_view.destroy()

    widget.attributes('-disabled', 1)
    list_view.protocol("WM_DELETE_WINDOW", close_button_clicked)

    style = ttk.Style(list_view)
    style.theme_use("clam")  # "clam", "alt", "default", "classic", "vista"
    style.configure("Treeview.Heading", font=("Calibri", 12, "bold"))
    style.configure("Treeview", font=("Helvetica", 12), rowheight=30)
    style.map("Treeview", background=[("selected", "lightgrey")], foreground=[("selected", "black")])

    header = [item.replace("_", " ").title() for item in column]
    tree = ttk.Treeview(list_view, columns=header, show="headings")
    tree.tag_configure("Inactive", foreground="lightgrey", background="")

    for item in header:
        tree.heading(item, text=item)

    for item in data:
        status = "Active" if item[-1] == 1 else "Inactive"
        if title == "List of Employees":
            is_admin_value = map_value_text_yes_no.get(item[-2])
            tag = ("Inactive",) if status == "Inactive" else ()
            *val, active_flag, _ = item
            tree.insert("", "end", values=(*val, is_admin_value, status), tags=tag)

        else:
            tag = ("Inactive",) if status == "Inactive" else ()
            *val, active_flag = item
            tree.insert("", "end", values=(*val, status), tags=tag)

    vsb = ttk.Scrollbar(list_view, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(list_view, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")

    tree.pack(expand=True, fill="both")

    def treeview_sort_column(tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children("")]
        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

    for col in header:
        tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree, _col, False))

    list_view.mainloop()


def search_button_clicked(widget, window=None):
    entry_value = get_entry_value(widget)
    if not any(value.strip() for value in entry_value):
        messagebox.showerror("Error", "Please Fill In At Least One Entry.", parent=widget)
        return

    search_subject = widget.winfo_name()
    if search_subject == "employee_tab":
        column = ["employee_code", "first_name", "last_name", "national_code", "username", "is_admin",
                  "employee_status"]
        table = "Employee"
        status_condition = "employee_status"

    else:
        column = ["account_number", "first_name", "last_name", "national_code", "customer_status"]
        table = "Customer"
        status_condition = "customer_status"
        entry_value.insert(3, "")

    condition = f"""
                        first_name LIKE '%' || ? || '%'
                        AND last_name LIKE '%' || ? || '%'
                        AND national_code LIKE '%' || ? || '%'
                        AND sex_id LIKE '%' || ? || '%'
                        AND {status_condition} LIKE '%' || ? || '%';      
"""
    first_name = entry_value[0]
    last_name = entry_value[1]
    national_code = entry_value[2]
    sex_id = map_text_value.get(entry_value[4])
    status = map_text_value.get(entry_value[5])
    search_parameter = (first_name, last_name, national_code, sex_id, status)

    show_list(widget=window, table=table, column=column, condition=condition, search_parameter=search_parameter)


def find_customer_button_clicked(widget):
    entry_value = get_entry_value(widget)
    if not entry_value[0].strip():
        messagebox.showerror("Error", "Please Fill In Account Number.", parent=widget)
        return
    try:
        account_number = entry_value[0]
        search_parameter = (account_number,)
        table = "Customer"
        condition = """
                     account_number = ?
                    """
        data = list(get_data(table=table, condition=condition, search_parameter=search_parameter)[0])
        with sqlite3.connect("banking.db") as condition:
            cursor = condition.cursor()
            query = f'''
                        SELECT {data[0]},
                        SUM(debit) AS total_debit,
                        SUM(credit) AS total_credit
                        FROM Account
                        WHERE customer_id = {data[0]}
            '''
            turnover = cursor.execute(query).fetchall()[0]
            total_debit = int(turnover[1])
            total_credit = int(turnover[2])
            balance = total_credit - total_debit
        data = [data[0], data[4], data[3], data[1], data[2], total_credit, total_debit, balance]
        entry_list = []
        for entry in widget.winfo_children():
            entry_list.append(entry)

        for index in range(10, 17):
            entry_list[index].config(state='normal')
            entry_list[index].delete(0, END)
            entry_list[index].insert(
                0, data[index - 9]
            )
            entry_list[index].config(state='disable') if index in range(11, 17) else None
    except:
        messagebox.showerror("Error", "Invalid Account Number!", parent=widget)
        return


def record_button_clicked(widget, employee_id):
    entry_value = get_entry_value(widget)
    if not entry_value[1]:
        messagebox.showerror("Error", "Please Fill In Account Number And Then Click Find.", parent=widget)
        return
    if len(entry_value[7]) == 0:
        messagebox.showerror("Error", "Please Enter The Amount.", parent=widget)
        return
    elif len(entry_value[8]) == 0:
        messagebox.showerror("Error", "Please Select The Operation.", parent=widget)
        return
    customer_id = get_data(table="Customer", condition=f"account_number={entry_value[0]}")[0][0]
    balance = int(entry_value[6])
    amount = int(entry_value[7])
    operation = entry_value[8]
    if operation == "Withdrawal":
        if balance - amount < 0:
            messagebox.showerror(
                "Insufficient Credit", "The Customer's Account Balance Is Less Than The Withdrawal "
                                       "Request.", parent=widget
            )
            return
        operation = "debit"
    else:
        operation = "credit"

    with sqlite3.connect("banking.db") as connection:
        cursor = connection.cursor()
        query = f'''
        INSERT INTO Account (
                        customer_id,
                        employee_id,
                        {operation}
                    )
                    VALUES (
                        '{customer_id}',
                        '{employee_id}',
                        '{amount}'
                    );
        '''
        cursor.execute(query, )
        messagebox.showinfo(
            "Awareness", f"The Amount Of {amount} Rials\n Was Recorded In The {operation} Of\n {entry_value[2]} "
                         f"{entry_value[3]} "
                         f"account.", parent=widget
        )
    clear_entry(widget)


def finish_button_clicked(widget1, widget2):
    widget2.deiconify()
    widget2.attributes('-disabled', 0)
    widget1.destroy()


def login_button_clicked(username, password, frame):
    if username:
        data = get_data(table="Employee", condition=f"username='{username}'")
        if data:
            if password == data[0][9]:
                if data[0][6] == 1:
                    clear_frame(frame)
                    if data[0][8] == 1:
                        return "admin", data[0][0]
                    else:
                        return "user", data[0][0]

                else:
                    messagebox.showerror("Error", "The User Has Been Deactivated!\n Contact Administrator.")
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showerror("Error", "Invalid username or password.")
    else:
        messagebox.showerror("Error", "Please Enter your username!")
