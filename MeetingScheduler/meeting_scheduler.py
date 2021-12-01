import datetime
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar

from database_utils import Utils


class MeetingScheduler:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Meeting Scheduler')
        self.window.resizable(0, 0)
        self.window.geometry('1200x750')
        self.window.configure(bg='#E3F6FF')
        self.buttons_frame = tk.Frame()
        self.buttons_frame.pack(side='left')
        self.add_button = tk.Button(self.buttons_frame, text='Add person', activebackground='#4B93B7',
                                    bg='#64CBFF', padx=10, pady=10,
                                    command=self.add_command)
        self.add_button.grid(row=0, column=0, padx=10, pady=10)
        self.schedule_meeting_button = tk.Button(self.buttons_frame, text='New meeting', activebackground='#4B93B7',
                                                 bg='#64CBFF', padx=10, pady=10,
                                                 command=self.schedule_meeting_command)
        self.schedule_meeting_button.grid(row=2, column=0, padx=10, pady=10)
        self.view_meetings_button = tk.Button(self.buttons_frame, text='View meetings', activebackground='#4B93B7',
                                              bg='#64CBFF', padx=10, pady=10,
                                              command=self.view_meetings_command)
        self.view_meetings_button.grid(row=4, column=0, padx=10, pady=10)
        self.export_button = tk.Button(self.buttons_frame, text='Export', activebackground='#4B93B7',
                                       bg='#64CBFF', padx=10, pady=10,
                                       command=self.export_command)
        self.export_button.grid(row=6, column=0, padx=10, pady=10)
        self.import_button = tk.Button(self.buttons_frame, text='Import', activebackground='#4B93B7',
                                       bg='#64CBFF', padx=10, pady=10,
                                       command=self.import_command)
        self.import_button.grid(row=8, column=0, padx=10, pady=10)
        self.content_frame = None
        self.firstname_entry = None
        self.lastname_entry = None
        self.add_person_to_database_button = None
        self.start_date_calendar = None
        self.end_date_calendar = None
        self.start_hour_variable = None
        self.start_minutes_variable = None
        self.end_hour_variable = None
        self.end_minutes_variable = None
        self.start_hour_frame = None
        self.end_hour_frame = None
        self.new_meeting_button = None
        self.window.mainloop()

    def add_command(self):
        try:
            self.content_frame.destroy()
        except Exception as e:
            print(str(e))
        self.content_frame = tk.Frame(pady=10)
        self.content_frame.pack(side='left')
        tk.Label(self.content_frame, text="Firstname").grid(row=0)
        tk.Label(self.content_frame, text="Lastname").grid(row=1)

        self.firstname_entry = tk.Entry(self.content_frame)
        self.lastname_entry = tk.Entry(self.content_frame)
        self.firstname_entry.grid(row=0, column=1, padx=10)
        self.lastname_entry.grid(row=1, column=1, padx=10)
        self.add_person_to_database_button = tk.Button(self.content_frame, text='Add', activebackground='#4B93B7',
                                                       bg='#64CBFF', padx=10, pady=10,
                                                       command=self.add_person_to_database)
        self.add_person_to_database_button.grid(row=1, column=4, padx=10, pady=10)

    def schedule_meeting_command(self):
        try:
            self.content_frame.destroy()
        except Exception as e:
            print(str(e))
        self.content_frame = tk.Frame(self.window, pady=10)
        self.content_frame.pack(side='left')
        current_date = datetime.datetime.now()
        tk.Label(self.content_frame, text="Start Date").grid(row=0, column=0)
        tk.Label(self.content_frame, text="End Date").grid(row=0, column=3)
        self.start_date_calendar = Calendar(self.content_frame, year=int(current_date.strftime('%Y')),
                                            month=int(current_date.strftime('%m')),
                                            day=int(current_date.strftime('%d')))
        self.start_date_calendar.grid(row=1, column=0, padx=10, pady=10)

        self.end_date_calendar = Calendar(self.content_frame, year=int(current_date.strftime('%Y')),
                                          month=int(current_date.strftime('%m')),
                                          day=int(current_date.strftime('%d')))
        self.end_date_calendar.grid(row=1, column=3, padx=10, pady=10)
        self.start_hour_variable = tk.StringVar()
        self.start_hour_variable.set(current_date.strftime('%H'))
        self.start_minutes_variable = tk.StringVar()
        self.end_hour_variable = tk.StringVar()
        self.end_hour_variable.set(str(int(current_date.strftime('%H')) + 1))
        self.end_minutes_variable = tk.StringVar()
        self.start_hour_frame = tk.Frame(self.content_frame)
        self.start_hour_frame.grid(row=2, column=0)
        self.end_hour_frame = tk.Frame(self.content_frame)
        self.end_hour_frame.grid(row=2, column=3)

        start_hour_spinbox = tk.Spinbox(self.start_hour_frame, from_=0, to=23, wrap=True, width=2, state="readonly",
                                        justify='center', textvariable=self.start_hour_variable)

        start_minutes_spinbox = tk.Spinbox(self.start_hour_frame, from_=0, to=59, wrap=True, state="readonly",
                                           textvariable=self.start_minutes_variable, width=2, justify='center')
        start_hour_spinbox.grid(row=0, column=0)
        start_minutes_spinbox.grid(row=0, column=1)
        end_hour_spinbox = tk.Spinbox(self.end_hour_frame, from_=0, to=23, wrap=True, width=2, state="readonly",
                                      justify='center', textvariable=self.end_hour_variable)

        end_minutes_spinbox = tk.Spinbox(self.end_hour_frame, from_=0, to=59, wrap=True, state="readonly",
                                         textvariable=self.end_minutes_variable, width=2, justify='center')
        end_hour_spinbox.grid(row=0, column=0)
        end_minutes_spinbox.grid(row=0, column=1)
        self.new_meeting_button = tk.Button(self.content_frame, text='Add', activebackground='#4B93B7',
                                            bg='#64CBFF', padx=10, pady=10,
                                            command=self.add_new_meeting)
        self.new_meeting_button.grid(row=1, column=4, padx=10, pady=10)

    def view_meetings_command(self):
        try:
            self.content_frame.destroy()
        except Exception as e:
            print(str(e))
        self.content_frame = tk.Frame()
        # view meetings logic

    def export_command(self):
        try:
            self.content_frame.destroy()
        except Exception as e:
            print(str(e))
        self.content_frame = tk.Frame()
        # export logic

    def import_command(self):
        try:
            self.content_frame.destroy()
        except Exception as e:
            print(str(e))
        self.content_frame = tk.Frame()

    def add_person_to_database(self):
        firstname = self.firstname_entry.get().capitalize()
        lastname = self.lastname_entry.get().capitalize()
        if Utils.get_person(firstname, lastname):
            tk.messagebox.showerror(title="Person Already Exists",
                                    message="The person you are trying to add already exists!")
            return
        if firstname == '' or lastname == '':
            tk.messagebox.showerror(title="Invalid arguments",
                                    message="Firstname and lastname must be a non-empty string!")
            return
        status = Utils.add_person(firstname, lastname)
        if status:
            tk.messagebox.showinfo(title="Success", message=f"{lastname} {firstname} was added to the database!")
        else:
            tk.messagebox.showerror(title="Database error",
                                    message=f"Failed to add person to database\nCause:{status}")

    def add_new_meeting(self):
        pass
