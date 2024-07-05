from customtkinter import *
from tkinter import ttk
from PIL import Image
from core import *


# Function to clear the table
def clear_table():
    for item in bank.tree.get_children():
        bank.tree.delete(item)


# Function to create the user table
def make_user_table():
    for item in bank.show_data:
        if item[6] == 1 and item[7] == 1:
            bank.tree.insert(parent="", index="end", text="",
                             values=(item[1], item[3], item[4], item[5], "active", "admin"))
        elif item[6] == 1 and item[7] == 2:
            bank.tree.insert(parent="", index="end", text="",
                             values=(item[1], item[3], item[4], item[5], "active", "client"))
        elif item[6] == 2 and item[7] == 1:
            bank.tree.insert(parent="", index="end", text="",
                             values=(item[1], item[3], item[4], item[5], "inactive", "admin"), tags=('colored',))
        else:
            bank.tree.insert(parent="", index="end", text="",
                             values=(item[1], item[3], item[4], item[5], "inactive", "client"), tags=('colored',))


# Function to create the user table in the right frame
def user_table(right_frame):
    bank.tree = ttk.Treeview(master=right_frame)
    bank.tree.grid(row=0, column=0, sticky="nsew")
    tree_scrollbar = CTkScrollbar(right_frame, orientation="vertical", command=bank.tree.yview)
    tree_scrollbar.grid(row=0, column=1, sticky='ns')
    bank.tree.configure(yscrollcommand=tree_scrollbar.set)

    # Function to sort the columns in the treeview
    def treeview_sort_column(tree, column, reverse):
        sort_object = [(tree.set(k, column), k) for k in tree.get_children('')]
        sort_object.sort(reverse=reverse)
        for index, (val, k) in enumerate(sort_object):
            tree.move(k, '', index)
        tree.heading(column, command=lambda _col=column: treeview_sort_column(tree, _col, not reverse))

    columns = ("Employee ID", "First Name", "Last Name", "National ID", "Status", "Type")
    bank.tree["columns"] = columns

    bank.tree.column("#0", width=0, stretch=False)
    bank.tree.heading("#0", text="", anchor="center")

    for col in columns:
        bank.tree.column(col, anchor="center", width=200, stretch=False)
        bank.tree.heading(col, text=col, anchor="center",
                          command=lambda _col=col: treeview_sort_column(bank.tree, _col, False))

    style = ttk.Style(master=right_frame)

    style.configure("Treeview", font=("Roboto", 20), rowheight=40)

    style.configure("Treeview.Heading", font=("Roboto", 20, "bold"), rowheight=40)

    bank.tree.tag_configure('colored', background='lightgrey')

    make_user_table()

    # Function to select a row in the treeview
    def select_row(_):
        selected_item = bank.tree.focus()
        item_value = bank.tree.item(selected_item, 'values')
        get_row_value(item_value)

    bank.tree.bind("<<TreeviewSelect>>", select_row)

    # Function to handle click events in the treeview
    def handle_click(event):
        if bank.tree.identify_region(event.x, event.y) == "separator":
            return "break"

    bank.tree.bind("<Button-1>", handle_click)


# Function to create the admin frame
def admin_frame(root, windows_frame, name):
    windows_frame.destroy()
    root.title("Admin Panel")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, minsize=350)
    root.grid_columnconfigure(1, weight=1)

    left_frame = CTkFrame(master=root)
    left_frame.grid(row=0, column=0, padx=(20, 12), pady=20, sticky="nsew")
    left_frame.grid_columnconfigure(0, weight=1)

    right_frame = CTkFrame(master=root)
    right_frame.grid(row=0, column=1, padx=(12, 20), pady=20, sticky="nsew")
    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    user_table(right_frame)

    user_label = CTkLabel(master=left_frame, text=f"Welcome\n{name}", font=("Roboto", 20))
    user_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nsew")

    avatar = CTkImage(Image.open(bank.avatar_path), size=(100, 100))
    avatar_label = CTkLabel(master=left_frame, image=avatar, text="", corner_radius=200)
    avatar_label.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="nsew")

    # Function to create a second window for adding or editing users
    def create_second_windows(first_name="", last_name="", national_id="", username="", status="", user_type=""):
        second_windows = CTkToplevel(root)
        second_windows.grab_set()
        if first_name:
            second_windows.title("Edit user")
        else:
            second_windows.title("Add new user")
        second_windows.resizable(False, False)
        first_name_label = CTkLabel(master=second_windows, text="First Name:")
        first_name_label.grid(row=0, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
        name_id_cmd = (second_windows.register(only_letters), '%S')
        first_name_entry = CTkEntry(master=second_windows, width=200, validate='key', validatecommand=name_id_cmd)
        first_name_entry.grid(row=0, column=1, pady=(10, 0), padx=10, sticky="e")
        first_name_entry.insert(0, first_name)
        last_name_label = CTkLabel(master=second_windows, text="Last Name:")
        last_name_label.grid(row=1, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
        last_name_entry = CTkEntry(master=second_windows, width=200, validate='key', validatecommand=name_id_cmd)
        last_name_entry.grid(row=1, column=1, pady=(10, 0), padx=10, sticky="e")
        last_name_entry.insert(0, last_name)
        national_id_label = CTkLabel(master=second_windows, text="National ID:")
        national_id_label.grid(row=2, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
        number_id_cmd = (second_windows.register(only_numbers), '%S')
        national_id_entry = CTkEntry(master=second_windows, width=200, validate='key', validatecommand=number_id_cmd)
        national_id_entry.grid(row=2, column=1, pady=(10, 0), padx=10, sticky="e")
        national_id_entry.insert(0, national_id)
        if not first_name:
            password_label = CTkLabel(master=second_windows, text="Password:")
            password_label.grid(row=3, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
            password_entry = CTkEntry(master=second_windows, width=200)
            password_entry.grid(row=3, column=1, pady=(10, 0), padx=10, sticky="e")
        radio_var_status = IntVar(value=0)
        radio_var_type = IntVar(value=0)

        # Function to get the status of the radio button
        def radiobutton_event_status():
            return radio_var_status.get()

        # Function to get the type of the radio button
        def radiobutton_event_type():
            return radio_var_type.get()

        radiobutton_active = CTkRadioButton(master=second_windows, text="Active", variable=radio_var_status,
                                            value=1, command=radiobutton_event_status)
        radiobutton_active.grid(row=4, column=0, pady=(10, 0), padx=(10, 0), sticky="e")
        radiobutton_inactive = CTkRadioButton(master=second_windows, text="Inactive", variable=radio_var_status,
                                              value=2, command=radiobutton_event_status)
        radiobutton_inactive.grid(row=4, column=1, pady=(10, 0), padx=10, sticky="w")
        radiobutton_admin = CTkRadioButton(master=second_windows, text="Admin", variable=radio_var_type, value=1,
                                           command=radiobutton_event_type)
        radiobutton_admin.grid(row=5, column=0, pady=(10, 0), padx=(10, 0), sticky="e")
        radiobutton_client = CTkRadioButton(master=second_windows, text="Client", variable=radio_var_type, value=2,
                                            command=radiobutton_event_type)
        radiobutton_client.grid(row=5, column=1, pady=(10, 0), padx=10, sticky="w")

        if status == "active":
            radio_var_status.set(1)
        elif status == "inactive":
            radio_var_status.set(2)

        if user_type == "admin":
            radio_var_type.set(1)
        elif user_type == "client":
            radio_var_type.set(2)

        # Function to close the second window
        def close_second_window():
            second_windows.destroy()
            root.grab_release()

        second_windows.protocol("WM_DELETE_WINDOW", close_second_window)

        # Function to handle the confirm button click
        def clicked_confirm_button():
            firstname_variable = first_name_entry.get()
            lastname_variable = last_name_entry.get()
            national_id_variable = national_id_entry.get()
            status_variable = radiobutton_event_status()
            type_variable = radiobutton_event_type()

            if first_name:
                try:
                    data_validation(firstname_variable, lastname_variable, national_id_variable,
                                    username, status_variable, type_variable)
                    update_action(firstname_variable, lastname_variable, national_id_variable,
                                  username, status_variable, type_variable)
                    second_windows.destroy()
                    CTkMessagebox(title="Info", message="Changes applied successfully.")
                except ValueError as error:
                    CTkMessagebox(title="Warning", message=error.args[0], icon="warning", option_1="OK")

            else:
                try:
                    password_variable = password_entry.get()
                    data_validation(firstname_variable, lastname_variable, national_id_variable,
                                    username, status_variable, type_variable)
                    reset_password_validation(password_variable, password_variable)
                    new_user = add_action(firstname_variable, lastname_variable, national_id_variable,
                                          password_variable, status_variable, type_variable)
                    second_windows.destroy()
                    CTkMessagebox(
                        title="Info", message=f"The new user has been added successfully.\nUsername is: {new_user}")
                except ValueError as error:
                    CTkMessagebox(title="Warning", message=error.args[0], icon="warning", option_1="OK")
            clear_table()
            make_user_table()

        save_button = CTkButton(master=second_windows, text="Confirm", width=100, command=clicked_confirm_button)
        save_button.grid(row=6, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="we")

        close_button = CTkButton(master=second_windows, text="Close", width=100, command=close_second_window)
        close_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="we")

    add_user_button = CTkButton(master=left_frame, text="Add User", command=create_second_windows)
    add_user_button.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="nsew")

    # Function to edit a user
    def edit_user():
        if bank.selected_value:
            create_second_windows(bank.selected_value[1], bank.selected_value[2], bank.selected_value[3],
                                  bank.selected_value[0], bank.selected_value[4], bank.selected_value[5])
        else:
            CTkMessagebox(title="Warning", message="No item is selected!", icon="warning", option_1="OK")

    edit_user_button = CTkButton(master=left_frame, text="Edit User", command=edit_user)
    edit_user_button.grid(row=3, column=0, padx=20, pady=(20, 0), sticky="nsew")

    # Function to remove a user
    def remove_user():
        if remove_action():
            clear_table()
            make_user_table()
            CTkMessagebox(title="Info", message="The selected user has been successfully deleted.")

    remove_user_button = CTkButton(master=left_frame, text="Remove User", command=remove_user)
    remove_user_button.grid(row=4, column=0, padx=20, pady=(20, 0), sticky="nsew")

    # Function to create a window for resetting the password
    def reset_password_windows(username):
        reset_windows = CTkToplevel(root)
        reset_windows.grab_set()
        reset_windows.title("Reset Password")
        reset_windows.resizable(False, False)

        # Function to close the reset password window
        def close_reset_windows():
            reset_windows.destroy()
            root.grab_release()

        reset_windows.protocol("WM_DELETE_WINDOW", close_reset_windows)
        password_label = CTkLabel(master=reset_windows, text="New password:")
        password_label.grid(row=0, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
        password_entry = CTkEntry(master=reset_windows, width=200)
        password_entry.grid(row=0, column=1, pady=(10, 0), padx=10, sticky="e")
        re_enter_password_label = CTkLabel(master=reset_windows, text="Re-enter password:")
        re_enter_password_label.grid(row=1, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
        re_enter_password_entry = CTkEntry(master=reset_windows, width=200)
        re_enter_password_entry.grid(row=1, column=1, pady=(10, 0), padx=10, sticky="e")

        # Function to handle the confirm button click
        def clicked_confirm_button():
            try:
                password_variable = password_entry.get()
                re_enter_password_variable = re_enter_password_entry.get()
                reset_password_validation(password_variable, re_enter_password_variable)
                update_password(username, password_variable)
                reset_windows.destroy()
                CTkMessagebox(title="Info", message="The password was changed.")
            except ValueError as error:
                CTkMessagebox(title="Warning", message=error.args[0], icon="warning", option_1="OK")

        save_button = CTkButton(master=reset_windows, text="Confirm", width=100, command=clicked_confirm_button)
        save_button.grid(row=2, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="we")
        close_button = CTkButton(master=reset_windows, text="Close", width=100, command=close_reset_windows)
        close_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="we")

    # Function to reset the password
    def reset_password():
        if bank.selected_value:
            reset_password_windows(bank.selected_value[0])
        else:
            CTkMessagebox(title="Warning", message="No item is selected!", icon="warning", option_1="OK")

    reset_password_button = CTkButton(master=left_frame, text="Reset Password", command=reset_password)
    reset_password_button.grid(row=5, column=0, padx=20, pady=(20, 0), sticky="nsew")

    search_entry = CTkEntry(master=left_frame, placeholder_text="Employee or National ID")
    search_entry.grid(row=6, column=0, padx=20, pady=(20, 0), sticky="nsew")

    # Function to search for a user
    def search():
        search_action(search_entry.get())
        clear_table()
        make_user_table()

    search_button = CTkButton(master=left_frame, text="Search", command=search)
    search_button.grid(row=7, column=0, padx=20, pady=(20, 0), sticky="nsew")

    # Function to log out
    def logout_clicked():
        bank.selected_value = ()
        left_frame.destroy()
        right_frame.destroy()
        bank.root_login(root)

    logout_button = CTkButton(master=left_frame, text="Logout", command=logout_clicked)
    logout_button.grid(row=8, column=0, padx=20, pady=(20, 0), sticky="nsew")


########################################################################################################################

# Function to create the customer table
def make_customer_table():
    for item in bank.show_data:
        if item[6] == 1:
            bank.tree.insert(parent="", index="end", text="", values=(
                item[3], item[1], item[2], item[4], item[5], "active"))
        else:
            bank.tree.insert(parent="", index="end", text="", values=(
                item[3], item[1], item[2], item[4], item[5], "inactive"), tags=('colored',))


# Function to create the customer table in the right frame
def customer_table(right_frame):
    bank.tree = ttk.Treeview(master=right_frame)
    bank.tree.grid(row=0, column=0, sticky="nsew")
    tree_scrollbar = CTkScrollbar(right_frame, orientation="vertical", command=bank.tree.yview)
    tree_scrollbar.grid(row=0, column=1, sticky='ns')
    bank.tree.configure(yscrollcommand=tree_scrollbar.set)

    # Function to sort the columns in the treeview
    def treeview_sort_column(tree, column, reverse):
        sort_object = [(tree.set(k, column), k) for k in tree.get_children('')]
        sort_object.sort(reverse=reverse)
        for index, (val, k) in enumerate(sort_object):
            tree.move(k, '', index)
        tree.heading(column, command=lambda _col=column: treeview_sort_column(tree, _col, not reverse))

    columns = ("National ID", "First Name", "Last Name", "Account", "Balance", "Status")
    bank.tree["columns"] = columns

    bank.tree.column("#0", width=0, stretch=False)
    bank.tree.heading("#0", text="", anchor="center")

    for col in columns:
        bank.tree.column(col, anchor="center", width=200, stretch=False)
        bank.tree.heading(col, text=col, anchor="center",
                          command=lambda _col=col: treeview_sort_column(bank.tree, _col, False))

    style = ttk.Style(master=right_frame)

    style.configure("Treeview", font=("Roboto", 20), rowheight=40)

    style.configure("Treeview.Heading", font=("Roboto", 20, "bold"), rowheight=40)

    bank.tree.tag_configure('colored', background='lightgrey')

    make_customer_table()

    # Function to select a row in the treeview
    def select_row(_):
        selected_item = bank.tree.focus()
        item_value = bank.tree.item(selected_item, 'values')
        get_row_value(item_value)

    bank.tree.bind("<<TreeviewSelect>>", select_row)

    # Function to handle click events in the treeview
    def handle_click(event):
        if bank.tree.identify_region(event.x, event.y) == "separator":
            return "break"

    bank.tree.bind("<Button-1>", handle_click)


# Function to create the customer frame
def customer_frame(root, windows_frame, name):
    windows_frame.destroy()
    root.title("Client Panel")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, minsize=350)
    root.grid_columnconfigure(1, weight=1)

    left_frame = CTkFrame(master=root)
    left_frame.grid(row=0, column=0, padx=(20, 12), pady=20, sticky="nsew")
    left_frame.grid_columnconfigure(0, weight=1)

    right_frame = CTkFrame(master=root)
    right_frame.grid(row=0, column=1, padx=(12, 20), pady=20, sticky="nsew")
    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    customer_table(right_frame)

    user_label = CTkLabel(master=left_frame, text=f"Welcome\n{name}", font=("Roboto", 20))
    user_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nsew")

    avatar = CTkImage(Image.open(bank.avatar_path), size=(100, 100))
    avatar_label = CTkLabel(master=left_frame, image=avatar, text="", corner_radius=200)
    avatar_label.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="nsew")

    # Function to create a second window for adding or editing customers
    def create_second_windows(first_name="", last_name="", national_id="", account_number="", balance="", status=""):
        second_windows = CTkToplevel(root)
        second_windows.grab_set()
        if first_name:
            second_windows.title("Edit customer")
        else:
            second_windows.title("Add new customer")
        second_windows.resizable(False, False)
        first_name_label = CTkLabel(master=second_windows, text="First Name:")
        first_name_label.grid(row=0, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
        name_id_cmd = (second_windows.register(only_letters), '%S')
        first_name_entry = CTkEntry(master=second_windows, width=200, validate='key', validatecommand=name_id_cmd)
        first_name_entry.grid(row=0, column=1, pady=(10, 0), padx=10, sticky="e")
        first_name_entry.insert(0, first_name)
        last_name_label = CTkLabel(master=second_windows, text="Last Name:")
        last_name_label.grid(row=1, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
        last_name_entry = CTkEntry(master=second_windows, width=200, validate='key', validatecommand=name_id_cmd)
        last_name_entry.grid(row=1, column=1, pady=(10, 0), padx=10, sticky="e")
        last_name_entry.insert(0, last_name)
        national_id_label = CTkLabel(master=second_windows, text="National ID:")
        national_id_label.grid(row=2, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
        number_id_cmd = (second_windows.register(only_numbers), '%S')
        national_id_entry = CTkEntry(master=second_windows, width=200, validate='key', validatecommand=number_id_cmd)
        national_id_entry.grid(row=2, column=1, pady=(10, 0), padx=10, sticky="e")
        national_id_entry.insert(0, national_id)
        if not first_name:
            funds_label = CTkLabel(master=second_windows, text="Funds:")
            funds_label.grid(row=3, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
            funds_entry = CTkEntry(master=second_windows, width=200, validate='key', validatecommand=number_id_cmd)
            funds_entry.grid(row=3, column=1, pady=(10, 0), padx=10, sticky="e")
        radio_var = IntVar(value=0)

        # Function to get the status of the radio button
        def radiobutton_event():
            return radio_var.get()

        radiobutton_active = CTkRadioButton(master=second_windows, text="Active", variable=radio_var, value=1,
                                            command=radiobutton_event)
        radiobutton_active.grid(row=4, column=0, pady=(10, 0), padx=(10, 0), sticky="e")
        radiobutton_inactive = CTkRadioButton(master=second_windows, text="Inactive", variable=radio_var, value=2,
                                              command=radiobutton_event)
        radiobutton_inactive.grid(row=4, column=1, pady=(10, 0), padx=10, sticky="w")

        if status == "active":
            radio_var.set(1)
        elif status == "inactive":
            radio_var.set(2)

        # Function to close the second window
        def close_second_window():
            second_windows.destroy()
            root.grab_release()

        second_windows.protocol("WM_DELETE_WINDOW", close_second_window)

        # Function to handle the confirm button click
        def clicked_confirm_button():
            firstname_variable = first_name_entry.get()
            lastname_variable = last_name_entry.get()
            national_id_variable = national_id_entry.get()
            status_variable = radiobutton_event()

            if first_name:
                try:
                    customer_data_validation(firstname_variable, lastname_variable, national_id_variable,
                                             account_number, balance, status_variable)
                    update_customer_action(firstname_variable, lastname_variable, national_id_variable,
                                           account_number, status_variable)
                    second_windows.destroy()
                    CTkMessagebox(title="Info", message="Changes applied successfully.")
                except ValueError as error:
                    CTkMessagebox(title="Warning", message=error.args[0], icon="warning", option_1="OK")

            else:
                try:
                    funds_variable = funds_entry.get()
                    customer_data_validation(firstname_variable, lastname_variable, national_id_variable,
                                             account_number, funds_variable, status_variable)
                    account = add_customer_action(
                        firstname_variable, lastname_variable, national_id_variable,
                        funds_variable, status_variable)
                    second_windows.destroy()
                    CTkMessagebox(
                     title="Info", message=f"The customer has been added successfully.\nAccount Number is: {account}")
                except ValueError as error:
                    CTkMessagebox(title="Warning", message=error.args[0], icon="warning", option_1="OK")
            clear_table()
            make_customer_table()

        save_button = CTkButton(master=second_windows, text="Confirm", width=100, command=clicked_confirm_button)
        save_button.grid(row=5, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="we")

        close_button = CTkButton(master=second_windows, text="Close", width=100, command=close_second_window)
        close_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, sticky="we")

    add_customer_button = CTkButton(master=left_frame, text="Add Customer", command=create_second_windows)
    add_customer_button.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="nsew")

    # Function to edit a customer
    def edit_customer():
        if bank.selected_value:
            create_second_windows(bank.selected_value[1], bank.selected_value[2], bank.selected_value[0],
                                  bank.selected_value[3], bank.selected_value[4], bank.selected_value[5])
        else:
            CTkMessagebox(title="Warning", message="No item is selected!", icon="warning", option_1="OK")

    edit_customer_button = CTkButton(master=left_frame, text="Edit Customer", command=edit_customer)
    edit_customer_button.grid(row=3, column=0, padx=20, pady=(20, 0), sticky="nsew")

    # Function to remove a customer
    def remove_customer():
        if remove_customer_action():
            clear_table()
            make_customer_table()
            CTkMessagebox(title="Info", message="The selected customer has been successfully deleted.")

    remove_customer_button = CTkButton(master=left_frame, text="Remove Customer", command=remove_customer)
    remove_customer_button.grid(row=4, column=0, padx=20, pady=(20, 0), sticky="nsew")

    # Function to create a page for banking operations (deposit or withdrawal)
    def banking_operation_page(account_number, balance):
        banking_windows = CTkToplevel(root)
        banking_windows.grab_set()
        banking_windows.title("Banking Operation")
        banking_windows.resizable(False, False)
        account_balance_label = CTkLabel(master=banking_windows, text="Balance:")
        account_balance_label.grid(row=0, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
        balance_label = CTkLabel(master=banking_windows, text=f"{balance} $")
        balance_label.grid(row=0, column=1, pady=(10, 0), padx=15, sticky="w")
        amount_label = CTkLabel(master=banking_windows, text="Amount:")
        amount_label.grid(row=1, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
        number_id_cmd = (banking_windows.register(only_numbers), '%S')
        amount_entry = CTkEntry(master=banking_windows, width=110, validate='key', validatecommand=number_id_cmd)
        amount_entry.grid(row=1, column=1, pady=(10, 0), padx=10, sticky="e")
        radio_var = IntVar(value=0)

        # Function to get the selected operation (deposit or withdrawal)
        def radiobutton_event():
            return radio_var.get()

        radiobutton_active = CTkRadioButton(master=banking_windows, text="Deposit", variable=radio_var, value=1,
                                            command=radiobutton_event)
        radiobutton_active.grid(row=2, column=0, pady=(10, 0), padx=(10, 0), sticky="e")
        radiobutton_inactive = CTkRadioButton(master=banking_windows, text="Withdrawal", variable=radio_var, value=2,
                                              command=radiobutton_event)
        radiobutton_inactive.grid(row=2, column=1, pady=(10, 0), padx=10, sticky="w")

        # Function to close the banking operation window
        def close_banking_window():
            banking_windows.destroy()
            root.grab_release()

        banking_windows.protocol("WM_DELETE_WINDOW", close_banking_window)

        # Function to handle the confirm button click
        def clicked_confirm_button():
            money = amount_entry.get()
            type_variable = radiobutton_event()
            try:
                check_entries(money, type_variable)
                if type_variable == 2:
                    bank_operation_validation(float(money), float(balance))
                update_balance_action(account_number, float(money), float(balance), type_variable)
                banking_windows.destroy()
                CTkMessagebox(title="Info", message="Changes applied successfully.")
            except ValueError as error:
                CTkMessagebox(title="Warning", message=error.args[0], icon="warning", option_1="OK")

            clear_table()
            make_customer_table()

        confirm_button = CTkButton(master=banking_windows, text="Confirm", width=100, command=clicked_confirm_button)
        confirm_button.grid(row=3, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="we")

        close_button = CTkButton(master=banking_windows, text="Close", width=100, command=close_banking_window)
        close_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="we")

    # Function to perform a banking operation (deposit or withdrawal)
    def banking_operation():
        if bank.selected_value:
            if bank.selected_value[5] == "inactive":
                CTkMessagebox(title="Warning", message="This account is inactive!", icon="warning", option_1="OK")
            else:
                banking_operation_page(bank.selected_value[3], bank.selected_value[4])
        else:
            CTkMessagebox(title="Warning", message="No item is selected!", icon="warning", option_1="OK")

    banking_operations_button = CTkButton(master=left_frame, text="Banking Operations", command=banking_operation)
    banking_operations_button.grid(row=5, column=0, padx=20, pady=(20, 0), sticky="nsew")

    search_entry = CTkEntry(master=left_frame, placeholder_text="National ID or Account")
    search_entry.grid(row=6, column=0, padx=20, pady=(20, 0), sticky="nsew")

    # Function to search for a customer
    def search():
        search_customer_action(search_entry.get())
        clear_table()
        make_customer_table()

    search_button = CTkButton(master=left_frame, text="Search", command=search)
    search_button.grid(row=7, column=0, padx=20, pady=(20, 0), sticky="nsew")

    # Function to create a window for changing the password
    def change_password_windows(username):
        change_windows = CTkToplevel(root)
        change_windows.grab_set()
        change_windows.title("Change Password")
        change_windows.resizable(False, False)

        # Function to close the change password window
        def close_reset_windows():
            change_windows.destroy()
            root.grab_release()

        change_windows.protocol("WM_DELETE_WINDOW", close_reset_windows)
        old_password_label = CTkLabel(master=change_windows, text="Old password:")
        old_password_label.grid(row=0, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
        old_password_entry = CTkEntry(master=change_windows, width=200)
        old_password_entry.grid(row=0, column=1, pady=(10, 0), padx=10, sticky="e")
        new_password_label = CTkLabel(master=change_windows, text="New password:")
        new_password_label.grid(row=1, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
        new_password_entry = CTkEntry(master=change_windows, width=200)
        new_password_entry.grid(row=1, column=1, pady=(10, 0), padx=10, sticky="e")
        re_enter_password_label = CTkLabel(master=change_windows, text="Re-enter password:")
        re_enter_password_label.grid(row=2, column=0, pady=(10, 0), padx=(10, 0), sticky="w")
        re_enter_password_entry = CTkEntry(master=change_windows, width=200)
        re_enter_password_entry.grid(row=2, column=1, pady=(10, 0), padx=10, sticky="e")

        # Function to handle the confirm button click
        def clicked_confirm_button():
            fetch_user_data()
            try:
                old_password_variable = old_password_entry.get()
                password_variable = new_password_entry.get()
                re_enter_password_variable = re_enter_password_entry.get()
                old_password_check(old_password_variable)
                reset_password_validation(password_variable, re_enter_password_variable)
                update_password(username, password_variable)
                change_windows.destroy()
                CTkMessagebox(title="Info", message="The password was changed.")
            except ValueError as error:
                CTkMessagebox(title="Warning", message=error.args[0], icon="warning", option_1="OK")
            finally:
                fetch_customer_data()

        save_button = CTkButton(master=change_windows, text="Confirm", width=100, command=clicked_confirm_button)
        save_button.grid(row=3, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="we")
        close_button = CTkButton(master=change_windows, text="Close", width=100, command=close_reset_windows)
        close_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="we")

    # Function to initiate the change password process
    def change_password():
        change_password_windows(bank.logged_in_user)

    change_password_button = CTkButton(master=left_frame, text="Change Password", command=change_password)
    change_password_button.grid(row=8, column=0, padx=20, pady=(20, 0), sticky="nsew")

    # Function to log out the user
    def logout_clicked():
        bank.selected_value = ()
        left_frame.destroy()
        right_frame.destroy()
        bank.root_login(root)

    logout_button = CTkButton(master=left_frame, text="Logout", command=logout_clicked)
    logout_button.grid(row=9, column=0, padx=20, pady=(20, 0), sticky="nsew")


# Function to reload the login page
def reload_login_page(login_page):
    bank.root_login = login_page
