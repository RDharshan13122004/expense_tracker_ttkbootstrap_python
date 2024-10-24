
from tkinter import *
from tkinter import filedialog
#from tkinter import font
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.toast import ToastNotification
import sqlite3
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import datetime
from datetime import datetime

root = tb.Window(title="Expense Tracker",
                 themename="superhero",
                 iconphoto="C:/Users/dharshan/Desktop/lang and tools/pyvsc/exp_tracker/image/84b81735b361bd85ac4cfef337c88308-removebg-preview.png",
                 size=(600,600))

#classes

class DB_work:

    entries = [] #stores all amount entries 
    combos = [] #store all combo boxes
    dynamic_frames = []  # stores dynamically created frames

    def __init__(self):
        try:
            '''
            # Get the path to the user's Documents folder
            document_path = os.path.join(os.path.expanduser("~"),"Documents")

            # Specify the database location in the Documents folder
            db_path = os.path.join(document_path,"exptracker.db")
            conn = sqlite3.connect(db_path)
            '''
            #connecting DB
            conn = sqlite3.connect("C:/Users/dharshan/Desktop/lang and tools/pyvsc/exp_tracker/exptracker.db")
            query = conn.cursor()

            #Create tables if they don't exist
            query.execute("""create table IF NOT EXISTS DATA(
                        entry_date Date PRIMARY KEY,
                        salary REAL,
                        addional_income REAL DEFAULT NULL,
                        travel REAL DEFAULT NULL,
                        food REAL DEFAULT NULL,
                        regular_expense REAL DEFAULT NULL
                        )""")
            
            query.execute("""create table IF NOT EXISTS Income_expenditure(
                        ITEMs TEXT PRIMARY KEY,
                        Inc_exp TEXT
                        )""")
            
            # Insert default items into Income_expenditure
            default_items = [
                ('addional_income', 'income'),
                ('travel', 'expense'),
                ('food', 'expense'),
                ('regular_expense', 'expense')
            ]

            for item in default_items:
                query.execute("INSERT OR IGNORE INTO Income_expenditure (ITEMs, Inc_exp) VALUES (?, ?)", item)

            conn.commit()

        except sqlite3.Error as e:

            toast = ToastNotification(title="Expense tracker warning message ⚠️",
                                      message=f"An error occurred while working with the database: {e}",
                                      duration=3000,
                                      bootstyle="danger",
                                      alert=True,
                                      ) 
            toast.show_toast()

        finally:
            # Ensure the connection is closed, even if an error occur
            if conn:
                conn.close()

    @classmethod
    def new_section_of_label(cls):
        
        #connecting DB
        conn = sqlite3.connect("C:/Users/dharshan/Desktop/lang and tools/pyvsc/exp_tracker/exptracker.db")
        query = conn.cursor()

        query.execute("select ITEMs from Income_expenditure")
        items_col = query.fetchall()

        # Create a new frame inside the same main frame to hold the new row
        new_set_frame = tb.Frame(main_ex_frame)
        new_set_frame.pack(fill="x", pady=5)
        
        # Add 1st entry in the new row frame
        cls.Exp_amount_entry = tb.Entry(new_set_frame,bootstyle="success")
        cls.Exp_amount_entry.pack(pady=10,side="left",padx=5)

        #creating expenditure category combobox

        cls.items = set()
        for i in items_col:
            val = i[0].replace("_"," ").strip()
            cls.items.add(val)

        # Add 2nd entry in the new row frame, on the same line
        cls.category_combobox = tb.Combobox(new_set_frame,bootstyle="success",values=sorted(list(cls.items)))
        cls.category_combobox.pack(side="left",pady=10,padx=5)

        cls.category_combobox.current(0)

        # Save references for later use
        cls.entries.append(cls.Exp_amount_entry)
        cls.combos.append(cls.category_combobox)
        cls.dynamic_frames.append(new_set_frame)  # Add the frame to the dynamic_frames list

        conn.commit()
        conn.close()


    @classmethod
    def submit(cls):
        conn = sqlite3.connect("C:/Users/dharshan/Desktop/lang and tools/pyvsc/exp_tracker/exptracker.db")
        query =  conn.cursor()

        query.execute("select * from DATA where entry_date = ?",(Date_Entry.entry.get(),))
        ck_data_presented = query.fetchone()

        
        if not ck_data_presented:
            query.execute("insert into DATA (entry_date,salary) values(?,?)",(Date_Entry.entry.get(),salary_Entry.get()))

        # Loop through the dynamically added entries and combo boxes
        for i in range(len(cls.entries)):
            amount = cls.entries[i].get()
            category = cls.combos[i].get()

            print(amount)
            print(category)
            
            if category in cls.items:
                #create a function which need to add record if the record already has a value
                caty_item2 = category.replace(" ", "_").strip().lower() 

                query.execute(f"SELECT {caty_item2} FROM DATA WHERE entry_date = ?", (Date_Entry.entry.get(),))
                ck_1 = query.fetchone()

                # If the category is None, insert the amount
                if ck_1 is None or ck_1[0] is None:
                    query.execute(f"UPDATE DATA SET {caty_item2} = ? WHERE entry_date = ?", (amount, Date_Entry.entry.get()))
                else:
                    existing_value = ck_1[0]

                    # Handle None or empty existing value
                    if not existing_value:
                        existing_value = 0

                    # Safely add the new value
                    try:
                        new_value = float(existing_value) + float(amount)
                        query.execute(f"UPDATE DATA SET {caty_item2} = ? WHERE entry_date = ?", (new_value, Date_Entry.entry.get()))
                    except ValueError:
                        print(f"Invalid data in database or input: {existing_value} or {amount}")

        for i in range(len(cls.entries)):
            amount = cls.entries[i].get()
            category = cls.combos[i].get()

            if category not in cls.items:
                DB_work.category_pop(category,amount)

        conn.commit()
        conn.close()
        
        for frame in cls.dynamic_frames:
            frame.destroy()

        # Clear the lists after destroying the frames
        cls.entries.clear()
        cls.combos.clear()
        cls.dynamic_frames.clear()

    @classmethod
    def category_pop(cls,caty,amt):
        
        new_category_pop = tb.Toplevel(title="new category insert",size=(300,300))

        the_category = caty
        amt_of_newcat = amt
        
        new_category_entry = tb.Entry(new_category_pop)
        new_category_entry.pack(pady=20)
        new_category_entry.insert(0,the_category)

        inc_or_exp = StringVar()

        income_radio_btn = tb.Radiobutton(new_category_pop,variable=inc_or_exp,value="income",bootstyle = "success",text="income")
        income_radio_btn.pack(pady=20)

        expense_radio_btn = tb.Radiobutton(new_category_pop,variable=inc_or_exp,value="expense",bootstyle = "danger",text="expense")
        expense_radio_btn.pack(pady=20)

        cp_submit = tb.Button(new_category_pop,bootstyle="success",text="ADD",command=lambda: DB_work.alt_tables(the_category,inc_or_exp.get(),amt_of_newcat,new_category_pop))
        cp_submit.pack(pady=20)

    @classmethod 
    def alt_tables(cls,caty,value,amt,pop_window):

        caty_item = caty.replace(" ","_").strip().lower()

        the_amount = amt
        
        conn = sqlite3.connect("C:/Users/dharshan/Desktop/lang and tools/pyvsc/exp_tracker/exptracker.db")
        query = conn.cursor()

        query.execute("insert into Income_expenditure values (?,?)",(caty_item,value))

        query.execute(f"ALTER TABLE DATA ADD COLUMN {caty_item} REAL DEFAULT NULL")

        query.execute(f"update DATA set {caty_item} = ? where entry_date = ?",(the_amount,Date_Entry.entry.get()))

        conn.commit()
        conn.close()
        
        pop_window.destroy()

    @classmethod
    def update_salary_for_month(cls,base_date):

        try:

            conn = sqlite3.connect("C:/Users/dharshan/Desktop/lang and tools/pyvsc/exp_tracker/exptracker.db")
            query = conn.cursor()

            base_date_obj = datetime.strptime(base_date,"%d-%m-%Y").replace(day=1)

            query.execute("""select * from DATA where strftime('%Y-%m', entry_date) = strftime('%Y-%m', ?)
            """, (base_date_obj.strftime('%Y-%m-%d'),))

            entries = query.fetchall()

            query.execute("PRAGMA table_info(DATA)")
            columns = query.fetchall()
            column_names = [col[2] for col in columns]

            income_columns = []
            expense_columns = []

            for col in column_names:
                query.execute("SELECT Inc_exp FROM Income_expenditure WHERE ITEMs = ?", (col,))
                inc_exp = query.fetchone()
                if inc_exp:
                    if inc_exp[0] == 'income':
                        income_columns.append(col)
                    elif inc_exp[0] == 'expense':
                        expense_columns.append(col)

            net_income = 0 
            
            if entries:
                for entry in entries:
                    e_date = entry[0]  # entry_date is the first column

                    # Calculate total income dynamically
                    total_income = sum([entry[columns.index(col)] or 0 for col in income_columns])

                    # Calculate total expenses dynamically
                    total_expenses = sum([entry[columns.index(col)] or 0 for col in expense_columns])

                    # Calculate net income
                    net_income = total_income - total_expenses

                    query.execute("""
                        UPDATE DATA
                        SET salary = ?
                        WHERE entry_date > ? AND strftime('%Y-%m', entry_date) = strftime('%Y-%m', ?)
                        LIMIT 1
                    """, (net_income, e_date, base_date_obj.strftime('%Y-%m-%d')))

            # Update the salary entry in the GUI
            salary_Entry.delete(0, END)  # Clear the current value in the salary entry
            salary_Entry.insert(0, net_income)  # Insert the calculated net income

            conn.commit()

        except sqlite3.Error as e:
            # Handle any database errors
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()
#functions

def select_theme(x):
    root.style.theme_use(x)

def on_date_selected():
    selected_date = Date_Entry.entry.get()
    DB_work.update_salary_for_month(selected_date)

def upload_csv():
    CSV_frame.filename = filedialog.askopenfilename(initialdir="C:/users/",title="CSV files",filetypes=[("csv files","*csv")])
    if CSV_frame.filename:  # Check if a file was selected
        # Now you can handle the CSV file as needed
        with open(CSV_frame.filename, newline='') as csvfile:
            # Process the CSV content here, e.g., using the csv module
            reader = csv.reader(csvfile)
            for row in reader:
                print(row)  # Example: Print each row in the CSV file

def enable_disable_date(get_date):

    selected_date = get_date.get()

    if selected_date == "":
        return

    selected_date_obj = datetime.strptime(selected_date,"%d-%m-%Y")
    
    if selected_date_obj.day == 1:
        salary_Entry.config(state="normal") 
    else:
        salary_Entry.config(state="disabled")


#GUI Title

title_label = tb.Label(root,text="Expense Tracker",font=("Poor Richard",38))
title_label.pack(pady=20)

#menubutton label frame
theme_menu_label_frame =tb.Frame(root)
theme_menu_label_frame.pack(pady=10)

#theme menubutton label
menu_label = tb.Label(theme_menu_label_frame,text="Select the theme:")
menu_label.pack(padx=5,side="left")

#theme menubutton
theme_menu = tb.Menubutton(theme_menu_label_frame,bootstyle="info",text="theme")
theme_menu.pack(padx=5,side="left")

#create a menu
select_menu = tb.Menu(theme_menu)

theme_var = StringVar()
for theme in ["cosmo","flatly","litera","minty","lumen","yeti","pulse","united","morph","journal","darkly","superhero","solar","cyborg","vapor","simplex","cerculean"]:
    select_menu.add_radiobutton(label=theme,variable=theme_var,command= lambda x = theme: select_theme(x))

theme_menu["menu"] = select_menu

#to get the font families
"""
font_fam = list(font.families()) 
print(font_fam)
"""

#creating a notebook

note_book = tb.Notebook(root,bootstyle="info")
note_book.pack(pady=40,padx=20,fill="both",expand=1)

#creating frames
DB_frame = tb.Frame(note_book)
CSV_frame = tb.Frame(note_book)
XL_frame = tb.Frame(note_book)

#****************************************************************************************************************************************#
#DB_Frame Section

#creating scrolled frame

DB_Scrolled_frame = ScrolledFrame(DB_frame)
DB_Scrolled_frame.pack(fill=BOTH,expand=True)

intk = DB_work()

#defualt labels and entry

Date_label = tb.Label(DB_Scrolled_frame,text="Date:",font=('Helvertica',18))
Date_label.pack(pady=10)

Date_Entry = tb.DateEntry(DB_Scrolled_frame,firstweekday=6,bootstyle="info")
Date_Entry.pack()

date_get = StringVar()
date_get.trace_add("write",lambda name, mode, value, get_date = date_get: enable_disable_date(get_date))
Date_Entry.entry.config(textvariable=date_get)

Salary_label = tb.Label(DB_Scrolled_frame,text="Salary:",font=('Helvertica',18))
Salary_label.pack(pady=10)

salary_Entry = tb.Entry(DB_Scrolled_frame,state="disabled")
salary_Entry.pack(pady=10,ipadx=16)

#income and expenditure labels,Entry,combobutton

#creating expenditure category label
category_label = tb.Label(DB_Scrolled_frame,text= "Enter the amount and set the category:",font=("Helvertica",18))
category_label.pack(pady=20)

#creating a main frame to hold multiple frames 
main_ex_frame = tb.Frame(DB_Scrolled_frame)
main_ex_frame.pack(pady=5)

#1st frame in main frame and setting a frame to bring the amount entry and category menubutton on a same line
set_frame = tb.Frame(main_ex_frame)
set_frame.pack(fill="x", pady=5)


#add button to insert multiple income and expenditure labels,Entry,combobox

exp_add_button = tb.Button(DB_Scrolled_frame,text="+",bootstyle = "info",command=DB_work.new_section_of_label)
exp_add_button.pack()

'''
test1 = tb.Label(DB_Scrolled_frame,bootstyle="warning")
test1.pack()
'''

#submit buttons

submit_button = tb.Button(DB_Scrolled_frame,text="Submit",bootstyle="success outline",command=DB_work.submit)
submit_button.pack(pady=20)

#separator

my_sep = tb.Separator(DB_Scrolled_frame,bootstyle="light",orient="horizontal")
my_sep.pack(fill="x",padx=40)

#Data visualization section
DV_title_label = tb.Label(DB_Scrolled_frame,text="Visualize your Expense",font=("Helvertica",22))
DV_title_label.pack(pady=20)

From_date = tb.Label(DB_Scrolled_frame,text="From :",font=("Helvertica", 18))
From_date.pack(pady=10)

From_date_entry = tb.DateEntry(DB_Scrolled_frame,firstweekday=6,bootstyle="warning")
From_date_entry.pack(pady=10)


to_date = tb.Label(DB_Scrolled_frame,text="To :",font=("Helvertica", 18))
to_date.pack(pady=10)

to_date_entry = tb.DateEntry(DB_Scrolled_frame,firstweekday=6,bootstyle="warning")
to_date_entry.pack(pady=10)

DV_submit_btn = tb.Button(DB_Scrolled_frame,text="View Data",bootstyle = "success")
DV_submit_btn.pack(pady=20)

#******************************************************************************************************************************#

#CSV_Frame Section

upload_csv_btn = tb.Button(CSV_frame,bootstyle="reverse light",text="Upload CSV",command=upload_csv)
upload_csv_btn.pack(pady=20)

#****************************************************************************************************************************#
#XL_Frame Section

export_xl_btn = tb.Button(XL_frame,bootstyle="success outline",text="Export Excel")
export_xl_btn.pack(pady=20)

#*****************************************************************************************************************************#
#add frame to notebook
note_book.add(DB_frame,text="Database")
note_book.add(CSV_frame,text="Upload Csv")
note_book.add(XL_frame,text="Export Excel")

root.mainloop()