import csv
import datetime
import json
import os
import sys
from functools import partial
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

import gridfs
import pymongo
from PIL import ImageTk
from bson.binary import Binary
from bson.objectid import ObjectId
from pymongo import MongoClient

database_path="mongodb://localhost:27017/"

def database(db, col, thequery):
    try:
        theclient = pymongo.MongoClient(database_path)
        thedb = theclient[str(db)]
        thecol = thedb[str(col)]
        thedoc = thecol.find(thequery)
        return thedoc
    except Exception:
        pass


def database_update(db, col, myquery, newval):
    try:
        myclient = pymongo.MongoClient(database_path)
        mydb = myclient[str(db)]
        mycol = mydb[str(col)]
        mycol.update_one(myquery, newval)
        return True
    except Exception:
        return False


def identityDownloader(_id):
    mydoc = list(database("CLASS", "class", {"admin": _id}))
    temp = mydoc[0]['members']
    for i in temp:
        mydoc = list(database("Users", "users", {"_id": str(i)}))
        setinfo(mydoc[0])


def setinfo(LIST):
    with open('membersData.csv', mode='a') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        data = []
        data = [LIST['name'],
                LIST['email'],
                LIST['phone_no'],
                LIST['blood_group'],
                LIST['religion'],
                LIST['gender'],
                LIST['university'],
                LIST['dept'],
                LIST['series'],
                LIST['roll'],
                LIST['section'],
                LIST['college'],
                LIST['college_city'],
                LIST['school'],
                LIST['school_city'],
                LIST['permenent_address'],
                LIST['permanent_address_district'],
                LIST['present_address'],
                LIST['present_address_district'],

                ]

        employee_writer.writerow(data)


def getImage(filename):
    try:
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = "icons/" + str(filename)
        abs_file_path = os.path.join(script_dir, rel_path)
        img = ImageTk.PhotoImage(Image.open(abs_file_path))

        return img
    except Exception as ex:
        print(ex)


class LoginInfo:
    def setinfo(self, email, password):
        data = {}
        data['user'] = []
        data['user'].append({
            'email': str(email),
            'pass': str(password),
        })

        with open('logininfo.json', 'w') as logininfo:
            json.dump(data, logininfo)
        logininfo.close()

    def getid(self):
        with open('logininfo.json') as json_file:
            data = json.load(json_file)
        json_file.close()
        return data['user'][0]['email']


class Login:
    def __init__(self, root):
        root.geometry("400x378")
        master_frame = Frame(root, bg="#FAFAFA")
        master_frame.place(height=378, width=400)

        email_frame = Frame(master_frame, bg="#FAFAFA")
        email_frame.place(height=38, width=320, y=57.5, x=34)

        email_label = Label(email_frame, text="Email", font=("Helvetica 9 italic", 9, "bold"), borderwidth=2,
                            relief="raised")
        email_label.place(height=36, width=62, y=1, x=5)

        entryText = StringVar()
        email_entry = Entry(email_frame, textvariable=entryText)
        email_entry.place(height=36, width=246, y=1, x=69)

        password_frame = Frame(master_frame, bg="#FAFAFA")
        password_frame.place(height=38, width=320, y=105.5, x=34)

        password_label = Label(password_frame, text="Password", font=("Helvetica 9 italic", 8, "bold"), borderwidth=2,
                               relief="raised")
        password_label.place(height=36, width=62, y=1, x=5)

        entryText = StringVar()
        password_entry = Entry(password_frame, textvariable=entryText, show='*')
        password_entry.place(height=36, width=246, y=1, x=69)

        submit_btn_frame = Frame(master_frame, bg="#FAFAFA")
        submit_btn_frame.place(height=30, width=320, y=153.5, x=34)
        login_btn = Button(submit_btn_frame, text='Login', font=("Helvetica 9 italic", 10, "bold"), bg="#3897F0",
                           fg='#FAFAFA', command=partial(self.login, root, master_frame, email_entry, password_entry))
        login_btn.place(height=28, width=310, y=1, x=5)

        register_label = Label(master_frame, text="Don't have an account?")
        register_label.place(height=18, width=310, y=193.5, x=40)
        register_button = Button(master_frame, text="Register", bg="#3897F0",
                                 command=partial(self.register, root, master_frame))
        register_button.place(height=19, width=45, y=214, x=160)

    def login(self, root, master_frame, email_entry, password_entry):
        global EMAIL
        global PASSWORD
        EMAIL = email_entry.get()
        PASSWORD = password_entry.get()

        try:
            login_doc = list(database("Users", "users", {"_id": EMAIL, "pass": PASSWORD}))
        except Exception:
            exit()
        if login_doc:
            LoginInfo().setinfo(EMAIL, PASSWORD)
            master_frame.destroy()
            Profile(root)
        else:
            email_entry.delete(0, 'end')
            password_entry.delete(0, 'end')

    def register(self, root, master_frame):
        master_frame.destroy()
        Register(root)


class Register:
    def __init__(self, root):
        self.root = root
        self.root.geometry("981x600")
        self.register_frame = Frame(self.root, bg="#FAFAFA")
        self.register_frame.place(width=981, height=600)

        # frame
        self.heading_frame = Frame(self.register_frame, bg="#385838")
        self.heading_frame.place(width=981, height=30, x=0, y=0)
        # label
        self.heading_label = Label(self.register_frame, text="Registration Form", bg="#385828", fg="#FAFAFA")
        self.heading_label.place(width=977, height=28, x=2, y=1)

        # frame
        self.personal_info_frame = Frame(self.register_frame, bg="#EFF6F0")
        self.personal_info_frame.place(width=981, height=200, x=0, y=30)

        # label
        self.name_label = Label(self.personal_info_frame, text="Name", bg="#3897F0", fg="#FAFAFA")
        self.name_label.place(width=92, height=22, x=2, y=1)
        # entry
        self.name_entry = Entry(self.personal_info_frame)
        self.name_entry.place(width=200, height=22, x=96, y=1)
        # label
        self.email_label = Label(self.personal_info_frame, text="Email", bg="#3897F0", fg="#FAFAFA")
        self.email_label.place(width=92, height=22, x=2, y=25)
        # entry
        self.email_entry = Entry(self.personal_info_frame)
        self.email_entry.place(width=200, height=22, x=96, y=25)
        # label
        self.pass_label = Label(self.personal_info_frame, text="Password", bg="#3897F0", fg="#FAFAFA")
        self.pass_label.place(width=92, height=22, x=2, y=50)
        # entry
        self.pass_entry = Entry(self.personal_info_frame, show='*')
        self.pass_entry.place(width=200, height=22, x=96, y=50)
        # label
        self.conf_pass_label = Label(self.personal_info_frame, text="Confirm Password", bg="#3897F0", fg="#FAFAFA")
        self.conf_pass_label.place(width=100, height=22, x=310, y=50)
        # entry
        self.conf_pass_entry = Entry(self.personal_info_frame, show='*')
        self.conf_pass_entry.place(width=200, height=22, x=412, y=50)
        # label
        self.phone_no_label = Label(self.personal_info_frame, text="Phone No.", bg="#3897F0", fg="#FAFAFA")
        self.phone_no_label.place(width=92, height=22, x=2, y=75)
        # entry
        self.phone_no_entry = Entry(self.personal_info_frame)
        self.phone_no_entry.place(width=200, height=22, x=96, y=75)
        # label
        self.blood_group_label = Label(self.personal_info_frame, text="Blood group", bg="#3897F0", fg="#FAFAFA")
        self.blood_group_label.place(width=92, height=22, x=2, y=100)
        # entry
        self.blood_group_entry = Entry(self.personal_info_frame)
        self.blood_group_entry.place(width=200, height=22, x=96, y=100)
        # label
        self.religion_label = Label(self.personal_info_frame, text="Religion", bg="#3897F0", fg="#FAFAFA")
        self.religion_label.place(width=92, height=22, x=2, y=125)
        # entry
        self.religion_entry = Entry(self.personal_info_frame)
        self.religion_entry.place(width=200, height=22, x=96, y=125)
        # label
        self.gender_label = Label(self.personal_info_frame, text="Gender", bg="#3897F0", fg="#FAFAFA")
        self.gender_label.place(width=92, height=22, x=2, y=150)
        # radio button
        self.gender_var = StringVar()
        self.gender_radiobtn_male = Radiobutton(self.personal_info_frame, text="male", variable=self.gender_var,
                                                value="male")
        self.gender_radiobtn_male.place(width=92, height=22, x=96, y=150)
        self.gender_radiobtn_female = Radiobutton(self.personal_info_frame, text="female", variable=self.gender_var,
                                                  value="female")
        self.gender_radiobtn_female.place(width=92, height=22, x=204, y=150)

        # frame
        self.institute_info_frame = Frame(self.register_frame, bg="#EFF6F5")
        self.institute_info_frame.place(width=981, height=150, x=0, y=240)

        # label
        self.university_label = Label(self.institute_info_frame, text="University", bg="#3897E0", fg="#FAFAFA")
        self.university_label.place(width=92, height=22, x=2, y=1)
        # entry
        self.university_entry = Entry(self.institute_info_frame)
        self.university_entry.place(width=300, height=22, x=96, y=1)

        # label
        self.dept_label = Label(self.institute_info_frame, text="Department", bg="#3897E0", fg="#FAFAFA")
        self.dept_label.place(width=92, height=22, x=2, y=25)
        # entry
        self.dept_entry = Entry(self.institute_info_frame)
        self.dept_entry.place(width=200, height=22, x=96, y=25)

        # label
        self.series_label = Label(self.institute_info_frame, text="Series", bg="#3897E0", fg="#FAFAFA")
        self.series_label.place(width=92, height=22, x=300, y=25)
        # entry
        self.series_entry = Entry(self.institute_info_frame)
        self.series_entry.place(width=200, height=22, x=394, y=25)

        # label
        self.roll_label = Label(self.institute_info_frame, text="Roll", bg="#3897E0", fg="#FAFAFA")
        self.roll_label.place(width=92, height=22, x=598, y=25)
        # entry
        self.roll_entry = Entry(self.institute_info_frame)
        self.roll_entry.place(width=200, height=22, x=692, y=25)

        # label
        self.section_label = Label(self.institute_info_frame, text="Section", bg="#3897E0", fg="#FAFAFA")
        self.section_label.place(width=92, height=22, x=2, y=50)
        # entry
        self.section_entry = Entry(self.institute_info_frame)
        self.section_entry.place(width=200, height=22, x=96, y=50)

        # label
        self.college_label = Label(self.institute_info_frame, text="College", bg="#3897E0", fg="#FAFAFA")
        self.college_label.place(width=92, height=22, x=2, y=100)
        # entry
        self.college_entry = Entry(self.institute_info_frame)
        self.college_entry.place(width=300, height=22, x=96, y=100)

        # label
        self.college_city_label = Label(self.institute_info_frame, text="City", bg="#3897E0", fg="#FAFAFA")
        self.college_city_label.place(width=92, height=22, x=410, y=100)
        # entry
        self.college_city_entry = Entry(self.institute_info_frame)
        self.college_city_entry.place(width=200, height=22, x=504, y=100)

        # label
        self.school_label = Label(self.institute_info_frame, text="School", bg="#3897E0", fg="#FAFAFA")
        self.school_label.place(width=92, height=22, x=2, y=125)
        # entry
        self.school_entry = Entry(self.institute_info_frame)
        self.school_entry.place(width=300, height=22, x=96, y=125)

        # label
        self.school_city_label = Label(self.institute_info_frame, text="City", bg="#3897E0", fg="#FAFAFA")
        self.school_city_label.place(width=92, height=22, x=410, y=125)
        # entry
        self.school_city_entry = Entry(self.institute_info_frame)
        self.school_city_entry.place(width=200, height=22, x=504, y=125)

        # frame
        self.address_info_frame = Frame(self.register_frame, bg="#EFF6F5")
        self.address_info_frame.place(width=981, height=150, x=0, y=400)

        # label
        self.address_heading_label = Label(self.address_info_frame, text="Permanent Adress", bg="#E95C28", fg="#FAFAFA")
        self.address_heading_label.place(width=200, height=22, x=2, y=3)

        # label
        self.permenent_address_label = Label(self.address_info_frame, text="Adress", bg="#3987E0", fg="#FAFAFA")
        self.permenent_address_label.place(width=200, height=22, x=2, y=29)
        # entry
        self.permenent_address_entry = Entry(self.address_info_frame)
        self.permenent_address_entry.place(width=400, height=22, x=204, y=29)

        # label
        self.permanent_address_district_label = Label(self.address_info_frame, text="District", bg="#3897E0",
                                                      fg="#FAFAFA")
        self.permanent_address_district_label.place(width=92, height=22, x=608, y=29)
        # entry
        self.permanent_address_district_entry = Entry(self.address_info_frame)
        self.permanent_address_district_entry.place(width=200, height=22, x=704, y=29)

        # label
        self.address_heading_label = Label(self.address_info_frame, text="Present Adress", bg="#E95C28", fg="#FAFAFA")
        self.address_heading_label.place(width=200, height=22, x=2, y=61)

        # label
        self.present_address_label = Label(self.address_info_frame, text="Adress", bg="#3987E0", fg="#FAFAFA")
        self.present_address_label.place(width=200, height=22, x=2, y=87)
        # entry
        self.present_address_entry = Entry(self.address_info_frame)
        self.present_address_entry.place(width=400, height=22, x=204, y=87)

        # label
        self.present_address_district_label = Label(self.address_info_frame, text="District", bg="#3897E0",
                                                    fg="#FAFAFA")
        self.present_address_district_label.place(width=92, height=22, x=608, y=87)
        # entry
        self.present_address_district_entry = Entry(self.address_info_frame)
        self.present_address_district_entry.place(width=200, height=22, x=704, y=87)

        # frame
        self.footer_frame = Frame(self.register_frame, bg="#385838")
        self.footer_frame.place(width=981, height=40, x=0, y=560)

        # button
        self.back_button = Button(self.footer_frame, text="Back to 'Login page' ", command=self.backtologin)
        self.back_button.place(width=300, height=26, x=671, y=7)

        # button
        self.register_button = Button(self.footer_frame, text="Register", command=self.doregister)
        self.register_button.place(width=300, height=26, x=10, y=7)

    def backtologin(self):
        self.register_frame.destroy()
        self.root.geometry("400x378")
        Login(self.root)

    def doregister(self):
        global EMAIL
        global PASSWORD

        var1 = str(self.name_entry.get())

        var2 = str(self.email_entry.get())
        EMAIL = var2
        var3 = str(self.pass_entry.get())
        var4 = str(self.conf_pass_entry.get())
        if var3 == var4:
            PASSWORD = var3

            var5 = str(self.phone_no_entry.get())
            var6 = str(self.blood_group_entry.get())
            var7 = str(self.religion_entry.get())
            var8 = str(self.gender_var.get())

            var9 = str(self.university_entry.get())
            var10 = str(self.dept_entry.get())
            var11 = str(self.series_entry.get())
            var12 = str(self.roll_entry.get())
            var13 = str(self.section_entry.get())

            var14 = str(self.college_entry.get())
            var15 = str(self.college_city_entry.get())
            var16 = str(self.school_entry.get())
            var17 = str(self.school_city_entry.get())
            var18 = str(self.permenent_address_entry.get())
            var19 = str(self.permanent_address_district_entry.get())
            var20 = str(self.present_address_entry.get())
            var21 = str(self.present_address_district_entry.get())
            mydict = {"_id": var2,
                      "name": var1,
                      "email": EMAIL,
                      "pass": PASSWORD,
                      "phone_no": var5,
                      "blood_group": var6,
                      "religion": var7,
                      "gender": var8,
                      "university": var9,
                      "dept": var10,
                      "series": var11,
                      "roll": var12,
                      "section": var13,
                      "college": var14,
                      "college_city": var15,
                      "school": var16,
                      "school_city": var17,
                      "permenent_address": var18,
                      "permanent_address_district": var19,
                      "present_address": var20,
                      "present_address_district": var21,
                      "created_group": "",
                      "joined_group": ""
                      }
            try:
                myclient = pymongo.MongoClient(database_path)
                mydb = myclient["Users"]
                mycol = mydb["users"]
                mycol.insert_one(mydict)
                self.register_frame.destroy()
                self.root.geometry("400x378")
                Login(self.root)
            except Exception as e:
                print(e)
                messagebox.showinfo("Message","Email Already exist")
        else:
            self.conf_pass_entry.delete(0, 'end')


class Class:
    cr = 1

    def __init__(self, root):
        root.geometry("981x600")
        self.root = root
        self.root.geometry("981x600")
        # frame
        self.class_frame = Frame(root, background="#FAFAFA")
        self.class_frame.place(height=600, width=981)
        # header frame
        self.class_header_frame = Frame(self.class_frame, background="#385838")
        self.class_header_frame.place(x=0, y=0, width=981, height=42)
        # frame
        self.nav_frame = Frame(self.class_header_frame, background="#485830")
        self.nav_frame.place(x=2, y=2, width=987, height=38)
        # button
        self.back_profile_btn = Button(self.nav_frame, text="Profile", bg="#0E1284", fg='#FAFAFA',
                                       command=self.backprofile)
        self.back_profile_btn.place(x=2, y=1, height=36, width=87)

        # class-routine frame
        self.class_routine_frame = Frame(self.class_frame, background="#FBFBFB")
        self.class_routine_frame.place(x=0, y=45, width=981, height=235)
        # class-routine-header-frame
        self.class_routine_header_frame = Frame(self.class_routine_frame, background="#071322")
        self.class_routine_header_frame.place(x=0, y=0, width=981, height=25)
        # routine heading label
        self.class_routine_heading_label = Label(self.class_routine_header_frame, text="ROUTINE", bg="#07134F",
                                                 fg="#FBFBFB")
        self.class_routine_heading_label.place(x=2, y=0, width=800, height=23)
        self.class_Courses_heading_label = Label(self.class_routine_header_frame, text="COURSES", bg="#07136F",
                                                 fg="#FBFBFB")
        self.class_Courses_heading_label.place(x=804, y=0, width=175, height=23)

        # class-routine-footer-main-frame
        self.class_routine_footer_frame = Frame(self.class_routine_frame, background="#FBFBFB")
        self.class_routine_footer_frame.place(x=2, y=30, width=800, height=200)
        # courses-footer-main-frame
        self.courses_footer_frame = Frame(self.class_routine_frame, background="#FBFBFB")
        self.courses_footer_frame.place(x=804, y=30, width=175, height=200)
        # set the term "day\time"
        Label(self.class_routine_footer_frame, text="Day\Time").place(x=0, y=0, width=70, height=30)
        # class-routine-footer-frmae---> period_time_setter frame
        self.period_timesetter_frame = Frame(self.class_routine_footer_frame, background="#FBFBFB")  # bg ch
        self.period_timesetter_frame.place(x=80, y=0, width=720, height=30)
        # set period ( time)
        time_list = ["08:00", "08:50", "09:40", "10:50", "11:40", "12:30", "02:30", "3:20", "04:10"]
        self.period_time_label = []
        for i in range(9):
            self.period_time_label.append(Label(self.period_timesetter_frame, text=time_list[i]))
            self.period_time_label[i].place(x=i * 80, y=0, width=70, height=30)

            # class-routine-footer-frmae---> day-label-setter-column-frame
        self.day_label_setter_column_frame = Frame(self.class_routine_footer_frame, background="#FBFBFB")  # bg ch
        self.day_label_setter_column_frame.place(x=0, y=50, width=80, height=150)

        # set days
        days_list = ["A DAY", "B DAY", "C DAY", "D DAY", "E DAY"]
        self.days_label = []
        for i in range(5):
            self.days_label.append(Label(self.day_label_setter_column_frame, text=days_list[i]))
            self.days_label[i].place(x=0, y=i * 30, width=70, height=25)

            # class-routine-footer-frmae---> time-wise-column_setter frame
        self.timewise_columnsetter_frame = Frame(self.class_routine_footer_frame, background="#FBFBFB")  # bg ch
        self.timewise_columnsetter_frame.place(x=80, y=50, width=720, height=150)
        # set timewise column
        self.column_frame = []
        for i in range(9):
            self.column_frame.append(Frame(self.timewise_columnsetter_frame, background="#FBFBFB"))
            self.column_frame[i].place(x=i * 80, y=0, width=70, height=150)

        self.cr
        if self.cr:
            self.routine()

            # submit button
        self.submit_btn = Button(self.class_frame, text="Create", command=self.createClass)
        self.submit_btn.place(x=2, y=560, width=46, height=35)

    def routine(self):
        self.elements_entry = []
        for i in range(9):
            Lst = []
            for j in range(5):
                Lst.append(Entry(self.column_frame[i]))
                Lst[j].place(x=0, y=j * 30, width=70, height=25)
            self.elements_entry.append(Lst)

    def createClass(self):

        with open('logininfo.json') as logininfo:
            data = json.load(logininfo)
            EMAIL = str(data['user'][0]['email'])
        logininfo.close()
        myclient = pymongo.MongoClient(database_path)
        mydb = myclient["CLASS"]
        mycol = mydb["class"]

        the_routine = []
        raw_courses = []
        for i in range(9):
            Lst = []
            for j in range(5):
                Lst.append(str(self.elements_entry[i][j].get()))
                raw_courses.append(str(self.elements_entry[i][j].get()))
            the_routine.append(Lst)

        # get the name of courses
        courses = list(set(raw_courses))
        # remove empty string
        while ("" in courses):
            courses.remove("")

        mydict = {'admin': EMAIL,
                  'routine': the_routine,
                  'unique_sub': courses,
                  'members': [],
                  'member_request': [],
                  'announcements': [],

                  }
        i = 1
        for x in courses:
            mydict['course' + str(i)] = []
            i = i + 1

        _id = mycol.insert_one(mydict)

        # add the id of created class to admins record
        myclient = pymongo.MongoClient(database_path)
        mydb = myclient["Users"]
        mycol = mydb["users"]
        myquery = {"_id": EMAIL}
        newvalues = {"$set": {"created_group": str(_id.inserted_id)}}
        mycol.update_one(myquery, newvalues)
        newvalues = {"$set": {"joined_group": str(_id.inserted_id)}}
        mycol.update_one(myquery, newvalues)
        self.class_frame.destroy()
        Profile(root)

    def backprofile(self):
        self.root.geometry("400x378")
        self.class_frame.destroy()


class ShowClass:
    joined_group_id = ""
    created_group_id = ""

    def __init__(self, master):

        master.geometry("981x600")
        self.master = master
        # frame
        master_frame = Frame(master, background="#FAFAFA")
        master_frame.place(x=0, y=0, height=600, width=981)

        # header frame
        header_frame = Frame(master_frame, background="#385838")
        header_frame.place(x=0, y=0, width=981, height=42)
        # button
        back_profile_btn = Button(header_frame, text="Profile", font=("Helvetica 9 italic", 9, "bold"),
                                  command=partial(self.backprofile, master_frame))
        back_profile_btn.place(x=2, y=1, height=36, width=87)

        # routine heading label
        Label(master_frame, text="ROUTINE", bg="#07134F", fg="#FBFBFB", font=("Helvetica 9 italic", 9)).place(x=2, y=44,
                                                                                                              width=800,
                                                                                                              height=23)
        # Label(master_frame,text="MATERIALS",bg="#07136F",fg="#FBFBFB",font=("Helvetica 9 italic",9)).place(x=804,y=44,width=175,height=23)

        # class-routine-frame
        routine_frame = Frame(master_frame, background="#FBFBFB")
        routine_frame.place(x=2, y=70, width=800, height=200)

        # show_routine
        self.routine(routine_frame, master_frame)

        Button(master_frame, text="Announcements", bg="#0A0A0A", fg="#FAFAFA", font=("Helvetica 9 italic", 8, "bold"),
               command=partial(self.show_announcement, master_frame)).place(x=804, y=44, width=175, height=23)

        ##########################################################################################################
        # only for Admin
        if self.created_group_id == self.joined_group_id:
            Button(master_frame, text="Members", bg="#0A0A0A", fg="#FAFAFA", font=("Helvetica 9 italic", 8, "bold"),
                   command=partial(self.showmember, master_frame)).place(x=804, y=70, width=175, height=23)
            Button(master_frame, text="Requests", bg="#0A0A0A", fg="#FAFAFA", font=("Helvetica 9 italic", 8, "bold"),
                   command=partial(self.showmemberrequest, master_frame)).place(x=804, y=96, width=175, height=23)
            # Label---> Announcement

            Announcement_label = Label(master_frame, text="Announcement", bg="#3B5998", fg="#FAFAFA")
            Announcement_label.place(x=2, y=275, width=95, height=25)

            # announcement Textbox
            t = Text(master_frame, width=400, height=150)
            t.place(x=2, y=300, width=800, height=250)

            # send button
            b = Button(master_frame, text="send", font=("Helvetica 9 italic", 8, "bold"))
            b['command'] = partial(self.send, b, t)
            b.place(x=755, y=552, width=40, height=26)
        ####################################################### xxx ##################################################

    def show_announcement(self, master_frame):
        frame = Frame(master_frame)
        frame.place(x=804, y=44, width=175, height=555)

        frame1 = Frame(frame)
        frame1.place(x=0, y=0, width=175, height=525)
        frame2 = Frame(frame)
        frame2.place(x=0, y=526, width=175, height=30)
        # back button
        Button(frame2, text="back", command=partial(self.back, frame)).place(x=0, y=1, width=170, height=26)
        # collect messeges
        try:
            cdoc = list(database("CLASS", "class", {"_id": ObjectId(self.joined_group_id)}))
            lst = list(cdoc[0]['announcements'])

            S = Scrollbar(frame1)

            T = Text(frame1, height=4, width=50)

            S.pack(side=RIGHT, fill=Y)
            T.pack(side=LEFT, fill=Y)

            S.config(command=T.yview)
            T.config(yscrollcommand=S.set)

            for i in lst:
                T.insert(END, i)
        except Exception as e:
            print(e)
            pass

    def routine(self, routine_frame, master_frame):
        try:
            # get the routine from database
            EMAIL = LoginInfo().getid()
            userdoc = list(database("Users", "users", {"_id": EMAIL}))
            self.joined_group_id = str(userdoc[0]['joined_group'])
            self.created_group_id = str(userdoc[0]['created_group'])
            joined_group_info = list(database("CLASS", "class", {"_id": ObjectId(self.joined_group_id)}))
        except Exception:
            exit()
        try:

            time_list = ["Day\Time", "08:00", "08:50", "09:40", "10:50", "11:40", "12:30", "02:30", "3:20", "04:10"]
            days_list = ["A DAY", "B DAY", "C DAY", "D DAY", "E DAY"]

            rows, cols = (5, 10)
            # set-days
            for i in range(rows):
                Label(routine_frame, text=days_list[i], bg="#0096F6", fg="#FAFAFA", font=("Helvetica", 9)).place(x=0,
                                                                                                                 y=33 * (
                                                                                                                         i + 1),
                                                                                                                 width=75,
                                                                                                                 height=23)
            # set-time
            for i in range(cols):
                Label(routine_frame, text=time_list[i], bg="#0096F6", fg="#FAFAFA", font=("Helvetica", 9)).place(
                    x=80 * i, y=0, width=75, height=23)

            rows, cols = (5, 9)
            for i in range(cols):
                for j in range(rows):
                    subject = Button(routine_frame, text=str(joined_group_info[0]['routine'][i][j]),
                                     font=("Helvetica", 8, "bold"))
                    subject.place(x=80 * (i + 1), y=33 * (j + 1), width=75, height=23)
                    subject['command'] = partial(UploaderDownloader, master_frame, subject['text'])
                    if subject['text'] == "":
                        subject['state'] = 'disabled'


        except Exception as e:
            print(e)

    def backprofile(self, master_frame):
        master_frame.destroy()
        self.master.geometry("400x378")
        Profile(self.master)

    def back(self, master_frame):
        master_frame.destroy()

    def send(self, b, t):
        b['state'] = "disabled"
        y = """

"""
        z = """


"""
        date = str(datetime.datetime.now().day) + "-" + str(datetime.datetime.now().month) + "-" + str(
            datetime.datetime.now().year) + "  "
        to_send = date + str(datetime.datetime.now().strftime("%I:%M %p")) + y + t.get("1.0", 'end') + z

        try:
            udoc = list(database("Users", "users", {"_id": LoginInfo().getid()}))
            cdoc = list(database("CLASS", "class", {"_id": ObjectId(udoc[0]['joined_group'])}))
            newval = list(cdoc[0]['announcements'])
            newval.insert(0, to_send)
            database_update("CLASS", "class", {"_id": ObjectId(udoc[0]['joined_group'])},
                            {"$set": {"announcements": newval}})
            t.delete("1.0", 'end')
            b['state'] = "normal"
        except Exception as ex:
            print(ex)
            t.delete("1.0", 'end')
            b['state'] = "normal"
            messagebox.showinfo("Error", "sending failed!")

    def addtomember(self, group, memberTOadd, master_frame, member_frame):

        try:

            cinfo = list(database("CLASS", "class", {"_id": ObjectId(group)}))
            temp_list1 = list(cinfo[0]['members'])
            temp_list1.append(str(memberTOadd))
            temp_list2 = list(cinfo[0]['member_request'])
            temp_list2.remove(str(memberTOadd))
            database_update("Users", "users", {"_id": str(memberTOadd)}, {"$set": {'joined_group': str(group)}})
            database_update("CLASS", "class", {"_id": ObjectId(group)}, {"$set": {'members': temp_list1}})
            database_update("CLASS", "class", {"_id": ObjectId(group)}, {"$set": {'member_request': temp_list2}})
            member_frame.destroy()
            self.showmemberrequest(master_frame)

        except Exception as ex:
            pass

    def showmemberrequest(self, master_frame):
        member_frame = Frame(master_frame)
        member_frame.place(x=804, y=44, width=175, height=555)
        # back button
        Button(member_frame, text="back", command=partial(self.back, member_frame)).place(x=2, y=527, width=171,
                                                                                          height=27)
        try:
            EMAIL = LoginInfo().getid()
            userdoc = list(database("Users", "users", {"_id": EMAIL}))
            created_group_id = str(userdoc[0]['created_group'])
            created_group_info = list(database("CLASS", "class", {"_id": ObjectId(created_group_id)}))
        except Exception as e:
            print(e)
            pass
        try:
            canvas = Canvas(member_frame, bg="#EAFAFA", width=175, height=525)
            canvas.place(x=0, y=0, width=175, height=525)

            lst = list(created_group_info[0]['member_request'])
            y = 0

            for i in lst:
                userdoc = list(database("Users", "users", {"_id": str(i)}))
                btn = Button(canvas, text="accept", bg="#00000F", fg="#FAFAFA")
                label = Label(canvas, text=userdoc[0]['name'], fg="#3B5998")
                canvas.create_window(2, y, window=label, anchor=NW, height=26)
                btn['command'] = partial(self.addtomember, created_group_id, userdoc[0]['_id'], master_frame,
                                         member_frame)
                canvas.create_window(2, y + 21, window=btn, anchor=NW, height=20)
                y += 50

            scrollbar = Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)
            scrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
            canvas.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, y))
        except Exception as e:
            print(e)
            pass

    def showmember(self, master_frame):
        member_frame = Frame(master_frame)
        member_frame.place(x=804, y=44, width=175, height=555)
        # back button
        Button(member_frame, text="back", command=partial(self.back, member_frame)).place(x=2, y=527, width=171,
                                                                                          height=27)
        try:
            mydoc = list(database("Users", "users", {"_id": str(LoginInfo().getid())}))
            created_group_id = str(mydoc[0]['created_group'])
            joined_group_id = str(mydoc[0]['joined_group'])

            created_group_info = list(database("CLASS", "class", {"_id": ObjectId(created_group_id)}))
        except Exception as e:
            print(e)
            pass
        try:
            canvas = Canvas(member_frame, bg="#EAFAFA", width=175, height=525)
            canvas.place(x=0, y=0, width=175, height=525)

            lst = list(created_group_info[0]['members'])
            y = 0

            for i in lst:
                mydoc = list(database("Users", "users", {"_id": str(i)}))
                btn = Button(canvas, text=mydoc[0]['name'], bg="#00000F", fg="#FAFAFA")
                # btn['command'] = partial(self.addtomember,created_group_id,mydoc[0]['name'])
                canvas.create_window(1, y, window=btn, anchor=NW, height=26)
                y += 30

            scrollbar = Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)
            scrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
            canvas.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, y))
        except Exception:
            pass


class UploaderDownloader:

    def __init__(self, master_frame, course_name):
        self.course_name = course_name
        self.master_frame = master_frame
        self.updown_frame = Frame(master_frame, background="#FAFAFA")
        self.updown_frame.place(height=600, width=981)

        # header frame
        self.class_header_frame = Frame(self.updown_frame, background="#385838")
        self.class_header_frame.place(x=0, y=0, width=981, height=42)
        # frame
        self.nav_frame = Frame(self.class_header_frame, background="#485830")
        self.nav_frame.place(x=2, y=2, width=977, height=38)
        # back_button
        self.back_btn = Button(self.nav_frame, text="Back", font=("Helvetica", 8, "bold"), command=self.backclass)
        self.back_btn.place(x=2, y=1, height=36, width=87)

        # course_name_label
        Label(self.nav_frame, text=course_name, bg="#0E1284", fg='#FAFAFA', font=("Helvetica", 8, "bold")).place(x=892,
                                                                                                                 y=1,
                                                                                                                 height=36,
                                                                                                                 width=87)

        # upload_button
        self.upload_btn = Button(self.nav_frame, text="Upload", font=("Helvetica", 8, "bold"), command=self.uploadfiles)
        self.upload_btn['command'] = partial(self.uploadfiles, self.upload_btn, self.back_btn)
        self.upload_btn.place(x=327, y=1, height=36, width=87)

        # a frame ( notes for downloading will be set here )

        self.download_frame = Frame(self.updown_frame, background="#485830")
        self.download_frame.place(x=2, y=50, width=977, height=550)

        try:
            EMAIL = LoginInfo().getid()
            mydoc = list(database("Users", "users", {"_id": EMAIL}))
            joined_group_id = str(mydoc[0]['joined_group'])

            joined_group_info = list(database("CLASS", "class", {"_id": ObjectId(joined_group_id)}))
            course_no = 1 + joined_group_info[0]['unique_sub'].index(course_name)

            LIST = joined_group_info[0]['course' + str(course_no)]

            canvas = Canvas(self.download_frame, width=977, height=550)
            canvas.place(x=0, y=0, width=977, height=550)
            y = 0

            for file_id in LIST:
                filedoc = list(database("Files", "fs.files", {"_id": ObjectId(file_id)}))
                btn = Button(self.download_frame, text=filedoc[0]['filename'],
                             command=partial(self.downloadfiles, file_id, filedoc[0]['filename'],
                                             filedoc[0]['contentType']))
                canvas.create_window(2, y, window=btn, anchor=NW)
                y += 36

            scrollbar = Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)
            scrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
            canvas.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, y))

        except Exception:
            pass

    def backclass(self):
        self.updown_frame.destroy()

    def downloadfiles(self, id_of_dnld_file, name_of_dnld_file, type_of_dnld_file):
        try:

            # download_state_label
            messagebox.showinfo("Information", "Downloading")

            myclient = pymongo.MongoClient(database_path)
            mydb = myclient["Files"]
            fs = gridfs.GridFS(mydb)

            path = os.path.dirname(os.path.realpath(sys.argv[0])) + "/downloads/" + str(name_of_dnld_file) + "." + str(
                type_of_dnld_file)

            for grid_out in fs.find({'_id': ObjectId(str(id_of_dnld_file))},
                                    no_cursor_timeout=True):
                data = grid_out.read()

            f = open(path, 'wb')
            f.write(data)
            f.close()
            messagebox.showinfo("Information", "Downloaded")
        except Exception:
            messagebox.showinfo("Information", "Download Failed!")

    def uploadfiles(self, up_btn, back_btn):
        try:
            path = askopenfilename()
        except Exception:
            path = ""
        if path != "":

            try:
                up_btn["state"] = "disabled"
                up_btn["text"] = "Uploading"
                back_btn['state'] = "disabled"
                myclient = pymongo.MongoClient(database_path)
                mydb = myclient["Files"]

                db = MongoClient().myDB
                fs = gridfs.GridFS(mydb)

                with open(path, 'rb') as f:
                    content_type = str(list(path.split("."))[-1])
                    filename = str(list(path.split("."))[-2].split("/")[-1])
                    encoded = Binary(f.read())
                    _id = fs.put(encoded, content_type=content_type, filename=filename)

                EMAIL = LoginInfo().getid()
                mydb = myclient["Users"]
                mycol = mydb["users"]
                myquery = {"_id": EMAIL}
                mydoc = list(mycol.find(myquery))
                joined_group_id = str(mydoc[0]['joined_group'])
                mydb = myclient["CLASS"]
                mycol = mydb["class"]
                joined_group_info = list(mycol.find({"_id": ObjectId(joined_group_id)}))
                course_no = 1 + joined_group_info[0]['unique_sub'].index(self.course_name)
                LIST = joined_group_info[0]['course' + str(course_no)]
                LIST.append(_id)
                myquery = {"_id": ObjectId(joined_group_id)}
                newvalues = {"$set": {'course' + str(course_no): LIST}}
                mycol.update_one(myquery, newvalues)
                self.updown_frame.destroy()
                UploaderDownloader(self.master_frame, self.course_name)
            except Exception as e:
                up_btn["state"] = "disabled"
                up_btn["text"] = "Uploading"
                back_btn['state'] = "normal"
                messagebox.showinfo("Information", "Upload failed!")
                print(e)

        else:
            pass


class Profile:

    def __init__(self, root):
        try:
            self.userdoc = list(database("Users", "users", {'_id': LoginInfo().getid()}))
            self.joined_group_id = self.userdoc[0]['joined_group']
            self.created_group_id = self.userdoc[0]['created_group']
        except Exception:
            pass
        root.geometry("400x378")
        self.root = root
        self.root.geometry("400x378")

        # frame created
        self.Profile_frame = Frame(self.root, background="#FAFAFA")
        self.Profile_frame.place(width=400, height=378)
        # header frame
        header_frame = Frame(self.Profile_frame, background="#385838")
        header_frame.place(x=0, y=0, width=400, height=42)
        # logout button
        Button(header_frame, text="logout", font=("Helvetica 9 italic", 8, "bold"), command=self.logout).place(x=352,
                                                                                                               y=6,
                                                                                                               width=46,
                                                                                                               height=30)

        # src-join frame
        search_join_frame = Frame(self.Profile_frame, background="#FAFAFA")
        search_join_frame.place(x=0, y=44, width=400, height=42)
        # src-entry
        src_entry = Entry(search_join_frame)
        src_entry.place(x=2, y=6, width=348, height=30)
        # src_button
        src_btn = Button(search_join_frame, text="Search", font=("Helvetica 9 italic", 8, "bold"),
                         command=partial(self.search, search_join_frame, src_entry))
        src_btn.place(x=352, y=6, width=46, height=30)
        if self.joined_group_id == "":
            src_btn['state'] = "normal"
        else:
            src_btn['state'] = "disabled"
            # pro-pic-frame
        propic_frame = Frame(self.Profile_frame, background="#F85838")
        propic_frame.place(x=0, y=88, width=200, height=200)

        # about button
        about_btn = Button(self.Profile_frame, text="About", font=("Helvetica 9 italic", 8, "bold"),command=partial(self.show_about))
        about_btn.place(x=306, y=88, width=92, height=30)
        # create_class_button
        create_class_btn = Button(self.Profile_frame, text="Create Class", font=("Helvetica 9 italic", 8, "bold"),
                                  command=self.createclass)
        create_class_btn.place(x=306, y=120, width=92, height=30)
        if self.joined_group_id == "":
            create_class_btn['state'] = "normal"
        else:
            create_class_btn['state'] = "disabled"

            # following frame
        following_frame = Frame(self.Profile_frame, background="#EAFAFA")
        following_frame.place(x=0, y=290, width=400, height=40)
        # following_button
        following_btn = Button(following_frame, text="Following Class", font=("Helvetica 9 italic", 8, "bold"),
                               command=partial(self.showfollowing, following_frame))
        following_btn.place(x=2, y=2, width=396, height=36)

    def show_about(self):
        About(self.root)
    def showfollowing(self, following_frame):
        #######################################################
        try:
            mydoc = list(database("Users", "users", {"_id": LoginInfo().getid()}))
            group_created_id = str(mydoc[0]['created_group'])
            group_joined_id = str(mydoc[0]['joined_group'])
        except Exception as e:
            print(e)
            pass

        try:
            cdoc = list(database("CLASS", "class", {"_id": ObjectId(group_joined_id)}))
            if len(cdoc):  # class exists
                print(cdoc)
                print(len(cdoc))
                try:
                    # frame
                    self.following_class_frame = Frame(following_frame, background="#EAFAFA")
                    self.following_class_frame.place(x=0, y=0, width=400, height=40)
                    # button class _id
                    classid_btn = Button(self.following_class_frame, text=group_joined_id,
                                         command=partial(self.manage_classid, "classid"))
                    classid_btn.place(x=35 + 50, y=2, width=184, height=25)

                    # button "delete" (only for admin)
                    if group_joined_id == group_created_id:
                        classid_delete_btn = Button(self.following_class_frame, text="delete",
                                                    command=partial(self.manage_classid, "delete"))
                        classid_delete_btn.place(x=221 + 100, y=2, width=62, height=25)


                    # button unfollow (class)(only for students)
                    else:
                        classid_unfollow_btn = Button(self.following_class_frame, text="unfollow",
                                                      command=partial(self.manage_classid, "unfollow"))
                        classid_unfollow_btn.place(x=221 + 100, y=2, width=62, height=25)

                    # button back
                    classid_back_btn = Button(self.following_class_frame, text="back",
                                              command=partial(self.manage_classid, "back"))
                    classid_back_btn.place(x=2, y=2, width=31, height=25)
                except Exception as e:
                    print(e)
                    pass

        except Exception:
            pass
        #######################################################

    def manage_classid(self, type):
        if type == "classid":
            self.following_class_frame.destroy()
            ShowClass(root)
        if type == "unfollow":
            ##############################################
            try:
                self.EMAIL = LoginInfo().getid()
                userdoc = list(database("Users", "users", {"_id": self.EMAIL}))
                group_joined_id = str(userdoc[0]['joined_group'])

                mydoc = list(database("CLASS", "class", {"_id": ObjectId(group_joined_id)}))
                L = list(mydoc[0]['members'])
                L.remove(self.EMAIL)
                database_update("CLASS", "class", {"_id": ObjectId(group_joined_id)}, {"$set": {"members": L}})

                database_update("Users", "users", {"_id": self.EMAIL}, {"$set": {"joined_group": ""}})

                self.Profile_frame.destroy()
                Profile(root)

            except Exception as e:
                print(e)
                pass
            #################################################

        if type == "delete":
            ##############################################
            try:

                self.EMAIL = LoginInfo().getid()
                myclient = pymongo.MongoClient(database_path)
                mydb = myclient["Users"]
                mycol = mydb["users"]
                myquery = {"_id": self.EMAIL}
                mydoc = list(mycol.find(myquery))
                group_joined_id = str(mydoc[0]['joined_group'])
                newval = {"$set": {"joined_group": ""}}
                mycol.update_one(myquery, newval)
                newval = {"$set": {"created_group": ""}}
                mycol.update_one(myquery, newval)

                classdoc = list(database("CLASS", "class", {'_id': ObjectId(group_joined_id)}))
                L = list(classdoc[0]['members'])

                for membr in L:
                    database_update("Users", "users", {'_id': membr}, {"$set": {"joined_group": ""}})
                mydb = myclient["CLASS"]
                mycol = mydb["class"]
                myquery = {"_id": ObjectId(group_joined_id)}
                mycol.delete_one(myquery)

                self.Profile_frame.destroy()
                Profile(root)

            except Exception:
                pass
            #################################################
            # self.following_class_frame.destroy()

        if type == "back":
            self.following_class_frame.destroy()

    def search(self, search_join_frame_prev, src_entry):
        try:
            myclient = pymongo.MongoClient(database_path)
            mydb = myclient["CLASS"]
            mycol = mydb["class"]
            self.search_data = ObjectId(src_entry.get())
            data = list(mycol.find({"_id": self.search_data}))
        except Exception as e:
            messagebox.showinfo("Message", "Invalid Class-ID")
        try:
            if data:
                print("checked")
                search_join_frame = Frame(search_join_frame_prev)
                search_join_frame.place(x=0, y=0, width=400, height=42)
                src_result_label = Label(search_join_frame, text=str(data[0]['_id']))
                src_result_label.place(x=2, y=6, width=348, height=30)
                src_result_btn = Button(search_join_frame, text="join", font=("Helvetica 9 italic", 8, "bold"),
                                        command=partial(self.join, search_join_frame, src_entry))
                src_result_btn.place(x=352, y=6, width=46, height=30)
            else:
                messagebox.showinfo("Message", "Invalid Class-ID")
        except Exception as e:
                messagebox.showinfo("Message", "Invalid Class-ID")

    def join(self, search_join_frame, src_entry):

        ##################################################################################
        try:
            self.EMAIL = LoginInfo().getid()
        except Exception:
            pass

        #####################################################################################

        try:
            classclient = pymongo.MongoClient(database_path)
            classdb = classclient["CLASS"]
            classcol = classdb["class"]
            classquery = {"_id": self.search_data}
            classdoc = list(classcol.find(classquery))
            member_request_lst = list(classdoc[0]['member_request'])
            flag = False
            for i in member_request_lst:
                if (i == self.EMAIL):
                    flag = True
                    break
            if flag == False:
                member_request_lst.append(self.EMAIL)
                class_newval = {"$set": {"member_request": member_request_lst}}
                classcol.update_one(classquery, class_newval)

        except Exception:
            pass
        ######################################################################################
        search_join_frame.destroy()
        src_entry.delete(0, 'end')

    def createclass(self):
        Class(self.root)

    def logout(self):
        self.Profile_frame.destroy()
        self.root.geometry("400x378")
        Login(self.root)

    def about(self):
        EMAIL = LoginInfo().getid()
        # frame created
        self.show_about_frame = Frame(self.Profile_frame, background="#F3E9EF")
        self.show_about_frame.place(x=4, y=246, width=384, height=280)

        # database
        myclient = pymongo.MongoClient(database_path)
        mydb = myclient["Users"]
        mycol = mydb["users"]

        myquery = {"_id": EMAIL}
        mydoc = mycol.find(myquery)

        # newvalues={"$set":{"password":"11235"}}
        # ycol.update_one(myquery,newvalues)

        self.label1 = Label(self.show_about_frame, text="Name: " + str(mydoc[0]['name']))
        self.label1.grid(row=1, column=0)
        self.label2 = Label(self.show_about_frame, text="University: " + mydoc[0]['university'])
        self.label2.grid(row=2, column=0)
        self.label3 = Label(self.show_about_frame, text="Roll: " + mydoc[0]['roll'])
        self.label3.grid(row=3, column=0)
        self.label4 = Label(self.show_about_frame, text="Section: " + mydoc[0]['section'])
        self.label4.grid(row=4, column=0)
        self.label4_1 = Label(self.show_about_frame, text="Series: " + mydoc[0]['series'])
        self.label4_1.grid(row=4, column=1)
        self.back_button = Button(self.show_about_frame, text="Back", command=self.back)
        self.back_button.grid(row=5, column=1)

    def back(self):
        self.show_about_frame.destroy()

class About:
    def __init__(self, root):
        try:
            self.userdoc = list(database("Users", "users", {'_id': LoginInfo().getid()}))

        except Exception:
            pass
        self.root = root
        self.root.geometry("981x600")
        self.about_frame = Frame(self.root, bg="#FAFAFA")
        self.about_frame.place(width=981, height=600)

        # frame
        self.heading_frame = Frame(self.about_frame, bg="#385838")
        self.heading_frame.place(width=981, height=30, x=0, y=0)
        # label
        self.heading_label = Label(self.about_frame, text="Registration Form", bg="#385828", fg="#FAFAFA")
        self.heading_label.place(width=977, height=28, x=2, y=1)

        # frame
        self.personal_info_frame = Frame(self.about_frame, bg="#EFF6F0")
        self.personal_info_frame.place(width=981, height=200, x=0, y=30)

        # label
        self.name_label = Label(self.personal_info_frame, text="Name", bg="#3897F0", fg="#FAFAFA")
        self.name_label.place(width=92, height=22, x=2, y=1)
        # entry
        self.name_entry = Label(self.personal_info_frame,text=self.userdoc[0]['name'])
        self.name_entry.place(width=200, height=22, x=96, y=1)
        # label
        self.email_label = Label(self.personal_info_frame, text="Email", bg="#3897F0", fg="#FAFAFA")
        self.email_label.place(width=92, height=22, x=2, y=25)
        # entry
        self.email_entry = Label(self.personal_info_frame,text=self.userdoc[0]['email'])
        self.email_entry.place(width=200, height=22, x=96, y=25)
        # label
        self.phone_no_label = Label(self.personal_info_frame, text="Phone No.", bg="#3897F0", fg="#FAFAFA")
        self.phone_no_label.place(width=92, height=22, x=2, y=75)
        # entry
        self.phone_no_entry = Label(self.personal_info_frame,text=self.userdoc[0]['phone_no'])
        self.phone_no_entry.place(width=200, height=22, x=96, y=75)
        # label
        self.blood_group_label = Label(self.personal_info_frame, text="Blood group", bg="#3897F0", fg="#FAFAFA")
        self.blood_group_label.place(width=92, height=22, x=2, y=100)
        # entry
        self.blood_group_entry = Label(self.personal_info_frame,text=self.userdoc[0]['blood_group'])
        self.blood_group_entry.place(width=200, height=22, x=96, y=100)
        # label
        self.religion_label = Label(self.personal_info_frame, text="Religion", bg="#3897F0", fg="#FAFAFA")
        self.religion_label.place(width=92, height=22, x=2, y=125)
        # entry
        self.religion_entry = Label(self.personal_info_frame,text=self.userdoc[0]['religion'])
        self.religion_entry.place(width=200, height=22, x=96, y=125)
        # label
        self.gender_label = Label(self.personal_info_frame, text="Gender", bg="#3897F0", fg="#FAFAFA")
        self.gender_label.place(width=92, height=22, x=2, y=150)
        # label
        self.gender_entry = Label(self.personal_info_frame, text=self.userdoc[0]['gender'])
        self.gender_entry.place(width=200, height=22, x=96, y=150)

        # frame
        self.institute_info_frame = Frame(self.about_frame, bg="#EFF6F5")
        self.institute_info_frame.place(width=981, height=150, x=0, y=240)

        # label
        self.university_label = Label(self.institute_info_frame, text="University", bg="#3897E0", fg="#FAFAFA")
        self.university_label.place(width=92, height=22, x=2, y=1)
        # entry
        self.university_entry = Label(self.institute_info_frame, text=self.userdoc[0]['university'])
        self.university_entry.place(width=300, height=22, x=96, y=1)

        # label
        self.dept_label = Label(self.institute_info_frame, text="Department", bg="#3897E0", fg="#FAFAFA")
        self.dept_label.place(width=92, height=22, x=2, y=25)
        # entry
        self.dept_entry = Label(self.institute_info_frame, text=self.userdoc[0]['dept'])
        self.dept_entry.place(width=200, height=22, x=96, y=25)

        # label
        self.series_label = Label(self.institute_info_frame, text="Series", bg="#3897E0", fg="#FAFAFA")
        self.series_label.place(width=92, height=22, x=300, y=25)
        # entry
        self.series_entry = Label(self.institute_info_frame, text=self.userdoc[0]['series'])
        self.series_entry.place(width=200, height=22, x=394, y=25)

        # label
        self.roll_label = Label(self.institute_info_frame, text="Roll", bg="#3897E0", fg="#FAFAFA")
        self.roll_label.place(width=92, height=22, x=598, y=25)
        # entry
        self.roll_entry = Label(self.institute_info_frame, text=self.userdoc[0]['roll'])
        self.roll_entry.place(width=200, height=22, x=692, y=25)

        # label
        self.section_label = Label(self.institute_info_frame, text="Section", bg="#3897E0", fg="#FAFAFA")
        self.section_label.place(width=92, height=22, x=2, y=50)
        # entry
        self.section_entry = Label(self.institute_info_frame, text=self.userdoc[0]['section'])
        self.section_entry.place(width=200, height=22, x=96, y=50)

        # label
        self.college_label = Label(self.institute_info_frame, text="College", bg="#3897E0", fg="#FAFAFA")
        self.college_label.place(width=92, height=22, x=2, y=100)
        # entry
        self.college_entry = Label(self.institute_info_frame, text=self.userdoc[0]['college'])
        self.college_entry.place(width=300, height=22, x=96, y=100)

        # label
        self.college_city_label = Label(self.institute_info_frame, text="City", bg="#3897E0", fg="#FAFAFA")
        self.college_city_label.place(width=92, height=22, x=410, y=100)
        # entry
        self.college_city_entry = Label(self.institute_info_frame, text=self.userdoc[0]['college_city'])
        self.college_city_entry.place(width=200, height=22, x=504, y=100)

        # label
        self.school_label = Label(self.institute_info_frame, text="School", bg="#3897E0", fg="#FAFAFA")
        self.school_label.place(width=92, height=22, x=2, y=125)
        # entry
        self.school_entry = Label(self.institute_info_frame, text=self.userdoc[0]['school'])
        self.school_entry.place(width=300, height=22, x=96, y=125)

        # label
        self.school_city_label = Label(self.institute_info_frame, text="City", bg="#3897E0", fg="#FAFAFA")
        self.school_city_label.place(width=92, height=22, x=410, y=125)
        # entry
        self.school_city_entry = Label(self.institute_info_frame, text=self.userdoc[0]['school_city'])
        self.school_city_entry.place(width=200, height=22, x=504, y=125)

        # frame
        self.address_info_frame = Frame(self.about_frame, bg="#EFF6F5")
        self.address_info_frame.place(width=981, height=150, x=0, y=400)

        # label
        self.address_heading_label = Label(self.address_info_frame, text="Permanent Adress", bg="#E95C28", fg="#FAFAFA")
        self.address_heading_label.place(width=200, height=22, x=2, y=3)

        # label
        self.permenent_address_label = Label(self.address_info_frame, text="Adress", bg="#3987E0", fg="#FAFAFA")
        self.permenent_address_label.place(width=200, height=22, x=2, y=29)
        # entry
        self.permenent_address_entry = Label(self.address_info_frame, text=self.userdoc[0]['permenent_address'])
        self.permenent_address_entry.place(width=400, height=22, x=204, y=29)

        # label
        self.permanent_address_district_label = Label(self.address_info_frame, text="District", bg="#3897E0",
                                                      fg="#FAFAFA")
        self.permanent_address_district_label.place(width=92, height=22, x=608, y=29)
        # entry
        self.permanent_address_district_entry = Label(self.address_info_frame, text=self.userdoc[0]['permanent_address_district'])
        self.permanent_address_district_entry.place(width=200, height=22, x=704, y=29)

        # label
        self.address_heading_label = Label(self.address_info_frame, text="Present Adress", bg="#E95C28", fg="#FAFAFA")
        self.address_heading_label.place(width=200, height=22, x=2, y=61)

        # label
        self.present_address_label = Label(self.address_info_frame, text="Adress", bg="#3987E0", fg="#FAFAFA")
        self.present_address_label.place(width=200, height=22, x=2, y=87)
        # entry
        self.present_address_entry = Label(self.address_info_frame, text=self.userdoc[0]['present_address'])
        self.present_address_entry.place(width=400, height=22, x=204, y=87)

        # label
        self.present_address_district_label = Label(self.address_info_frame, text="District", bg="#3897E0",
                                                    fg="#FAFAFA")
        self.present_address_district_label.place(width=92, height=22, x=608, y=87)
        # entry
        self.present_address_district_entry = Label(self.address_info_frame, text=self.userdoc[0]['present_address_district'])
        self.present_address_district_entry.place(width=200, height=22, x=704, y=87)

        # frame
        self.footer_frame = Frame(self.about_frame, bg="#385838")
        self.footer_frame.place(width=981, height=40, x=0, y=560)

        # button
        self.back_button = Button(self.footer_frame, text="Back", command=self.backtoprofile)
        self.back_button.place(width=300, height=26, x=671, y=7)


    def backtoprofile(self):
        self.about_frame.destroy()
        self.root.geometry("400x378")

root = Tk()
root.title("RUETERS")
root.geometry("400x378")
root.wm_iconbitmap(os.path.dirname(os.path.realpath(sys.argv[0])) + "\icons" + '\RUETERS_ICON.ico')
root.resizable(0, 0)
Login(root)
root.mainloop()
