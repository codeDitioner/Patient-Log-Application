#   Application: Patient Visit Logs                       #
#   Date: May, 2022                                       #
#   Author: Kevin Nguyen                                  #

# import libraries
from tkinter import *
# import message boxes
import tkinter.messagebox as messagebox
# import Treeview
import tkinter.ttk as ttk
# import database from python file CRUDdatabase
from CRUDdatabase import Database

# define path variable
path="C:/Users/User/Desktop/Patient-Log-Application/"
# create an object of Database class from the database python file
db = Database(path+"Patients.db")

# create a window
root = Tk()
# add title to window
root.title("Patient Visit Logs")
# size application window
root.geometry("1000x800")

# define functions to be used in button commands
def add_patient():
    """Add new patient data to treeview list."""
    # double check that all fields have an input
    boolean = entry_confirm()
    # if there are missing entries, then do not continue
    if boolean == False:
        return
    # insert patient information into database
    db.insert(entryPatientNumber.get(), entryDateOfVisit.get(), entryFirstName.get(), entryLastName.get(), entryBirthday.get(), entryPhone.get(), entryComplaint.get())
    # clear entry boxes for new input
    clear_patient()
    # load latest data from database
    load_data()

def remove_patient():
    """Remove patient from treeview list."""
    if entryPatientNumber.get()=='':
        messagebox.showinfo('Warning', "Please select a record to delete.")
        return
    box = messagebox.askquestion('Warning', "Do you want to delete this record?", icon='warning')
    if box =='yes':
        db.remove(entryPatientNumber.get())
        clear_patient()
    # load latest data from database
    load_data()

def update_patient():
    """Update patient information from treeview list."""
    # double check that all required fields have an input
    boolean = entry_confirm()
    # if there are missing entries, then do not continue
    if boolean == False:
        return
    # update database with new patient information
    db.update(entryPatientNumber.get(), entryDateOfVisit.get(), entryFirstName.get(), entryLastName.get(), entryBirthday.get(), entryPhone.get(), entryComplaint.get())
    # clear entry boxes for new input
    clear_patient()
    # load latest data from database
    load_data()

def clear_patient():
    """Clear all entry boxes and clear selected treeview on the bottom of application."""
    entryPatientNumber.delete(0, END)
    entryDateOfVisit.delete(0, END)
    entryFirstName.delete(0, END)
    entryLastName.delete(0, END)
    entryBirthday.delete(0, END)
    entryPhone.delete(0, END)
    entryComplaint.delete(0, END)
    # clear the treeview that shows selected information
    for row in selectedTreeview.get_children():
        selectedTreeview.delete(row)

def load_data():
    """Clear the treeview and fetch the latest data from the database."""
    for row in appTreeview.get_children():
        appTreeview.delete(row)
    # load each row column by column into the treeview
    for column in db.fetch():
        PatientNo = column[1]
        DateOfVisit = column[2]
        FirstName = column[3]
        LastName = column[4]
        Birthday = column[5]
        PhoneNo = column[6]
        Complaint = column[7]
        # '' is the parent to be master, 'end' is the index, text, values
        appTreeview.insert('','end',text=PatientNo, value=(PatientNo, DateOfVisit, FirstName, LastName, Birthday, PhoneNo, Complaint))

def exit_program():
    """Exits program."""
    box = messagebox.askquestion('Exit', 'Do you want to exit the program?', icon='warning')
    if box =='yes':
        # closes the program
        root.destroy()

def entry_confirm():
    """Confirms that entry boxes has valid inputs."""
    # if entry box is blank, show warning and return False
    if entryPatientNumber.get() =='' or entryPatientNumber.get().isnumeric == False:
        messagebox.showinfo('Warning', "Please enter a valid patient number.")
        return False
    if entryDateOfVisit.get()=='':
        messagebox.showinfo('Warning', "Please enter a date of visit.")
        return False
    if entryFirstName.get()=='' or entryFirstName.get().isalpha == False:
        messagebox.showinfo('Warning', "Please enter a valid first name.")
        return False
    if entryLastName.get()=='' or entryLastName.get().isalpha == False:
        messagebox.showinfo('Warning', "Please enter a valid last name.")
        return False
    if entryBirthday.get()=='':
        messagebox.showinfo('Warning', "Please enter a birthday.")
        return False
    if entryPhone.get()=='':
        messagebox.showinfo('Warning', "Please enter a phone number.")
        return False
    if entryComplaint.get()=='':
        messagebox.showinfo('Warning', "Please enter a complaint or reason for visit.")
        return False

def selection_event():
    """Show selected patient on bottom treeview."""
    # clear treeview
    clear_patient()
    # repopulate treeview and show selected items in entry boxes
    for choose in appTreeview.selection():
        item = appTreeview.item(choose)
        # assigns values to variables from tuple items
        PatientNo, DateOfVisit, FirstName, LastName, Birthday, PhoneNo, Complaint = item["values"][0:7]
        # start at index 0 and inserts value into each entry box
        entryPatientNumber.insert(0, PatientNo)
        entryDateOfVisit.insert(0, DateOfVisit)
        entryFirstName.insert(0, FirstName)
        entryLastName.insert(0, LastName)
        entryBirthday.insert(0, Birthday)
        entryPhone.insert(0, PhoneNo)
        entryComplaint.insert(0, Complaint)
        # clear and insert selected items into selected treeview window
        for row in selectedTreeview.get_children():
            selectedTreeview.delete(row)
        selectedTreeview.insert('','end',text=PatientNo, value=(PatientNo, DateOfVisit, FirstName, LastName, Birthday, PhoneNo, Complaint))

# create entry box widgets
entryPatientNumber=Entry(root)
entryDateOfVisit=Entry(root)
entryFirstName=Entry(root)
entryLastName=Entry(root)
entryBirthday=Entry(root)
entryPhone=Entry(root)
entryComplaint=Entry(root)

# create labels for GUI
labelAppTitle = Label(root, text="Patient Visit Log", font=("Arial", 16))
labelSelectedTitle = Label(root, text="Selected Patient Entry", font=("Arial", 12))
labelSelectPrompt = Label(root, text="Please select a patient entry above or input new patient information below.", font=("Arial", 10))

# labels for entry
labelPatientNumber=Label(root, text="Patient No.:", font=("Arial",10))
labelDateOfVisit=Label(root, text="Date of Visit:", font=("Arial", 10))
labelFirstName=Label(root, text="First Name:", font=("Arial", 10))
labelLastName=Label(root, text="Last Name:", font=("Arial", 10))
labelBirthday=Label(root, text="Birthday:", font=("Arial",10))
labelPhone=Label(root, text="Phone:", font=("Arial", 10))
labelComplaint=Label(root, text="Patient Complaint:", font=("Arial", 10))

# create button widgets and assign commands to each button
buttonAdd=Button(root, text="Add Patient", font=("Arial", 10), command=add_patient)
buttonRemove=Button(root, text="Remove Patient", font=("Arial", 10), command=remove_patient)
buttonUpdate=Button(root, text="Update", font=("Arial", 10), command=update_patient)
buttonClear=Button(root, text="Clear", font=("Arial", 10), command=clear_patient)
buttonExit=Button(root, text="Exit", font=("Arial", 10), command=exit_program)

# place labels on GUI
labelAppTitle.place(x=375, y=5, height=50, width = 250)
labelSelectedTitle.place(x=375, y=600, height=50, width=250)
labelSelectPrompt.place(x=250, y=362, height=25, width=500)
labelPatientNumber.place(x=50, y=400, height=23, width=80)
labelDateOfVisit.place(x=50, y=400+30, height=23, width=80)
labelFirstName.place(x=50, y=400+60, height=23, width=80)
labelLastName.place(x=50, y=400+90, height=23, width=80)
labelBirthday.place(x=420, y=400, height=23, width=80)
labelPhone.place(x=425, y=400+30, height=23, width=80)
labelComplaint.place(x=378, y=400+60, height=23, width=110)

# place entry boxes on GUI
entryPatientNumber.place(x=150, y=400, height=23, width=150)
entryDateOfVisit.place(x=150, y=400+30, height=23, width=150)
entryFirstName.place(x=150, y=400+60, height=23, width=150)
entryLastName.place(x=150, y=400+90, height=23, width=150)
entryBirthday.place(x=520, y=400, height=23, width=150)
entryPhone.place(x=520, y=400+30, height=23, width=150)
entryComplaint.place(x=520, y=400+60, height=23, width=400)

# place buttons on GUI
buttonAdd.place(x=200, y=550, height=30, width=110)
buttonRemove.place(x=200+120, y=550, height=30, width=110)
buttonUpdate.place(x=200+240, y=550, height=30, width=110)
buttonClear.place(x=200+360, y=550, height=30, width=110)
buttonExit.place(x=200+480, y=550, height=30, width=110)

# create treeview to be used in root
# main treeview showing all patient logs
appTreeview=ttk.Treeview(root)
# treeview to show currently selected patient log
selectedTreeview=ttk.Treeview(root)

# create treeview columns
appTreeview['columns']=("Column 2", "Column 3", "Column 4", "Column 5", "Column 6", "Column 7", "Column 8")
selectedTreeview['columns']=("Column 2", "Column 3", "Column 4", "Column 5", "Column 6", "Column 7", "Column 8")

# format treeview columns
# main treeview
appTreeview.column("#0", width=0, minwidth=0)
appTreeview.column("Column 2", width=30, minwidth=30, stretch=True)
appTreeview.column("Column 3", width=50, minwidth=50, stretch=True)
appTreeview.column("Column 4", width=50, minwidth=50, stretch=True)
appTreeview.column("Column 5", width=30, minwidth=30, stretch=True)
appTreeview.column("Column 6", width=30, minwidth=30, stretch=True)
appTreeview.column("Column 7", width=50, minwidth=50, stretch=True)
appTreeview.column("Column 8", width=150, minwidth=150, stretch=True)

# selected patient log treeview
selectedTreeview.column("#0", width=0, minwidth=0)
selectedTreeview.column("Column 2", width=30, minwidth=30, stretch=True)
selectedTreeview.column("Column 3", width=50, minwidth=50, stretch=True)
selectedTreeview.column("Column 4", width=50, minwidth=50, stretch=True)
selectedTreeview.column("Column 5", width=30, minwidth=30, stretch=True)
selectedTreeview.column("Column 6", width=30, minwidth=30, stretch=True)
selectedTreeview.column("Column 7", width=50, minwidth=50, stretch=True)
selectedTreeview.column("Column 8", width=150, minwidth=150, stretch=True)

# add headings to treeview columns
# main treeview
appTreeview.heading("Column 2", text="Patient No.", anchor=W)
appTreeview.heading("Column 3", text="Date of Visit", anchor=W)
appTreeview.heading("Column 4", text="First Name", anchor=W)
appTreeview.heading("Column 5", text="Last Name", anchor=W)
appTreeview.heading("Column 6", text="Birthday", anchor=W)
appTreeview.heading("Column 7", text="Phone No.", anchor=W)
appTreeview.heading("Column 8", text="Patient Complaint", anchor=W)

# elected patient log treeview
selectedTreeview.heading("Column 2", text="Patient No.", anchor=W)
selectedTreeview.heading("Column 3", text="Date of Visit", anchor=W)
selectedTreeview.heading("Column 4", text="First Name", anchor=W)
selectedTreeview.heading("Column 5", text="Last Name", anchor=W)
selectedTreeview.heading("Column 6", text="Birthday", anchor=W)
selectedTreeview.heading("Column 7", text="Phone No.", anchor=W)
selectedTreeview.heading("Column 8", text="Patient Complaint", anchor=W)

# do not show identifier column on treeview
appTreeview['show']='headings'
selectedTreeview['show']='headings'

# create scrollbars for main treeview
# vertical scroll bar
verticalSB = ttk.Scrollbar(root, orient=VERTICAL, command=appTreeview.yview)
verticalSB.place(x=950, y=50, height=300)
# configure treeview to use vertical scrollbar
appTreeview.configure(yscroll=verticalSB.set)

# horizontal scrollbar
horizontalSB = ttk.Scrollbar(root, orient=HORIZONTAL, command=appTreeview.xview)
horizontalSB.place(x=50, y=350, width=900)
# configure treeview to use horizontal scrollbar
appTreeview.configure(xscroll=horizontalSB.set)

# placement of treeview
appTreeview.place(x=50, y=50, width=900, height=300)
selectedTreeview.place(x=50, y=650, width=900, height=50)

# selection in treeview populates entry boxes and selection treeview
appTreeview.bind("<<TreeviewSelect>>", selection_event)

# load data at program startup
load_data()

# call the mainloop
root.mainloop()
