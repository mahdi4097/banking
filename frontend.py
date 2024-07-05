from tkinter import Tk, Label, Entry, Button, Frame, StringVar, ttk
from PIL import Image, ImageTk
from backend import *


def window_geometry(window: str) -> None:
    """
    Sets the size of Tk() based on widgets and resolution of display.
    :param window:
    :return: None
    """
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    window.geometry(
        f"{window_width}x{window_height}+{(screen_width - window_width) // 2}+"
        f"{(screen_height - window_height) // 2}"
    )
    window.resizable(width=False, height=False)


# ================= Login Page
# <editor-fold desc="Login Page">
root = Tk()
image_path = "background.png"
image = Image.open(image_path)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
image = image.resize((screen_width, screen_height))
photo = ImageTk.PhotoImage(image)
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.attributes('-fullscreen', True)

frame = Frame(root, bg='')
frame.place(x=0, y=0)
label = Label(frame, image=photo)
label.pack(fill="both", expand=True)


def login_page():
    username_label = Label(frame, text="Username:", font=("Tahoma", 12), bg="#E2E9F2")
    username_label.place(anchor='center', relx=0.35, rely=0.68)
    password_label = Label(frame, text="Password:", font=("Tahoma", 12), bg="#E2E9F2")
    password_label.place(anchor='center', relx=0.35, rely=0.71)

    username_entry = Entry(frame, width=27, font=("Tahoma", 12), bg="#E2E9F2")
    username_entry.place(anchor='center', relx=0.45, rely=0.68)
    username_entry.focus()

    password = StringVar()
    password_entry = Entry(frame, width=27, textvariable=password, show='*', font=("Tahoma", 12), bg="#E2E9F2")
    password_entry.place(anchor='center', relx=0.45, rely=0.71)

    def login_check():
        login_value = login_button_clicked(
            username_entry.get(), password_entry.get(), frame
        )
        if login_value:
            global employee_id
            employee_id = login_value[1]
            if login_value[0] == "admin":
                admin_logged_in()
            elif login_value[0] == "user":
                user_logged_in()
            else:
                return

    login_button = Button(
        frame, text="Login", width=12, font=("Tahoma", 12), bg="#E2E9F2", command=login_check
    )
    login_button.place(anchor='center', relx=0.413, rely=0.745)

    exit_button = Button(frame, text="Exit", width=12, font=("Tahoma", 12), bg="#E2E9F2", command=root.destroy)
    exit_button.place(anchor='center', relx=0.487, rely=0.745)

    root.mainloop()


# </editor-fold>


# ================= Admin Window
def admin_logged_in():
    # <editor-fold desc="Admin Window">
    win_admin = Tk()
    win_admin.title("Administrator Panel")
    win_admin.call("wm", "attributes", ".", "-topmost", "1")
    win_admin.protocol("WM_DELETE_WINDOW", lambda: None)
    tab_control = ttk.Notebook(win_admin)
    admin_tab = Frame(tab_control, borderwidth=3, pady=5, relief="groove", name="admin_tab")
    # flat, groove, raised, ridge, solid, or sunken
    employee_tab = Frame(tab_control, borderwidth=3, pady=5, relief="groove", name="employee_tab")
    tab_control.add(employee_tab, text="Employee ")
    tab_control.add(admin_tab, text="Admin")
    tab_control.grid(row=0, column=0, padx=(15, 15), pady=10)
    win_admin.update()
    win_admin.deiconify()
    # </editor-fold>

    # ================= Employee Tab
    # <editor-fold desc="Employee Tab">
    first_name_label = Label(employee_tab, text="First Name")
    first_name_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="w")
    last_name_label = Label(employee_tab, text="Last Name")
    last_name_label.grid(row=0, column=2, padx=(10, 5), pady=(10, 5), sticky="w")
    gender_label = Label(employee_tab, text="Gender")
    gender_label.grid(row=0, column=4, padx=(10, 5), pady=(10, 5), sticky="w")
    national_code_label = Label(employee_tab, text="National Code")
    national_code_label.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
    username_label = Label(employee_tab, text="username")
    username_label.grid(row=1, column=2, padx=(10, 5), pady=5, sticky="w")
    status_label = Label(employee_tab, text="Is Active")
    status_label.grid(row=1, column=4, padx=(10, 5), pady=5, sticky="w")

    text_validator = (employee_tab.register(only_alpha_input), '%P')
    number_validator = (employee_tab.register(only_numeric_input), '%P')
    first_name_entry = Entry(employee_tab, width=15, validate="key", validatecommand=text_validator)
    first_name_entry.grid(row=0, column=1, pady=(10, 5), sticky="w")
    last_name_entry = Entry(employee_tab, width=20, validate="key", validatecommand=text_validator)
    last_name_entry.grid(row=0, column=3, pady=(10, 5), sticky="w")
    national_code_entry = Entry(employee_tab, width=15, validate="key", validatecommand=number_validator)
    national_code_entry.grid(row=1, column=1, pady=(10, 5), sticky="w")
    username_entry = Entry(employee_tab, width=20, state='disabled', disabledbackground="#FAFAFA", relief="solid")
    username_entry.grid(row=1, column=3, padx=(0, 10), pady=5, sticky="w")

    gender_var = StringVar()
    gender_combobox = ttk.Combobox(employee_tab, width=10, textvariable=gender_var, state='readonly')
    gender_combobox["values"] = ("", "Male", "Female")
    gender_combobox.grid(row=0, column=5, padx=(0, 10), pady=(10, 5), sticky="w")

    status_var = StringVar()
    status_combobox = ttk.Combobox(employee_tab, width=10, textvariable=status_var, state='readonly')
    status_combobox["values"] = ("", "Yes", "No")
    status_combobox.grid(row=1, column=5, pady=5, sticky="w")

    separator = ttk.Separator(employee_tab, orient='horizontal')
    separator.grid(row=3, columnspan=6, padx=10, sticky='ew', pady=(10, 0))

    employee_frame_tab = Frame(employee_tab)
    employee_frame_tab.grid(row=4, column=0, columnspan=6, padx=(0, 10), pady=5)

    add_employee_button = Button(
        employee_frame_tab, text="Add Employee", width=15, command=lambda: add_person_button_clicked(employee_tab)
    )

    add_employee_button.grid(row=4, column=0, padx=(0, 10), pady=5)

    column_employee_list = ["employee_code", "first_name", "last_name", "national_code", "username", "is_admin",
                            "employee_status"]
    employee_list_button = Button(
        employee_frame_tab, text="List of Employees", width=15, command=lambda: show_list(
            widget=win_admin, table="Employee", column=column_employee_list
        )
    )
    employee_list_button.grid(row=4, column=1, padx=(0, 10), pady=5)

    search_employee_button = Button(
        employee_frame_tab, text="Search", width=15, command=lambda: search_button_clicked(
            widget=employee_tab, window=win_admin
        )
    )
    search_employee_button.grid(row=4, column=2, padx=(0, 10), pady=5)

    logout_button = Button(employee_frame_tab, text="Logout", width=15, command=lambda: logged_out(win_admin, frame))
    logout_button.grid(row=4, column=3, padx=(0, 10), pady=5)
    # </editor-fold>

    # ================= Admin Tab
    # <editor-fold desc="Admin Tab">
    employee_code_label = Label(admin_tab, text="Employee Code")
    employee_code_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="w")
    username_label = Label(admin_tab, text="username")
    username_label.grid(row=0, column=2, padx=(10, 5), pady=(10, 5), sticky="w")
    status_label = Label(admin_tab, text="Is Active")
    status_label.grid(row=0, column=4, padx=(10, 5), pady=(10, 5), sticky="w")
    first_name_label = Label(admin_tab, text="First Name")
    first_name_label.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
    last_name_label = Label(admin_tab, text="Last Name")
    last_name_label.grid(row=1, column=2, padx=(10, 5), pady=5, sticky="w")
    is_admin_label = Label(admin_tab, text="Is Admin")
    is_admin_label.grid(row=1, column=4, padx=(10, 5), pady=5, sticky="w")

    username_entry = Entry(admin_tab, width=20, state='disabled', disabledbackground="#FAFAFA", relief="solid")
    username_entry.grid(row=0, column=3, padx=(0, 10), pady=(10, 5), sticky="w")
    first_name_entry = Entry(admin_tab, width=15, state='disabled', disabledbackground="#FAFAFA", relief="solid")
    first_name_entry.grid(row=1, column=1, pady=5, sticky="w")
    first_name_entry.focus()
    last_name_entry = Entry(admin_tab, width=20, state='disabled', disabledbackground="#FAFAFA", relief="solid")
    last_name_entry.grid(row=1, column=3, pady=5, sticky="w")

    def employee_code_combobox_select(event):
        employee_code = employee_code_combobox.get()
        clear_entry(admin_tab)
        fill_admin_info(employee_code, admin_tab)

    employee_code_var = StringVar()
    employee_code_combobox = ttk.Combobox(admin_tab, width=10, textvariable=employee_code_var, state='readonly')
    employee_code_combobox["values"] = employee_list()
    employee_code_combobox.grid(row=0, column=1, pady=(10, 5), sticky="w")
    employee_code_combobox.bind('<<ComboboxSelected>>', employee_code_combobox_select)

    admin_status_var = StringVar()
    admin_status_combobox = ttk.Combobox(admin_tab, width=5, textvariable=admin_status_var, state='readonly')
    admin_status_combobox["values"] = ("", "Yes", "No")
    admin_status_combobox.grid(row=0, column=5, pady=(10, 5), sticky="w")

    is_admin_var = StringVar()
    is_admin_combobox = ttk.Combobox(admin_tab, width=5, textvariable=is_admin_var, state='readonly')
    is_admin_combobox["values"] = ("", "Yes", "No")
    is_admin_combobox.grid(row=1, column=5, pady=(10, 5), sticky="w")

    separator = ttk.Separator(admin_tab, orient='horizontal')
    separator.grid(row=3, columnspan=6, sticky='ew', pady=(10, 0))

    admin_frame_tab = Frame(admin_tab)
    admin_frame_tab.grid(row=4, column=0, columnspan=6, padx=(0, 10), pady=5)

    submit_admin_button = Button(
        admin_frame_tab, text="Submit Changes", width=15, command=lambda: submit_admin_button_clicked(admin_tab)
    )

    submit_admin_button.grid(row=4, column=0, padx=(0, 10), pady=5)

    column_admin_list = ["employee_code", "first_name", "last_name", "username", "employee_status"]
    condition_admin = f"is_admin='{1}'"
    admin_list_button = Button(
        admin_frame_tab, text="List of Admins", width=15, command=lambda: show_list(
            widget=win_admin, table="Employee", column=column_admin_list, condition=condition_admin
        )
    )
    admin_list_button.grid(row=4, column=1, padx=(0, 10), pady=5)
    reset_password_button = Button(
        admin_frame_tab, text="Reset Password", width=15, command=lambda: reset_password_button_clicked(admin_tab)
    )
    reset_password_button.grid(row=4, column=2, padx=(0, 10), pady=5)

    logout_button = Button(admin_frame_tab, text="Logout", width=15, command=lambda: logged_out(win_admin, frame))
    logout_button.grid(row=4, column=3, padx=(0, 10), pady=5)
    window_geometry(win_admin)

    win_admin.mainloop()  # </editor-fold>


# ================= User Window
def user_logged_in():
    # <editor-fold desc="User Window">
    win_user = Tk()
    win_user.title("User Panel")
    win_user.call("wm", "attributes", ".", "-topmost", "1")
    win_user.protocol("WM_DELETE_WINDOW", lambda: None)
    win_user.update()
    win_user.deiconify()

    user_frame = Frame(win_user, borderwidth=3, pady=5, relief="groove", name="customer_user_frame")
    # flat, groove, raised, ridge, solid, or sunken
    user_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="w")

    # <editor-fold desc="User Panel">

    first_name_label = Label(user_frame, text="First Name", font=("Tahoma", 11))
    first_name_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="w")
    last_name_label = Label(user_frame, text="Last Name", font=("Tahoma", 11))
    last_name_label.grid(row=0, column=2, padx=(10, 5), pady=(10, 5), sticky="w")
    gender_label = Label(user_frame, text="Gender", font=("Tahoma", 11))
    gender_label.grid(row=0, column=4, padx=(10, 5), pady=(10, 5), sticky="w")
    national_code_label = Label(user_frame, text="National Code", font=("Tahoma", 11))
    national_code_label.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
    status_label = Label(
        user_frame, text="Are the customer’s file documents complete?", font=("Tahoma", 11, "bold"), fg="red"
    )
    status_label.grid(row=1, column=2, columnspan=3, padx=(10, 5), pady=5, sticky="w")

    text_validator = (user_frame.register(only_alpha_input), '%P')
    number_validator = (user_frame.register(only_numeric_input), '%P')
    first_name_entry = Entry(user_frame, width=15, font=("Tahoma", 12), validate="key", validatecommand=text_validator)
    first_name_entry.grid(row=0, column=1, pady=(10, 5), sticky="w")
    first_name_entry.focus()
    last_name_entry = Entry(user_frame, width=20, font=("Tahoma", 12), validate="key", validatecommand=text_validator)
    last_name_entry.grid(row=0, column=3, pady=(10, 5), sticky="w")
    national_code_entry = Entry(
        user_frame, width=15, font=("Tahoma", 12), validate="key", validatecommand=number_validator
    )
    national_code_entry.grid(row=1, column=1, pady=5, sticky="w")

    gender_var = StringVar()
    gender_combobox = ttk.Combobox(user_frame, width=10, font=("Tahoma", 12), textvariable=gender_var, state='readonly')
    gender_combobox["values"] = ("", "Male", "Female")
    gender_combobox.grid(row=0, column=5, padx=(0, 10), pady=(10, 5), sticky="w")

    status_var = StringVar()
    status_combobox = ttk.Combobox(user_frame, width=10, font=("Tahoma", 12), textvariable=status_var, state='readonly')
    status_combobox["values"] = ("", "Yes", "No")
    status_combobox.grid(row=1, column=5, pady=5, sticky="w")

    separator = ttk.Separator(user_frame, orient='horizontal')
    separator.grid(row=3, columnspan=6, padx=10, pady=(10, 0), sticky='ew')

    user_frame_tab = Frame(user_frame)
    user_frame_tab.grid(row=4, column=0, columnspan=6, padx=(5, 5), pady=5)

    add_customer_button = Button(
        user_frame_tab, text="Add Customer", font=("Tahoma", 11), width=15,
        command=lambda: add_person_button_clicked(user_frame)
    )
    add_customer_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    column_customer_list = ["first_name", "last_name", "national_code", "account_number", "customer_status"]
    customer_list_button = Button(
        user_frame_tab, text="List of Customers", font=("Tahoma", 11), width=15, command=lambda: show_list(
            widget=win_user, table="Customer", column=column_customer_list
        )
    )
    customer_list_button.grid(row=0, column=1, padx=10, pady=5)

    search_customer_button = Button(
        user_frame_tab, text="Search", font=("Tahoma", 11), width=15, command=lambda: search_button_clicked(
            widget=user_frame, window=win_user
        )
    )
    search_customer_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")

    banking_operation = Button(
        win_user, text="Customer Banking Operations", width=48, font=("tahoma", 14), relief="raised", borderwidth=3,
        border=5, command=lambda: banking_operation_clicked(win_user)
    )  # relife: "raised", "sunken", "flat", "ridge", "solid", "groove"]'
    banking_operation.grid(row=1, column=0, columnspan=5, pady=(5, 5))

    logout_button = Button(
        win_user, text="Logout", font=("Tahoma", 11), width=10, command=lambda: logged_out(win_user, frame)
    )
    logout_button.grid(row=2, column=0, padx=(0, 10), pady=5, sticky="e")

    window_geometry(win_user)

    win_user.mainloop()  # </editor-fold>


def banking_operation_clicked(widget):
    widget.attributes('-disabled', 1)
    widget.wm_state('iconic')
    win_operation = Tk()
    win_operation.title("Customer Banking Operation Panel")
    win_operation.call("wm", "attributes", ".", "-topmost", "1")
    win_operation.protocol("WM_DELETE_WINDOW", lambda: None)

    operation_frame = Frame(win_operation, borderwidth=3, pady=5, relief="groove", name="customer_operation_frame")
    # flat, groove, raised, ridge, solid, or sunken
    operation_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="w")
    operation_frame_button = Frame(operation_frame)
    operation_frame_button.grid(row=4, column=0, padx=(5, 5), pady=5)

    # <editor-fold desc="Operation Panel">
    account_number_label = Label(operation_frame, text="Account Number", font=("Tahoma", 11))
    account_number_label.grid(row=0, column=0, padx=5, pady=(5, 10), sticky="w")
    national_code_label = Label(operation_frame, text="National Code", font=("Tahoma", 11))
    national_code_label.grid(row=1, column=0, padx=5, pady=(5, 10), sticky="w")
    first_name_label = Label(operation_frame, text="First Name", font=("Tahoma", 11))
    first_name_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")
    last_name_label = Label(operation_frame, text="Last Name", font=("Tahoma", 11))
    last_name_label.grid(row=1, column=4, pady=5, sticky="w")

    total_credit_label = Label(operation_frame, text="Total Credit", font=("Tahoma", 11))
    total_credit_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    total_debit_label = Label(operation_frame, text="Total Debit", font=("Tahoma", 11))
    total_debit_label.grid(row=3, column=2, padx=5, pady=5, sticky="w")

    balance_label = Label(operation_frame, text="Balance", font=("Tahoma", 11))
    balance_label.grid(row=3, column=4, pady=5, sticky="w")

    operation_label = Label(operation_frame, text="Operation", font=("Tahoma", 11))
    operation_label.grid(row=5, column=2, padx=5, pady=5, sticky="w")

    amount_label = Label(operation_frame, text="Amount (Rials)", font=("Tahoma", 11))
    amount_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

    number_validator = (operation_frame.register(only_numeric_input), '%P')
    account_number_entry = Entry(
        operation_frame, width=10, font=("Tahoma", 12), validate="key", validatecommand=number_validator
    )
    account_number_entry.grid(row=0, column=1, pady=5, sticky="w")
    account_number_entry.focus_force()

    national_code_entry = Entry(
        operation_frame, width=10, font=("Tahoma", 12), state='disabled', disabledbackground="#FAFAFA", relief="solid"
    )
    national_code_entry.grid(row=1, column=1, pady=5, sticky="w")

    first_name_entry = Entry(
        operation_frame, width=10, font=("Tahoma", 12), state='disabled', disabledbackground="#FAFAFA", relief="solid"
    )
    first_name_entry.grid(row=1, column=3, pady=5, sticky="w")
    last_name_entry = Entry(
        operation_frame, width=15, font=("Tahoma", 12), state='disabled', disabledbackground="#FAFAFA", relief="solid"
    )
    last_name_entry.grid(row=1, column=5, padx=5, pady=5, sticky="w")

    total_credit_entry = Entry(
        operation_frame, width=10, font=("Tahoma", 12), state='disabled', disabledbackground="#FAFAFA", relief="solid"
    )
    total_credit_entry.grid(row=3, column=1, pady=5, sticky="w")
    total_debit_entry = Entry(
        operation_frame, width=10, font=("Tahoma", 12), state='disabled', disabledbackground="#FAFAFA", relief="solid"
    )
    total_debit_entry.grid(row=3, column=3, pady=5, sticky="w")

    balance_entry = Entry(
        operation_frame, width=15, font=("Tahoma", 12), state='disabled', disabledbackground="#FAFAFA", relief="solid"
    )
    balance_entry.grid(row=3, column=5, padx=5, pady=5, sticky="w")

    amount_entry = Entry(
        operation_frame, width=12, font=("Arial", 12), validate="key", validatecommand=number_validator
    )
    amount_entry.grid(row=5, column=1, pady=5, sticky="w")

    operation_var = StringVar()
    operation_combobox = ttk.Combobox(
        operation_frame, width=10, font=("Tahoma", 12), textvariable=operation_var, state='readonly'
    )
    operation_combobox["values"] = ("", "Deposit", "Withdrawal")
    operation_combobox.grid(row=5, column=3, padx=(0, 10), pady=5, sticky="w")

    separator = ttk.Separator(operation_frame, orient='horizontal')
    separator.grid(row=4, columnspan=6, padx=10, pady=(10, 0), sticky='ew')

    find_customer_button = Button(
        operation_frame, text="Find", font=("Tahoma", 11), width=14, command=lambda: find_customer_button_clicked(
            operation_frame
        )
    )
    find_customer_button.grid(row=4, column=5, padx=(0, 10), pady=5)
    record_button = Button(
        operation_frame, text="Record", font=("Tahoma", 12, "bold"), relief="solid",
        command=lambda: record_button_clicked(operation_frame, employee_id)
    )
    record_button.grid(row=5, column=4, padx=1, pady=10)

    finish_button = Button(
        win_operation, text="Finish", font=("Tahoma", 11), width=14,
        command=lambda: finish_button_clicked(win_operation, widget)
    )
    finish_button.grid(row=1, column=0, padx=20, pady=10, sticky='e')

    window_geometry(win_operation)

    win_operation.mainloop()

    # </editor-fold>


def logged_out(window, frame):
    window.destroy()
    clear_frame(frame)
    login_page()


login_page()
