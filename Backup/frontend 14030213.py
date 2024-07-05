from tkinter import Tk, Label, Entry, Button, Frame, StringVar, ttk
from PIL import Image, ImageTk
from backend import *


# ================= Login Page
# TODO: Temporary disabled.
# root = Tk()
# image_path = "background.png"
# image = Image.open(image_path)
# global screen_width, screen_height
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# image = image.resize((screen_width, screen_height))
# photo = ImageTk.PhotoImage(image)
# root.geometry(f"{screen_width}x{screen_height}+0+0")
# root.attributes('-fullscreen', True)
#
# frame = Frame(root, bg='')
# frame.place(x=0, y=0)
# label = Label(frame, image=photo)
# label.pack(fill="both", expand=True)


def login_page():
    label_username = Label(frame, text="Username:", font=("Tahoma", 12), bg="#E2E9F2")
    label_username.place(anchor='center', relx=0.35, rely=0.68)
    label_password = Label(frame, text="Password:", font=("Tahoma", 12), bg="#E2E9F2")
    label_password.place(anchor='center', relx=0.35, rely=0.71)

    entry_username = Entry(frame, width=27, font=("Tahoma", 12), bg="#E2E9F2")
    entry_username.place(anchor='center', relx=0.44, rely=0.68)
    entry_username.focus()

    password = StringVar()
    entry_password = Entry(frame, width=27, textvariable=password, show='*', font=("Tahoma", 12), bg="#E2E9F2")
    entry_password.place(anchor='center', relx=0.44, rely=0.71)

    def login_check():
        login_value = btn_login_clicked(
            entry_username.get(), entry_password.get(), frame
        )
        if login_value == "Admin":
            admin_logged_in()
        else:
            user_logged_in()

    button_login = Button(
        frame, text="Login", width=12, font=("Tahoma", 12), bg="#E2E9F2", command=login_check
    )
    button_login.place(anchor='center', relx=0.406, rely=0.745)

    button_exit = Button(frame, text="Exit", width=12, font=("Tahoma", 12), bg="#E2E9F2", command=root.destroy)
    button_exit.place(anchor='center', relx=0.474, rely=0.745)

    root.mainloop()


# ================= Admin Window
def admin_logged_in():
    # TODO: Temporary screen_width and screen_height.
    screen_width = 1920
    screen_height = 1200
    win_admin = Tk()
    win_admin.title("Administrator Panel")
    win_admin.geometry(f"660x170+{int(screen_width / 2) - 330}+{int(screen_height / 2) - 85}")
    win_admin.resizable(width=False, height=False)

    tab_control = ttk.Notebook(win_admin)
    tab_admin = Frame(tab_control)
    tab_employee = Frame(tab_control)
    tab_control.add(tab_employee, text="Employee ")
    tab_control.add(tab_admin, text="Admin")
    tab_control.grid(row=0, column=0, padx=(15, 15), pady=10)

    # ================= Employee Tab
    label_first_name = Label(tab_employee, text="First Name")
    label_first_name.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="w")
    label_last_name = Label(tab_employee, text="Last Name")
    label_last_name.grid(row=0, column=2, padx=(10, 5), pady=(10, 5), sticky="w")
    label_gender = Label(tab_employee, text="Gender")
    label_gender.grid(row=0, column=4, padx=(10, 5), pady=(10, 5), sticky="w")
    label_national_code = Label(tab_employee, text="National Code")
    label_national_code.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
    label_username = Label(tab_employee, text="username")
    label_username.grid(row=1, column=2, padx=(10, 5), pady=5, sticky="w")
    label_status = Label(tab_employee, text="Status")
    label_status.grid(row=1, column=4, padx=(10, 5), pady=5, sticky="w")

    entry_first_name = Entry(tab_employee, width=15)
    entry_first_name.grid(row=0, column=1, pady=(10, 5), sticky="w")
    entry_first_name.focus()
    entry_last_name = Entry(tab_employee, width=20)
    entry_last_name.grid(row=0, column=3, pady=(10, 5), sticky="w")
    entry_national_code = Entry(tab_employee, width=15)
    entry_national_code.grid(row=1, column=1, pady=(10, 5), sticky="w")
    entry_username = Entry(tab_employee, width=15)
    entry_username.grid(row=1, column=3, padx=(0, 10), pady=5, sticky="w")

    gender_var = StringVar()
    gender_combobox = ttk.Combobox(tab_employee, width=10, textvariable=gender_var)
    gender_combobox['values'] = ("Male", "Female")
    gender_combobox.grid(row=0, column=5, padx=(0, 10), pady=(10, 5), sticky="w")

    status_var = StringVar()
    status_combobox = ttk.Combobox(tab_employee, width=10, textvariable=status_var)
    status_combobox['values'] = ("Active", "Deactivated")
    status_combobox.grid(row=1, column=5, pady=5, sticky="w")
    status_var.set("Deactivated")

    separator = ttk.Separator(tab_employee, orient='horizontal')
    separator.grid(row=3, columnspan=6, sticky='ew', pady=(10, 0))

    frame_tab_employee = Frame(tab_employee)
    frame_tab_employee.grid(row=4, column=0, columnspan=6, padx=(0, 10), pady=5)



    button_add_employee = Button(
        frame_tab_employee, text="Add Employee", width=12, command=button_add_employee_clicked
        )  # TODO: Write
    # code.



    button_add_employee.grid(row=4, column=0, padx=(0, 10), pady=5)
    button_employee_list = Button(frame_tab_employee, text="List", width=12, command="")  #
    # TODO: Write
    # code.
    button_employee_list.grid(row=4, column=1, padx=(0, 10), pady=5)
    button_search_employee = Button(frame_tab_employee, text="Search", width=10, command="")  # TODO: Write code.
    button_search_employee.grid(row=4, column=2, padx=(0, 10), pady=5)
    button_logout = Button(frame_tab_employee, text="Logout", width=10, command=lambda: logged_out(win_admin, frame))
    button_logout.grid(row=4, column=3, padx=(0, 10), pady=5)

    # ================= Admin Tab
    label_employee_code = Label(tab_admin, text="Employee Code")
    label_employee_code.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="w")
    label_username = Label(tab_admin, text="username")
    label_username.grid(row=0, column=2, padx=(10, 5), pady=(10, 5), sticky="w")
    label_status = Label(tab_admin, text="Status")
    label_status.grid(row=0, column=4, padx=(10, 5), pady=(10, 5), sticky="w")
    label_first_name = Label(tab_admin, text="First Name")
    label_first_name.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
    label_last_name = Label(tab_admin, text="Last Name")
    label_last_name.grid(row=1, column=2, padx=(10, 5), pady=5, sticky="w")

    # entry_employee_code = Entry(tab_admin, width=15)
    # entry_employee_code.grid(row=0, column=1, pady=(10, 5), sticky="w")
    entry_username = Entry(tab_admin, width=15)
    entry_username.grid(row=0, column=3, padx=(0, 10), pady=(10, 5), sticky="w")
    # entry_status = Entry(tab_admin, width=15)
    # entry_status.grid(row=0, column=5, pady=(10, 5), sticky="w")
    entry_first_name = Entry(tab_admin, width=15)
    entry_first_name.grid(row=1, column=1, pady=5, sticky="w")
    entry_first_name.focus()
    entry_last_name = Entry(tab_admin, width=20)
    entry_last_name.grid(row=1, column=3, pady=5, sticky="w")

    employee_code_var = StringVar()
    employee_code_combobox = ttk.Combobox(tab_admin, width=10, textvariable=employee_code_var)
    employee_code_combobox['values'] = ("Male", "Female")
    employee_code_combobox.grid(row=0, column=1, pady=(10, 5), sticky="w")

    admin_status_var = StringVar()
    admin_status_combobox = ttk.Combobox(tab_admin, width=10, textvariable=admin_status_var)
    admin_status_combobox['values'] = ("Active", "Deactivated")
    admin_status_combobox.grid(row=0, column=5, pady=(10, 5), sticky="w")
    admin_status_var.set("Deactivated")

    separator = ttk.Separator(tab_admin, orient='horizontal')
    separator.grid(row=3, columnspan=6, sticky='ew', pady=(10, 0))

    frame_tab_employee = Frame(tab_admin)
    frame_tab_employee.grid(row=4, column=0, columnspan=6, padx=(0, 10), pady=5)

    button_add_admin = Button(frame_tab_employee, text="Add Admin", width=12, command="")  # TODO: Write code.
    button_add_admin.grid(row=4, column=0, padx=(0, 10), pady=5)
    button_admin_list = Button(frame_tab_employee, text="List", width=12, command="")  # TODO: Write code.
    button_admin_list.grid(row=4, column=1, padx=(0, 10), pady=5)
    button_search_admin = Button(frame_tab_employee, text="Search", width=10, command="")  # TODO: Write code.
    button_search_admin.grid(row=4, column=2, padx=(0, 10), pady=5)
    button_logout = Button(frame_tab_employee, text="Logout", width=10, command=lambda: logged_out(win_admin, frame))
    button_logout.grid(row=4, column=3, padx=(0, 10), pady=5)

    win_admin.mainloop()


# ================= User Window
def user_logged_in():
    pass


def logged_out(window, frame):
    window.destroy()
    clear_frame(frame)
    login_page()


# TODO: Temporary disabled.
# login_page()

# TODO: Temporary code.
admin_logged_in()

# TODO: Remember
# add reset password.
# add add as admin

# button_delete_admin = Button(frame_tab_admin, text="Delete", width=10, command="")
# button_delete_admin.grid(row=4, column=4, padx=(0, 10), pady=5)
