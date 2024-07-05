from tkinter import Tk, Label, Entry, Button, Frame, StringVar, ttk
from PIL import Image, ImageTk
from backend import *


# ================= Login Page
# <editor-fold desc="Login Page">
# TODO: Temporary disabled.
# root = Tk()
# image_path = "background.png"
# image = Image.open(image_path)
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
        if login_value == "Admin":
            admin_logged_in()
        else:
            user_logged_in()

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
    # TODO: Temporary screen_width and screen_height.
    screen_width = 1920
    screen_height = 1200
    # <editor-fold desc="Admin Window">
    win_admin = Tk()
    win_admin.title("Administrator Panel")
    win_admin.geometry(f"650x200+{int(screen_width / 2) - 325}+{int(screen_height / 2) - 200}")
    win_admin.resizable(width=False, height=False)

    # win_admin.overrideredirect(True) # TODO: Temporary disabled.

    tab_control = ttk.Notebook(win_admin)
    admin_tab = Frame(tab_control, borderwidth=3, pady=5, relief="groove")
    # flat, groove, raised, ridge, solid, or sunken
    employee_tab = Frame(tab_control, borderwidth=3, pady=5, relief="groove")
    tab_control.add(employee_tab, text="Employee ")
    tab_control.add(admin_tab, text="Admin")
    tab_control.grid(row=0, column=0, padx=(15, 15), pady=10)
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

    first_name_entry = Entry(employee_tab, width=15)
    first_name_entry.grid(row=0, column=1, pady=(10, 5), sticky="w")
    first_name_entry.focus()
    last_name_entry = Entry(employee_tab, width=20)
    last_name_entry.grid(row=0, column=3, pady=(10, 5), sticky="w")
    national_code_entry = Entry(employee_tab, width=15)
    national_code_entry.grid(row=1, column=1, pady=(10, 5), sticky="w")
    username_entry = Entry(employee_tab, width=20, state='disabled')
    username_entry.grid(row=1, column=3, padx=(0, 10), pady=5, sticky="w")

    gender_var = StringVar()
    gender_combobox = ttk.Combobox(employee_tab, width=10, textvariable=gender_var)
    gender_combobox['values'] = ("Male", "Female")
    gender_combobox.grid(row=0, column=5, padx=(0, 10), pady=(10, 5), sticky="w")

    status_var = StringVar()
    status_combobox = ttk.Combobox(employee_tab, width=10, textvariable=status_var)
    status_combobox['values'] = ("Yes", "No")
    status_combobox.grid(row=1, column=5, pady=5, sticky="w")
    status_var.set("No")

    separator = ttk.Separator(employee_tab, orient='horizontal')
    separator.grid(row=3, columnspan=6, sticky='ew', pady=(10, 0))

    employee_frame_tab = Frame(employee_tab)
    employee_frame_tab.grid(row=4, column=0, columnspan=6, padx=(0, 10), pady=5)

    add_employee_button = Button(
        employee_frame_tab, text="Add Employee", width=12, command=lambda:add_employee_button_clicked(employee_tab))

    add_employee_button.grid(row=4, column=0, padx=(0, 10), pady=5)
    employee_list_button = Button(employee_frame_tab, text="List", width=12, command="")  #
    # TODO: Write code.
    employee_list_button.grid(row=4, column=1, padx=(0, 10), pady=5)
    search_employee_button = Button(employee_frame_tab, text="Search", width=10, command="")  # TODO: Write code.
    search_employee_button.grid(row=4, column=2, padx=(0, 10), pady=5)
    logout_button = Button(employee_frame_tab, text="Logout", width=10, command=lambda: logged_out(win_admin, frame))
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

    username_entry = Entry(admin_tab, width=20, state='disabled')
    username_entry.grid(row=0, column=3, padx=(0, 10), pady=(10, 5), sticky="w")
    first_name_entry = Entry(admin_tab, width=15, state='disabled')
    first_name_entry.grid(row=1, column=1, pady=5, sticky="w")
    first_name_entry.focus()
    last_name_entry = Entry(admin_tab, width=20, state='disabled')
    last_name_entry.grid(row=1, column=3, pady=5, sticky="w")

    def employee_code_combobox_select(event):
        employee_code = employee_code_var.get()
        clear_entry(admin_tab)
        fill_admin_info(employee_code, admin_tab)

    employee_code_var = StringVar()
    employee_code_combobox = ttk.Combobox(admin_tab, width=10, textvariable=employee_code_var)
    employee_code_combobox['values'] = employee_list()
    employee_code_combobox.grid(row=0, column=1, pady=(10, 5), sticky="w")
    employee_code_combobox.bind('<<ComboboxSelected>>', employee_code_combobox_select)

    admin_status_var = StringVar()
    admin_status_combobox = ttk.Combobox(admin_tab, width=5, textvariable=admin_status_var)
    admin_status_combobox['values'] = ("Yes", "No")
    admin_status_combobox.grid(row=0, column=5, pady=(10, 5), sticky="w")

    is_admin_var = StringVar()
    is_admin_combobox = ttk.Combobox(admin_tab, width=5, textvariable=is_admin_var)
    is_admin_combobox['values'] = ("Yes", "No")
    is_admin_combobox.grid(row=1, column=5, pady=(10, 5), sticky="w")

    separator = ttk.Separator(admin_tab, orient='horizontal')
    separator.grid(row=3, columnspan=6, sticky='ew', pady=(10, 0))

    admin_frame_tab = Frame(admin_tab)
    admin_frame_tab.grid(row=4, column=0, columnspan=6, padx=(0, 10), pady=5)

    submit_admin_button = Button(
        admin_frame_tab, text="Submit Changes", width=15,
        command=lambda: submit_admin_button_clicked(admin_tab)
    )

    submit_admin_button.grid(row=4, column=0, padx=(0, 10), pady=5)

    def list_admin_button_clicked():
        column = ["employee_code", "first_name", "last_name", "username", "employee_status"]
        data = get_list("Employee", column, f"is_admin='{1}'")

        list_view = Tk()
        list_view.title("List OF Administrators")
        list_view.minsize(600, 400)

        def close_button_clicked():
            win_admin.attributes('-disabled', 0)
            list_view.destroy()
        win_admin.attributes('-disabled', 1)
        list_view.protocol("WM_DELETE_WINDOW", close_button_clicked)


        style = ttk.Style(list_view)
        style.theme_use('clam')  # or 'alt', 'default', 'classic', 'vista'
        style.configure("Treeview.Heading", font=('Calibri', 12, 'bold'))
        style.configure("Treeview", font=('Helvetica', 12), rowheight=30)
        style.map("Treeview", background=[('selected', 'lightblue')], foreground=[('selected', 'black')])

        header = ("Employee Code", "First Name", "Last Name", "Username", "Status")
        tree = ttk.Treeview(list_view, columns=header, show="headings")
        tree.tag_configure('Inactive', foreground='red')

        for item in header:
            tree.heading(item, text=item)

        for item in data:
            status = "Active" if item[4] == 1 else "Inactive"
            tag = ("Inactive",) if status == "Inactive" else ()
            tree.insert("", "end", values=(item[0], item[1], item[2], item[3], status), tags=tag)

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

    list_admin_button = Button(
        admin_frame_tab, text="List of Admins", width=15, command=list_admin_button_clicked
    )
    list_admin_button.grid(row=4, column=1, padx=(0, 10), pady=5)
    reset_password_button = Button(
        admin_frame_tab, text="Reset Password", width=15,
        command=lambda: reset_password_button_clicked(admin_tab)
    )
    reset_password_button.grid(row=4, column=2, padx=(0, 10), pady=5)
    logout_button = Button(admin_frame_tab, text="Logout", width=15, command=lambda: logged_out(win_admin, frame))
    logout_button.grid(row=4, column=3, padx=(0, 10), pady=5)

    win_admin.mainloop()
    # </editor-fold>


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
# change default password
# add reset password.
# add add as admin

# button_delete_admin = Button(frame_tab_admin, text="Delete", width=10, command="")
# button_delete_admin.grid(row=4, column=4, padx=(0, 10), pady=5)
