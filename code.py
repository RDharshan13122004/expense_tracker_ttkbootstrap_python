
from tkinter import *
from tkinter import filedialog
#from tkinter import font
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
import sqlite3
import csv
import numpy as np
import matplotlib.pyplot as plt
import datetime

root = tb.Window(title="Expense Tracker",
                 themename="superhero",
                 iconphoto="C:/Users/dharshan/Desktop/lang and tools/pyvsc/exp_tracker/image/84b81735b361bd85ac4cfef337c88308-removebg-preview.png",
                 size=(600,600))

#classes

class DB_work:

    def __init__(self):
        conn = sqlite3.connect("C:/Users/dharshan/Desktop/lang and tools/pyvsc/exp_tracker/exptracker.db")
        query = conn.cursor()

        query.execute("""create table IF NOT EXISTS DATA(
                      entry_date Date PRIMARY KEY,
                      addional_income REAL,
                      travel REAL,
                      food REAL,
                      regular_expense REAL
                      )""")
        
        query.execute("""create table IF NOT EXISTS Income_expenditure(
                      ITEMs TEXT PRIMARY KEY,
                      Inc_exp TEXT
                      )""")
        conn.commit()

        conn.close()

    @classmethod
    def new_section_of_label(cls):

        # Create a new frame inside the same main frame to hold the new row
        new_set_frame = tb.Frame(main_ex_frame)
        new_set_frame.pack(fill="x", pady=5)
        
        # Add 1st entry in the new row frame
        Exp_amount_entry2 = tb.Entry(new_set_frame,bootstyle="success")
        Exp_amount_entry2.pack(pady=10,side="left",padx=5)

        #creating expenditure category combobox

        items = ["addional income","travel","food","regular expense"]

        # Add 2nd entry in the new row frame, on the same line
        category_combobox2 = tb.Combobox(new_set_frame,bootstyle="success",values=items)
        category_combobox2.pack(side="left",pady=10,padx=5)

        category_combobox2.current(0)


#functions

def select_theme(x):
    root.style.theme_use(x)

def ck_combo_ex():
    '''
    if category_combobox.get() in items:
        print("yess")
    else:
        print("no")
    '''
    
    #test1.config(text=f"{Date_Entry.entry.get()}")

def upload_csv():
    CSV_frame.filename = filedialog.askopenfilename(initialdir="C:/users/",title="CSV files",filetypes=[("csv files","*csv")])
    if CSV_frame.filename:  # Check if a file was selected
        # Now you can handle the CSV file as needed
        with open(CSV_frame.filename, newline='') as csvfile:
            # Process the CSV content here, e.g., using the csv module
            reader = csv.reader(csvfile)
            for row in reader:
                print(row)  # Example: Print each row in the CSV file
    

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


#defualt labels and entry

Date_label = tb.Label(DB_Scrolled_frame,text="Date:",font=('Helvertica',18))
Date_label.pack(pady=10)

Date_Entry = tb.DateEntry(DB_Scrolled_frame,firstweekday=6,bootstyle="info")
Date_Entry.pack()

Salary_label = tb.Label(DB_Scrolled_frame,text="Salary:",font=('Helvertica',18))
Salary_label.pack(pady=10)

salary_Entry = tb.Entry(DB_Scrolled_frame)
salary_Entry.pack(pady=10,ipadx=16)

#income and expenditure labels,Entry,combobutton

#creating expenditure category label
category_label = tb.Label(DB_Scrolled_frame,text= "Enter the amount and set the category:",font=("Helvertica",18))
category_label.pack(pady=20)

#creating a main frame to hold multiple frames 
main_ex_frame = tb.Frame(DB_Scrolled_frame)
main_ex_frame.pack(pady=20)

#1st frame in main frame and setting a frame to bring the amount entry and category menubutton on a same line
set_frame = tb.Frame(main_ex_frame)
set_frame.pack(fill="x", pady=5)

#placing a amount entry with  category menubutton

Exp_amount_entry = tb.Entry(set_frame,bootstyle="success")
Exp_amount_entry.pack(pady=10,side="left",padx=5)

#creating expenditure category combobox

items = ["addional income","travel","food","regular expense"]

category_combobox = tb.Combobox(set_frame,bootstyle="success",values=items)
category_combobox.pack(side="left",pady=10,padx=5)

category_combobox.current(0)

#add button to insert multiple income and expenditure labels,Entry,combobox

exp_add_button = tb.Button(DB_Scrolled_frame,text="+",bootstyle = "info",command=DB_work.new_section_of_label)
exp_add_button.pack()

'''
test1 = tb.Label(DB_Scrolled_frame,bootstyle="warning")
test1.pack()
'''
#intk = DB_work()

#submit buttons

submit_button = tb.Button(DB_Scrolled_frame,text="Submit",bootstyle="success outline",command=ck_combo_ex)
submit_button.pack(pady=20)

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