import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
import os
from tkinter.ttk import Treeview
import sqlite3

con= sqlite3.connect("bank.db")

login_ok=0

class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("فرم ورود به برنامه")
        self.root.geometry("800x600+{}+{}".format(
        int(self.root.winfo_screenwidth() / 2 - 800 / 2),
        int(self.root.winfo_screenheight() / 2 - 600 / 2)
        ))
      # ایجاد ویجت Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # تب اول: اطلاعات کارکرد
        self.login_tab = ttk.Frame(self.notebook)

        # گروه باکس اطلاعات شخصی
        self.login_group = ttk.LabelFrame(self.login_tab, text="اطلاعات شخصی")
        self.login_group.pack(padx=10, pady=10, ipadx=10, ipady=10, fill="both", expand=True)
        self.login_group.place(relx=0.5, rely=0.5, anchor="center")

        self.lblCode=tk.Label(self.login_group,text='نام کاربری')
        self.lblCode.grid(row=1,column=1)

        self.txtUsername=tk.Entry(self.login_group,justify="right")
        self.txtUsername.grid(row=1,column=0)

        self.lblCode=tk.Label(self.login_group,text='گذروآژه')
        self.lblCode.grid(row=2,column=1)

        self.txtPassword=tk.Entry(self.login_group,justify="right")
        self.txtPassword.grid(row=2,column=0)

        self.btnLogin=tk.Button(self.login_group,text='ورود به برنامه',command=self.login)
        self.btnLogin.grid(row=9,column=0)


        self.btnClear=tk.Button(self.login_group,text='خروج ',command=self.exit)
        self.btnClear.grid(row=9,column=1)


        self.notebook.add(self.login_tab, text="فرم ورود")

    def login(self):
        global login_ok
        global con
        cursor = con.cursor()
        cursor.execute(""" select count(*) from employee where username=? and password=? """,(self.txtUsername.get(),self.txtPassword.get()))
        result = cursor.fetchone()
        if int(result[0]) > 0:
            messagebox.showinfo("پیغام", "با موفقیت وارد شدید") 
            login_ok=1
            self.root.destroy()
        else:
            messagebox.showerror("پیغام", "نام کاربری یا گذرواژه اشتباه میباشد") 
            self.root.deiconify()


    def exit(self):
        exit()

class PersenelForm:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(self.parent)
        self.root.title("ثبت پرسنل جدید")
        self.root.geometry("800x600+{}+{}".format(
        int(self.root.winfo_screenwidth() / 2 - 800 / 2),
        int(self.root.winfo_screenheight() / 2 - 600 / 2)
        ))
       
      # ایجاد ویجت Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

 
        self.family_tab = ttk.Frame(self.notebook)

        self.family_group = ttk.LabelFrame(self.family_tab, text="اطلاعات شخصی")
        self.family_group.pack( fill="both", expand=True)
        self.family_group.place(relx=0.5, rely=0.5, anchor="center")

    
        self.lblName=tk.Label(self.family_group,text='نام و نام خانوادگی')
        self.lblName.grid(row=0,column=1)

        self.txtFlname=tk.Entry(self.family_group,justify="right")
        self.txtFlname.grid(row=0,column=0)


        self.lblName=tk.Label(self.family_group,text='کد ملی')
        self.lblName.grid(row=1,column=1)

        self.txtCodem=tk.Entry(self.family_group,justify="left")
        self.txtCodem.grid(row=1,column=0)

        self.lblName=tk.Label(self.family_group,text='تلفن همراه')
        self.lblName.grid(row=2,column=1)

        self.txtTell=tk.Entry(self.family_group,justify="left")
        self.txtTell.grid(row=2,column=0)

        self.lblName=tk.Label(self.family_group,text='نام کاربری')
        self.lblName.grid(row=3,column=1)

        self.txtUsername=tk.Entry(self.family_group,justify="left")
        self.txtUsername.grid(row=3,column=0)


        self.lblName=tk.Label(self.family_group,text='گذرواژه')
        self.lblName.grid(row=4,column=1)

        self.txtPassword=tk.Entry(self.family_group,justify="left")
        self.txtPassword.grid(row=4,column=0)

        self.btnInsert=tk.Button(self.family_group,text='ثبت اطلاعات ',command=self.insert)
        self.btnInsert.grid(row=5,column=0)


        self.btnClear=tk.Button(self.family_group,text='پاکسازی',command=self.clear)
        self.btnClear.grid(row=5,column=1)

        self.lblCodePerseneliSearch=tk.Label(self.family_group,text='کد پرسنلی یا کد ملی')
        self.lblCodePerseneliSearch.grid(row=6,column=1)

        self.txtCodePerseneliSearch=tk.Entry(self.family_group,justify="left")
        self.txtCodePerseneliSearch.grid(row=6,column=0)


        self.btnSearch=tk.Button(self.family_group,text='جستجو اطلاعات',command=self.search)
        self.btnSearch.grid(row=7,column=0)

        self.btnEdit=tk.Button(self.family_group,text='ویرایش اطلاعات',command=self.edit)
        self.btnEdit.grid(row=8,column=0)


        self.btnDelete=tk.Button(self.family_group,text='حذف',command=self.delete)
        self.btnDelete.grid(row=8,column=1)


        self.notebook.add(self.family_tab, text="اطلاعات شخصی")

    def clear(self):
        self.txtFlname.delete(0, tk.END)
        self.txtTell.delete(0, tk.END)
        self.txtCodem.delete(0, tk.END)
        self.txtUsername.delete(0, tk.END)
        self.txtPassword.delete(0, tk.END)
        self.txtCodePerseneliSearch.delete(0,tk.END)

    def edit(self):
        if self.txtFlname.get() == "" or self.txtCodem.get() == "" or self.txtTell.get() == "" or self.txtUsername.get() == "" or self.txtPassword.get() == "":
            messagebox.showerror("پیغام", "یکی از مقادیر خالی میباشد") 
            self.root.deiconify()
            return
        global con 
        cursor = con.cursor()
        cursor.execute(""" update employee set flname=?,tell=?,password=? where codem=?""",(self.txtFlname.get(),self.txtTell.get(),self.txtPassword.get(),self.txtCodem.get()))
        con.commit()
        messagebox.showinfo("پیغام", "با موفقیت ویرایش شد") 
        self.root.deiconify()
        self.clear()


    def delete(self):
        if self.txtFlname.get() == "" or self.txtCodem.get() == "" or self.txtTell.get() == "" or self.txtUsername.get() == "" or self.txtPassword.get() == "":
            messagebox.showerror("پیغام", "یکی از مقادیر خالی میباشد") 
            self.root.deiconify()
            return
        global con 
        cursor = con.cursor()
        cursor.execute(""" delete from employee where codem=? """,(str(self.txtCodem.get()),))
        con.commit()
        messagebox.showinfo("پیغام", "با موفقیت حذف شد") 
        self.root.deiconify()
        self.clear()


    def insert(self):
        global con
        if self.txtFlname.get() == "" or self.txtCodem.get() == "" or self.txtTell.get() == "" or self.txtUsername.get() == "" or self.txtPassword.get() == "":
            messagebox.showerror("پیغام", "یکی از مقادیر خالی میباشد") 
            self.root.deiconify()
            return
        
        cursor = con.cursor()
        cursor.execute(""" insert into employee(flname,codem,tell,username,password) values(?,?,?,?,?) """,(self.txtFlname.get(),self.txtCodem.get(),self.txtTell.get(),self.txtUsername.get(),self.txtPassword.get()))
        con.commit()
        messagebox.showinfo("پیغام", "با موفقیت افزوده شد") 
        self.root.deiconify()
        self.clear()


    def search(self):
        global con
        check = False
        cursor = con.cursor()
        reuslt = cursor.execute("""select flname,codem,tell,username,password from employee where id=? or codem=?""",(self.txtCodePerseneliSearch.get(),self.txtCodePerseneliSearch.get()))
        for item in reuslt:
            self.txtFlname.insert(0,item[0])
            self.txtCodem.insert(0,item[1])
            self.txtTell.insert(0,item[2])
            self.txtUsername.insert(0,item[3])
            self.txtPassword.insert(0,item[4])
            check = True
            break
        if check == False:
            messagebox.showerror("پیغام", "پرسنلی یافت نشد") 
            self.root.deiconify()
            self.clear()

class AccountForm:
    def __init__(self, parent):
        self.root =parent
        self.root = tk.Toplevel(self.root)

        self.root.title("ثبت حساب جدید")
        self.root.geometry("800x600+{}+{}".format(
        int(self.root.winfo_screenwidth() / 2 - 800 / 2),
        int(self.root.winfo_screenheight() / 2 - 600 / 2)
        ))
       
      # ایجاد ویجت Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.chk_var = tk.IntVar()

        self.family_tab = ttk.Frame(self.notebook)

        self.family_group = ttk.LabelFrame(self.family_tab, text="اطلاعات حساب")
        self.family_group.pack( fill="both", expand=True)
        self.family_group.place(relx=0.5, rely=0.5, anchor="center")

    
        self.lblName=tk.Label(self.family_group,text='شماره حساب')
        self.lblName.grid(row=0,column=1)

        self.txtShHesab=tk.Entry(self.family_group,justify="left")
        self.txtShHesab.grid(row=0,column=0)


        self.lblName=tk.Label(self.family_group,text='دارنده حساب')
        self.lblName.grid(row=1,column=1)

        self.txtCodem=tk.Entry(self.family_group,justify="left")
        self.txtCodem.grid(row=1,column=0)

        self.lblName=tk.Label(self.family_group,text='تلفن همراه')
        self.lblName.grid(row=2,column=1)

        self.txtTell=tk.Entry(self.family_group,justify="left")
        self.txtTell.grid(row=2,column=0)

        self.lblName=tk.Label(self.family_group,text='موجودی اولیه')
        self.lblName.grid(row=3,column=1)

        self.txtBalance=tk.Entry(self.family_group,justify="left")
        self.txtBalance.grid(row=3,column=0)



        self.lblName=tk.Label(self.family_group,text='بانک')
        self.lblName.grid(row=4,column=1)

        self.txtBank=tk.Entry(self.family_group,justify="right")
        self.txtBank.grid(row=4,column=0)

        self.lblED=tk.Label(self.family_group,text='فعال یا غیر فعال')
        self.lblED.grid(row=5,column=1)

        self.chkED=tk.Checkbutton(self.family_group,variable=self.chk_var)
        self.chkED.grid(row=5,column=0)




        self.btnInsert=tk.Button(self.family_group,text='ثبت اطلاعات ',command=self.insert)
        self.btnInsert.grid(row=6,column=0)


        self.btnClear=tk.Button(self.family_group,text='پاکسازی',command=self.clear)
        self.btnClear.grid(row=6,column=1)

        self.lblCodePerseneliSearch=tk.Label(self.family_group,text='کد پرسنلی یا کد ملی')
        self.lblCodePerseneliSearch.grid(row=7,column=1)

        self.txtCodePerseneliSearch=tk.Entry(self.family_group,justify="left")
        self.txtCodePerseneliSearch.grid(row=7,column=0)

        self.btnSearch=tk.Button(self.family_group,text='جستجو اطلاعات',command=self.search)
        self.btnSearch.grid(row=8,column=0)

        self.btnEdit=tk.Button(self.family_group,text='ویرایش اطلاعات',command=self.edit)
        self.btnEdit.grid(row=9,column=0)


        self.btnDelete=tk.Button(self.family_group,text='حذف',command=self.delete)
        self.btnDelete.grid(row=9,column=1)

        self.lblPriceBardasht=tk.Label(self.family_group,text='مبلغ برای برداشت')
        self.lblPriceBardasht.grid(row=10,column=1)

        self.txtPrice=tk.Entry(self.family_group,justify="left")
        self.txtPrice.grid(row=10,column=0)

        self.btnBardasht=tk.Button(self.family_group,text=' برداشت از حساب',command=self.bardasht)
        self.btnBardasht.grid(row=11,column=0)

        self.notebook.add(self.family_tab, text="اطلاعات شخصی")

    def clear(self):
        self.txtShHesab.delete(0, tk.END)
        self.txtTell.delete(0, tk.END)
        self.txtCodem.delete(0, tk.END)
        self.txtBalance.delete(0, tk.END)
        self.txtBank.delete(0, tk.END)

    def edit(self):
        if self.txtShHesab.get() == "" or self.txtCodem.get() == "" or self.txtTell.get() == "" or self.txtBalance.get() == "" or self.txtBank.get() == "":
            messagebox.showerror("پیغام", "یکی از مقادیر خالی میباشد") 
            self.root.deiconify()
            return
        
        global con 
        cursor = con.cursor()
        cursor.execute(""" update account set tell=?,balance=?,bank=?,ed=? where shhesab=?""",(self.txtTell.get(),self.txtBalance.get(),self.txtBank.get(),self.chk_var.get(),self.txtShHesab.get()))
        con.commit()
        messagebox.showinfo("پیغام", "با موفقیت ویرایش شد") 
        self.root.deiconify()
        self.clear()

    def bardasht(self):
        if self.txtShHesab.get() == "" or  self.txtPrice.get() == "":
            messagebox.showerror("پیغام", "یکی از مقادیر خالی میباشد") 
            self.root.deiconify()
            return
        if int(self.txtPrice.get()) <= 0 :
            messagebox.showerror("پیغام", "مبلغ قابل برداشت نیست") 
            self.root.deiconify()
            return
        if int(self.txtBalance.get()) < int(self.txtPrice.get()) :
            messagebox.showerror("پیغام", "مبلغ بیشتر از موجودی میباشد") 
            self.root.deiconify()
            return

        global con 
        cursor = con.cursor()
        cursor.execute(""" update account set balance=balance-? where shhesab=?""",(self.txtPrice.get(),self.txtShHesab.get()))
        con.commit()
        messagebox.showinfo("پیغام", "با موفقیت برداشت شد") 
        self.root.deiconify()
        self.clear()

    def insert(self):
        global con
        if self.txtShHesab.get() == "" or self.txtCodem.get() == "" or self.txtTell.get() == "" or self.txtBalance.get() == "" or self.txtBank.get() == "":
            messagebox.showerror("پیغام", "یکی از مقادیر خالی میباشد") 
            self.root.deiconify()
            return
        
        cursor = con.cursor()
        cursor.execute(""" insert into account(shhesab,codem,tell,balance,bank,ed) values(?,?,?,?,?,?) """,(self.txtShHesab.get(),self.txtCodem.get(),self.txtTell.get(),self.txtBalance.get(),self.txtBank.get(),self.chk_var.get()))
        con.commit()
        messagebox.showinfo("پیغام", "با موفقیت افزوده شد") 
        self.root.deiconify()
        self.clear()

    def delete(self):
        if self.txtShHesab.get() == "" or self.txtCodem.get() == "" or self.txtTell.get() == "" or self.txtBalance.get() == "" or self.txtBank.get() == "":
            messagebox.showerror("پیغام", "یکی از مقادیر خالی میباشد") 
            self.root.deiconify()
            return
        global con 
        cursor = con.cursor()
        cursor.execute(""" delete from account where shhesab=? """,(str(self.txtShHesab.get()),))
        con.commit()
        messagebox.showinfo("پیغام", "با موفقیت حذف شد") 
        self.root.deiconify()
        self.clear()

    def search(self):
        global con
        check = False
        cursor = con.cursor()
        reuslt = cursor.execute("""select shhesab,codem,tell,balance,bank,ed from account where shhesab=? or codem=?""",(self.txtCodePerseneliSearch.get(),self.txtCodePerseneliSearch.get()))
        for item in reuslt:
            self.txtShHesab.insert(0,item[0])
            self.txtCodem.insert(0,item[1])
            self.txtTell.insert(0,item[2])
            self.txtBalance.insert(0,item[3])
            self.txtBank.insert(0,item[4])
            if (item[5] == True):
                self.chkED.select()
            else:
                self.chkED.deselect()
            check = True
            break
        if check == False:
            messagebox.showerror("پیغام", "حسابی یافت نشد") 
            self.root.deiconify()
            self.clear()

class TransferForm:
    def __init__(self, parent):
        self.root =parent
        self.root = tk.Toplevel(self.root)

        self.root.title("واریز به حساب دیگران ")
        self.root.geometry("800x600+{}+{}".format(
        int(self.root.winfo_screenwidth() / 2 - 800 / 2),
        int(self.root.winfo_screenheight() / 2 - 600 / 2)
        ))
       
      # ایجاد ویجت Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")


        self.family_tab = ttk.Frame(self.notebook)

        self.family_group = ttk.LabelFrame(self.family_tab, text="اطلاعات حساب")
        self.family_group.pack( fill="both", expand=True)
        self.family_group.place(relx=0.5, rely=0.5, anchor="center")

    
        self.lblSource=tk.Label(self.family_group,text='شماره حساب مبدا')
        self.lblSource.grid(row=0,column=1)

        self.txtSource=tk.Entry(self.family_group,justify="left")
        self.txtSource.grid(row=0,column=0)


        self.lblDestination=tk.Label(self.family_group,text='شماره حساب مقصد')
        self.lblDestination.grid(row=1,column=1)

        self.txtDest=tk.Entry(self.family_group,justify="left")
        self.txtDest.grid(row=1,column=0)


        self.lblName=tk.Label(self.family_group,text='مبلغ')
        self.lblName.grid(row=3,column=1)

        self.txtPrice=tk.Entry(self.family_group,justify="left")
        self.txtPrice.grid(row=3,column=0)

        self.btnTransfer=tk.Button(self.family_group,text='انتقال ',command=self.transfer)
        self.btnTransfer.grid(row=6,column=0)


        self.btnClear=tk.Button(self.family_group,text='پاکسازی',command=self.clear)
        self.btnClear.grid(row=6,column=1)


        self.notebook.add(self.family_tab, text="اطلاعات شخصی")

    def clear(self):
        self.txtSource.delete(0, tk.END)
        self.txtDest.delete(0, tk.END)
        self.txtPrice.delete(0, tk.END)


    def transfer(self):
        

        source=""
        sourceB=0
        dest=""
        destB=0
        

        if self.txtSource.get() == "" or self.txtDest.get() == "" or self.txtPrice.get() == "" :
            messagebox.showerror("پیغام", "یکی از مقادیر خالی میباشد") 
            self.root.deiconify()
            return
        
        global con
        check = False
        cursor = con.cursor()
        reuslt = cursor.execute("""select shhesab,balance from account where shhesab=? """,(self.txtSource.get(),))
        for item in reuslt:
            source = item[0]
            sourceB = int(item[1])
            check=True
            break
        if check == False:
            messagebox.showerror("پیغام", "حسابی یافت نشد") 
            self.root.deiconify()
            self.clear()
            return

        check = False
        cursor = con.cursor()
        reuslt = cursor.execute("""select shhesab,balance from account where shhesab=? """,(self.txtDest.get(),))
        for item in reuslt:
            dest = item[0]
            destB = int(item[1])
            check=True
            break
        if check == False:
            messagebox.showerror("پیغام", "حسابی یافت نشد") 
            self.root.deiconify()
            self.clear()
            return

        if int(sourceB) < int(self.txtPrice.get()):
            messagebox.showerror("پیغام", "موجودی کافی نمیباشد") 
            self.root.deiconify()
            self.clear()
            return

        cursor = con.cursor()
        cursor.execute(""" update account set balance=balance+? where shhesab=?""",(self.txtPrice.get(),self.txtDest.get()))
        con.commit()

        cursor = con.cursor()
        cursor.execute(""" update account set balance=balance-? where shhesab=?""",(self.txtPrice.get(),self.txtSource.get()))
        con.commit()
        
        messagebox.showinfo("پیغام", "با موفقیت انتقال داده شد") 
        self.root.deiconify()
        self.clear()



class ReportForm:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(self.parent)
        self.root.title("گزارش گیری")
        self.root.geometry("800x600+{}+{}".format(
        int(self.root.winfo_screenwidth() / 2 - 800 / 2),
        int(self.root.winfo_screenheight() / 2 - 600 / 2)
        ))
       
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

 
        self.family_tab = ttk.Frame(self.notebook)

        self.family_group = ttk.LabelFrame(self.family_tab, text="اطلاعات حساب")
        self.family_group.pack( fill="both", expand=True)
        self.family_group.place(relx=0.5, rely=0.5, anchor="center")

        cols=('تلفن دارنده حساب','موجودی','کد ملی صاحب حساب','شماره حساب')
        self.listBox = Treeview(self.family_group, columns=cols, show='headings')
        
        for col in cols:
            self.listBox.heading(col, text=col)    
        
        self.listBox.grid(row=1, column=0, columnspan=2)
        self.listBox.column("# 1", width=120,anchor=tk.CENTER)
        self.listBox.column("# 2", width=120,anchor=tk.CENTER)
        self.listBox.column("# 3", width=120,anchor=tk.CENTER)
        self.listBox.column("# 4", width=120,anchor=tk.CENTER)



        self.lblCodePerseneliSearch=tk.Label(self.family_group,text='کد حساب یا کد ملی')
        self.lblCodePerseneliSearch.grid(row=6,column=1)

        self.txtCodeSearch=tk.Entry(self.family_group,justify="left")
        self.txtCodeSearch.grid(row=6,column=0)

        self.btnSearch=tk.Button(self.family_group,text='جستجو اطلاعات',command=self.search)
        self.btnSearch.grid(row=7,column=0)

        global con 
        cursor = con.cursor()
        result = cursor.execute("select tell,balance,codem,shhesab from account ")
        i=1
        for item in result:
            self.listBox.insert("", "end", values=( item[0],item[1],item[2],item[3]))
            i+=1

        self.btnClear=tk.Button(self.family_group,text='پاکسازی',command=self.clear)
        self.btnClear.grid(row=7,column=1)
        self.notebook.add(self.family_tab, text="جستجو و گزارش اطلاعات حساب")

    def clear(self):
        self.txtCodeSearch.delete(0, tk.END)

    def search(self):
        global con 
        cursor = con.cursor()
        result = cursor.execute("select tell,balance,codem,shhesab from account where codem=? or shhesab=?",(self.txtCodeSearch.get(),self.txtCodeSearch.get()))
        i=1
        x = self.listBox.get_children()
        for item in x:
            self.listBox.delete(item)
        for item in result:
            self.listBox.insert("", "end", values=( item[0],item[1],item[2],item[3]))
            i+=1

class MainForm:
    def __init__(self, root):
        self.root = root
        self.root.title("فرم اصلی")

        self.background_image = Image.open("background.png")  
        self.background_image = self.background_image.resize((800, 600), Image.BILINEAR)  
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.button1 = tk.Button(self.root, text="مدیریت کارمندان", command=self.btnPersenel_click,width=20)
        self.button1.place(x=600, y=200)
        
        self.button2 = tk.Button(self.root, text="ثبت اطلاعات حساب", command=self.btAccount_click,width=20)
        self.button2.place(x=600, y=250)
        
        self.btnTransfer = tk.Button(self.root, text="انقال وجه", command=self.btTransfer_click,width=20)
        self.btnTransfer.place(x=600, y=300)

        self.button3 = tk.Button(self.root, text="جستجو و گزارش حساب", command=self.btnReport,width=20)
        self.button3.place(x=600, y=350)

        self.button5 = tk.Button(self.root, text="خروج", command=self.btnExit_click,width=20)
        self.button5.place(x=100, y=550)

        self.lblWelcome = tk.Label(self.root, text="کاربر عزیز خوش آمدید",width=30)
        self.lblWelcome.place(x=600, y=100)


        self.root.geometry("800x600+{}+{}".format(
        int(self.root.winfo_screenwidth() / 2 - 800 / 2),
        int(self.root.winfo_screenheight() / 2 - 600 / 2)
        ))

    def btnPersenel_click(self):
        new_form = PersenelForm(self.root)

    def btAccount_click(self):
        new_form = AccountForm(self.root)
    
    def btnReport(self):
        new_form = ReportForm(self.root)

    def btTransfer_click(self):
        new_form = TransferForm(self.root)

    def btnExit_click(self):
        exit()


if __name__ == "__main__":
    login = tk.Tk()
    login_form = LoginForm(login)
    login.mainloop()

    if login_ok == 1:
        root = tk.Tk()
        main_form = MainForm(root)
        root.mainloop()
