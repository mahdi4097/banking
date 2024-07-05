from page import *
from PIL import Image
from tkinter import BooleanVar


# Function to create the login frame
def login_frame(root):
    root.title("The World Bank")
    design_label = CTkLabel(master=root, text="© Designed and Programmed by Farzad Gouya")
    design_label.pack(side="bottom")
    login_logo = CTkImage(Image.open("Data/Icon/login.png"), size=(200, 130))
    open_eye_icon = CTkImage(Image.open("Data/Icon/open_eye.ico"), size=(15, 15))
    close_eye_icon = CTkImage(Image.open("Data/Icon/close_eye.ico"), size=(15, 15))

    # Function to toggle the visibility of the password
    def toggle_password():
        if password_entry.cget("show") == '*':
            password_entry.configure(show='')
            eye_button.configure(image=open_eye_icon)
        else:
            password_entry.configure(show='*')
            eye_button.configure(image=close_eye_icon)

    windows_frame = CTkFrame(master=root)
    windows_frame.pack(pady=100, padx=100, fill="both", expand=True)
    frame = CTkFrame(master=windows_frame, fg_color="transparent")
    frame.place(relx=0.5, rely=0.5, anchor='center')
    frame.grid_columnconfigure(0, weight=1)

    login_label = CTkLabel(master=frame, image=login_logo, text="")
    login_label.grid(row=0, column=0, pady=(40, 0))

    username_entry = CTkEntry(master=frame, width=200, placeholder_text="Username")
    username_entry.grid(row=1, column=0, pady=(20, 0))

    password_entry = CTkEntry(master=frame, width=165, placeholder_text="Password", show="*")
    password_entry.grid(row=2, column=0, pady=(10, 0), sticky="w")

    eye_button = CTkButton(master=frame, width=15, image=close_eye_icon, text="", command=toggle_password)
    eye_button.grid(row=2, column=0, pady=(10, 0), sticky="e")
    remember_var = BooleanVar()

    # Function to load saved credentials at the start
    def load_credentials_at_start():
        username, password = load_credentials()
        if username and password:
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            username_entry.insert(0, username)
            password_entry.insert(0, password)
            remember_var.set(True)

    # Function to handle the login process
    def login():
        username, password = load_credentials()
        if username and password:
            renew_login(username, password)
        username = username_entry.get()
        password = password_entry.get()
        if remember_var.get():
            save_credentials(bank.service_name, username, password)
        name = login_action(username, password)
        if name:
            bank.avatar_path = None
            bank.logged_in_user = username
            get_avatar_path(username)
            if bank.user_type == 1:
                design_label.destroy()
                admin_frame(root, windows_frame, name)
            else:
                design_label.destroy()
                customer_frame(root, windows_frame, name)

    login_button = CTkButton(master=frame, width=200, text="Login", command=login)
    login_button.grid(row=3, column=0, pady=(10, 0))

    exit_button = CTkButton(master=frame, width=200, text="Exit", command=root.destroy)
    exit_button.grid(row=4, column=0, pady=(10, 0))

    remember_checkbox = CTkCheckBox(master=frame, text="Remember Me", variable=remember_var)
    remember_checkbox.grid(row=6, column=0, pady=(20, 40))

    load_credentials_at_start()


reload_login_page(login_frame)


# Function to create the root page
def root_page():
    set_appearance_mode("system")
    set_default_color_theme("dark-blue")

    root = CTk()
    root.iconbitmap("Data/Icon/favicon.ico")
    root.resizable(False, False)
    root.after(0, lambda: root.state('zoomed'))
    login_frame(root)
    root.mainloop()


root_page()
