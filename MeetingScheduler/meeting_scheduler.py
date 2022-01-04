import datetime
import tkinter as tk
import icalendar
import tkcalendar
from tkinter import messagebox, END, MULTIPLE, font, ttk, NO, CENTER, filedialog
from icalendar import Calendar, Event
from database_utils import Utils


class MeetingScheduler:
    def __init__(self):
        """
        Constructor that creates main window
        """
        self.window = tk.Tk()
        self.window.title('Meeting Scheduler')
        self.window.resizable(0, 0)
        self.window.geometry('1250x750')
        self.window.configure(bg='#E3F6FF')
        self.buttons_frame = tk.Frame()
        my_font = font.Font(family='Consolas', size=15, weight='bold')
        self.buttons_frame.pack(side='left')
        self.add_button = tk.Button(self.buttons_frame, text='Add person', activebackground='#4B93B7',
                                    bg='#64CBFF', padx=10, pady=10, width=15, font=my_font,
                                    command=self.add_command)
        self.add_button.grid(row=0, column=0, padx=10, pady=10)
        self.schedule_meeting_button = tk.Button(self.buttons_frame, text='New meeting', activebackground='#4B93B7',
                                                 bg='#64CBFF', padx=10, pady=10, width=15, font=my_font,
                                                 command=self.schedule_meeting_command)
        self.schedule_meeting_button.grid(row=2, column=0, padx=10, pady=10)
        self.view_meetings_button = tk.Button(self.buttons_frame, text='View meetings', activebackground='#4B93B7',
                                              bg='#64CBFF', padx=10, pady=10, width=15, font=my_font,
                                              command=self.view_meetings_command)
        self.view_meetings_button.grid(row=4, column=0, padx=10, pady=10)
        self.export_button = tk.Button(self.buttons_frame, text='Export', activebackground='#4B93B7',
                                       bg='#64CBFF', padx=10, pady=10, width=15, font=my_font,
                                       command=self.export_command)
        self.export_button.grid(row=6, column=0, padx=10, pady=10)
        self.import_button = tk.Button(self.buttons_frame, text='Import', activebackground='#4B93B7',
                                       bg='#64CBFF', padx=10, pady=10, width=15, font=my_font,
                                       command=self.import_command)
        self.import_button.grid(row=8, column=0, padx=10, pady=10)
        self.content_frame = None
        self.firstname_entry = None
        self.lastname_entry = None
        self.add_person_to_database_button = None
        self.start_date_calendar = None
        self.end_date_calendar = None
        self.start_hour_variable = None
        self.end_hour_variable = None
        self.start_hour_frame = None
        self.end_hour_frame = None
        self.new_meeting_button = None
        self.add_person_var = None
        self.add_person_listbox = None
        self.start_minutes_variable = None
        self.end_minutes_variable = None
        self.participants_frame = None
        self.participants_label = None
        self.participants_listbox = None
        self.meetings_view = None
        self.file_entry = None
        self.description_frame = None
        self.description_entry = None
        self.file_content = None
        self.view_button = None
        self.name_entry = None
        self.window.mainloop()

    def add_command(self):
        """
        Method to create UI for adding a person
        :return: None
        """

        self.destroy_content_frame()
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
        """
        Method to create UI for scheduling a meeting
        :return: None
        """
        self.destroy_content_frame()
        self.content_frame = tk.Frame(self.window, pady=10, height=150)
        self.content_frame.pack(side='left')
        current_date = datetime.datetime.now()
        tk.Label(self.content_frame, text="Start Date").grid(row=0, column=0)
        tk.Label(self.content_frame, text="End Date").grid(row=0, column=3)
        self.start_date_calendar = tkcalendar.Calendar(self.content_frame, year=int(current_date.strftime('%Y')),
                                                       month=int(current_date.strftime('%m')),
                                                       day=int(current_date.strftime('%d')))
        self.start_date_calendar.grid(row=1, column=0, padx=10, pady=10)

        self.end_date_calendar = tkcalendar.Calendar(self.content_frame, year=int(current_date.strftime('%Y')),
                                                     month=int(current_date.strftime('%m')),
                                                     day=int(current_date.strftime('%d')))
        self.end_date_calendar.grid(row=1, column=3, padx=10, pady=10)
        # hour_values = ('00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
        #                '16', '17', '18', '19', '20', '21', '22', '23')
        hour_values = [MeetingScheduler.fix_hour(x) for x in range(24)]
        self.start_hour_variable = tk.StringVar()
        self.end_hour_variable = tk.StringVar()
        self.start_minutes_variable = tk.StringVar()
        self.end_minutes_variable = tk.StringVar()
        current_hour = MeetingScheduler.fix_hour(current_date.strftime('%H'))
        self.start_hour_frame = tk.Frame(self.content_frame)
        self.end_hour_frame = tk.Frame(self.content_frame)
        start_hour_spinbox = tk.Spinbox(self.start_hour_frame, values=hour_values, wrap=True, width=2, state="readonly",
                                        justify='center', textvariable=self.start_hour_variable)
        end_hour_spinbox = tk.Spinbox(self.end_hour_frame, values=hour_values, wrap=True, width=2, state="readonly",
                                      justify='center', textvariable=self.end_hour_variable)
        start_minutes_spinbox = tk.Spinbox(self.start_hour_frame, values=('00', '15', '30', '45'), wrap=True, width=2,
                                           state="readonly", justify='center', textvariable=self.start_minutes_variable)
        end_minutes_spinbox = tk.Spinbox(self.end_hour_frame, values=('00', '15', '30', '45'), wrap=True, width=2,
                                         state="readonly", justify='center', textvariable=self.end_minutes_variable)
        self.start_hour_frame.grid(row=2, column=0)
        self.end_hour_frame.grid(row=2, column=3)

        self.new_meeting_button = tk.Button(self.content_frame, text='Create\nMeeting', activebackground='#4B93B7',
                                            bg='#64CBFF', padx=10, pady=10,
                                            command=self.add_new_meeting)
        self.add_person_var = tk.StringVar()
        self.add_person_listbox = tk.Listbox(self.content_frame, height=10, width=30, activestyle='dotbox',
                                             justify='center', selectmode=MULTIPLE)
        tk.Label(self.content_frame, text="Description").grid(row=0, column=4)
        tk.Label(self.content_frame, text="Participants").grid(row=0, column=5)
        self.description_entry = tk.Text(self.content_frame, height=10, width=20)
        persons = Utils.get_all_persons()
        for p in persons:
            self.add_person_listbox.insert(END, p[0])
        start_hour_spinbox.grid(row=0, column=0)
        end_hour_spinbox.grid(row=0, column=0)
        start_minutes_spinbox.grid(row=0, column=1)
        end_minutes_spinbox.grid(row=0, column=1)
        self.description_entry.grid(row=1, column=4, padx=10, pady=10)
        self.new_meeting_button.grid(row=1, column=6, padx=10, pady=10)
        self.add_person_listbox.grid(row=1, column=5, pady=10)
        self.start_hour_variable.set(MeetingScheduler.fix_hour(str(int(current_hour) + 1)))
        self.end_hour_variable.set(MeetingScheduler.fix_hour(str(int(current_hour) + 2)))

    def get_selected_persons(self):
        """
        Methid to get selected persons, used as participants for creating meetings
        :return: List of String
        """
        persons = []
        for i in self.add_person_listbox.curselection():
            persons.append(self.add_person_listbox.get(i))
        return persons

    def view_meetings_command(self):
        """
        Method to create UI for viewing meetings
        :return: None
        """
        self.destroy_content_frame()
        self.content_frame = tk.Frame()
        self.content_frame.pack(side='left')

        self.meetings_view = ttk.Treeview(self.content_frame, show='headings')
        self.meetings_view.bind('<Double-1>', self.update_participants)
        columns = ("meeting_id", "meeting_start", "meeting_end")
        self.meetings_view['columns'] = columns
        for col in columns:
            self.meetings_view.heading(col, text=col,
                                       command=lambda: MeetingScheduler.treeview_sort_column(self.meetings_view, col,
                                                                                             False))
        self.meetings_view.column("#0", width=0, stretch=NO)
        self.meetings_view.column("meeting_id", anchor=CENTER, width=80)
        self.meetings_view.column("meeting_start", anchor=CENTER, width=150)
        self.meetings_view.column("meeting_end", anchor=CENTER, width=150)
        self.meetings_view.heading("#0", text="", anchor=CENTER)
        self.meetings_view.heading("meeting_id", text="Id", anchor=CENTER)
        self.meetings_view.heading("meeting_start", text="Start Date", anchor=CENTER)
        self.meetings_view.heading("meeting_end", text="End Date", anchor=CENTER)

        self.description_frame = tk.Frame(self.content_frame)
        tk.Label(self.description_frame, text='Description').grid(row=0, column=0)
        self.description_entry = tk.Text(self.description_frame, height=10, width=30)
        current_date = datetime.datetime.now()
        self.start_date_calendar = tkcalendar.Calendar(self.content_frame, year=int(current_date.strftime('%Y')),
                                                       month=int(current_date.strftime('%m')),
                                                       day=int(current_date.strftime('%d')))

        self.end_date_calendar = tkcalendar.Calendar(self.content_frame, year=int(current_date.strftime('%Y')),
                                                     month=int(current_date.strftime('%m')),
                                                     day=int(current_date.strftime('%d')))
        self.participants_frame = tk.Frame(self.content_frame)
        self.participants_label = tk.Label(self.participants_frame, text='Participants')
        self.participants_listbox = tk.Listbox(self.participants_frame, height=10, width=40, justify='center')
        self.view_button = tk.Button(self.content_frame, text='View\nMeetings', activebackground='#4B93B7',
                                     bg='#64CBFF', padx=10, pady=10, command=self.view_meetings)
        self.view_button.grid(row=0, column=2, padx=10, pady=10)
        self.meetings_view.grid(row=1, column=0, padx=10, pady=10)
        self.participants_frame.grid(row=1, column=1, padx=10, pady=10)
        self.participants_label.grid(row=0, column=0, padx=10, pady=10)
        self.participants_listbox.grid(row=1, column=0, padx=10, pady=10)
        self.start_date_calendar.grid(row=0, column=0, padx=10, pady=10)
        self.end_date_calendar.grid(row=0, column=1, padx=10, pady=10)
        self.description_entry.grid(row=1, column=0, padx=10, pady=10)
        self.description_frame.grid(row=1, column=2, padx=10, pady=10)
        # view meetings logic

    def view_meetings(self):
        print(self.start_date_calendar.get_date())
        print(self.end_date_calendar.get_date())
        meetings = Utils.get_all_meetings(self.start_date_calendar.get_date(),
                                          self.end_date_calendar.get_date())
        print(meetings)
        for i in self.meetings_view.get_children():
            self.meetings_view.delete(i)
        for i, m in enumerate(meetings):
            self.meetings_view.insert(parent='', index='end', iid=i, text='', values=m)
        self.window.update()

    def export_command(self):
        """
        Method to create UI for exporting meetings
        :return: None
        """
        self.destroy_content_frame()
        self.content_frame = tk.Frame(self.window, pady=10, height=150)
        self.content_frame.pack(side='left')
        current_date = datetime.datetime.now()
        tk.Label(self.content_frame, text="Start Date").grid(row=0, column=0)
        tk.Label(self.content_frame, text="End Date").grid(row=0, column=3)
        self.start_date_calendar = tkcalendar.Calendar(self.content_frame, year=int(current_date.strftime('%Y')),
                                                       month=int(current_date.strftime('%m')),
                                                       day=int(current_date.strftime('%d')))
        self.start_date_calendar.grid(row=1, column=0, padx=10, pady=10)

        self.end_date_calendar = tkcalendar.Calendar(self.content_frame, year=int(current_date.strftime('%Y')),
                                                     month=int(current_date.strftime('%m')),
                                                     day=int(current_date.strftime('%d')))
        self.end_date_calendar.grid(row=1, column=3, padx=10, pady=10)
        tk.Button(self.content_frame, text='Export', activebackground='#4B93B7', bg='#64CBFF', padx=10, pady=10,
                  command=lambda: self.export_meetings(self.start_date_calendar.get_date(),
                                                       self.end_date_calendar.get_date())).grid(row=1, column=5,
                                                                                                padx=10, pady=10)

    def import_command(self):
        """
        Method to create UI for importing meetings
        :return: None
        """
        self.destroy_content_frame()
        self.content_frame = tk.Frame()
        self.content_frame = tk.Frame(self.window, pady=10, height=150)
        self.content_frame.pack(side='left')
        tk.Label(self.content_frame, text="Imported File").grid(row=0, column=0)
        tk.Button(self.content_frame, text='Browse', activebackground='#4B93B7', bg='#64CBFF', padx=10, pady=10,
                  command=self.browse_files).grid(row=1, column=1, padx=10, pady=10)
        self.file_entry = tk.Text(self.content_frame, width=30, height=2)
        self.file_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.content_frame, text="Content").grid(row=0, column=2, padx=10, pady=10)
        self.file_content = tk.Text(self.content_frame, height=10, width=35)
        self.file_content.grid(row=1, column=2, padx=10, pady=10)
        tk.Button(self.content_frame, text='Import Meetings', activebackground='#4B93B7', bg='#64CBFF', padx=10,
                  pady=10, command=self.import_meetings).grid(row=1, column=3, padx=10, pady=10)
        tk.Label(self.content_frame, text="Your Name:").grid(row=0, column=4, padx=10, pady=10)
        self.name_entry = tk.Entry(self.content_frame)
        self.name_entry.grid(row=1, column=4, padx=10, pady=10)

    def browse_files(self):
        """
        Method to browse files for importing
        :return: None
        """
        filename = filedialog.askopenfilename(initialdir=".", title="Select a File")
        f = open(filename, 'r')
        content = f.read(10000)

        self.file_content.delete('1.0', END)
        self.file_content.insert('1.0', content)
        self.file_entry.delete('1.0', END)
        self.file_entry.insert('1.0', filename)

    def import_meetings(self):
        """
        Method to handle importing meetings from .ics files
        :return: None
        """
        try:
            lastname, firstname = str(self.name_entry.get()).split(' ')
            lastname = str(lastname).capitalize()
            firstname = str(firstname).capitalize()
            print(lastname + " " + firstname)
            status = Utils.get_person_id(lastname, firstname)
            status_second = Utils.get_person_id(firstname, lastname)
            if status:
                p_id = status
            elif status_second:
                p_id = status_second
            else:
                Utils.add_person(firstname, lastname)
                p_id = Utils.get_person_id(firstname, lastname)
            file_calendar = Calendar.from_ical(self.file_content.get('1.0', END))

            for component in file_calendar.walk():
                if component.name == "VEVENT":
                    print(component.get('summary'))
                    print(component.get('dtstart').dt)
                    print(component.get('dtend').dt)
                    summary = component.get('summary')
                    dtstart = component.get('dtstart')
                    dtend = component.get('dtend')
                    Utils.add_meeting(dtstart.dt, dtend.dt, summary)
                    m_id = Utils.get_meeting_id(dtstart.dt, dtend.dt)
                    Utils.add_participants(m_id, p_id)
        except Exception as _:
            tk.messagebox.showerror(title="Name Error", message="You must provide a name")

    def add_person_to_database(self):
        """
        Method to handle adding a person from UI fields to the database
        :return: None
        """
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
        """
        Method to handle adding a meetings from UI fields to the database
        :return: None
        """
        persons = self.get_selected_persons()
        if not persons:
            tk.messagebox.showerror(title="Selection error",
                                    message=f"You must select at least 1 persons to create a meeting")
            return
        sm, sd, sy = self.start_date_calendar.get_date().split('/')
        em, ed, ey = self.end_date_calendar.get_date().split('/')
        sy = "20" + sy
        ey = "20" + ey

        start_hour = self.start_hour_variable.get()
        start_minutes = self.start_minutes_variable.get()
        end_hour = self.end_hour_variable.get()
        end_minutes = self.end_minutes_variable.get()
        full_start_date = datetime.datetime(int(sy), int(sm), int(sd), int(start_hour), int(start_minutes))
        full_end_date = datetime.datetime(int(ey), int(em), int(ed), int(end_hour), int(end_minutes))
        if full_end_date <= full_start_date:
            tk.messagebox.showerror(title="Date selection error",
                                    message=f"End date must be after start date")
            return
        description = self.description_entry.get('1.0', 'end')
        Utils.add_meeting(full_start_date, full_end_date, description)
        meeting_id = Utils.get_meeting_id(full_start_date, full_end_date)
        persons = self.get_selected_persons()
        for p in persons:
            person = p
            lastname, firstname, = person.split(' ')
            Utils.add_participants(meeting_id, Utils.get_person_id(firstname, lastname))
        tk.messagebox.showinfo(title="Success", message=f"The meeting was created")

    def destroy_content_frame(self):
        """
        Method for updating UI frames between different functionalities
        :return: None
        """
        try:
            self.content_frame.destroy()
        except AttributeError as _:
            pass

    @staticmethod
    def export_meetings(start_date, end_date):
        """
        Exports meetings between start date and end date in a .ics file
        :param start_date: start date 
        :param end_date: end date
        :return: None
        """
        print("exporting")
        meetings = Utils.get_all_meetings(start_date, end_date)
        cal = icalendar.Calendar()
        name = f"{str(start_date).replace(' ', '_').replace('/', '.')[:10]}-" \
               f"{str(end_date).replace(' ', '_').replace('/', '.')[:10]}"
        for meeting in meetings:
            event = Event()
            event.add('dtstart', meeting[1])
            event.add('dtend', meeting[2])
            event.add('summary', str(meeting[3]))
            cal.add_component(event)

        file = open(f"{name}_events.ics", 'wb+')
        file.write(cal.to_ical())
        file.close()

    def update_participants(self, _):
        """
        Updates the UI with each meeting's participants
        :param _: the mouse event
        :return: None
        """
        item = self.meetings_view.selection()[0]
        meeting_id = self.meetings_view.item(item, "values")[0]
        participants = Utils.get_participants(meeting_id)
        self.participants_listbox.delete(0, END)
        for p_id in participants:
            self.participants_listbox.insert(END, Utils.get_person_by_id(p_id)[0])
        description = Utils.get_meeting_description(meeting_id)
        self.description_entry.delete('1.0', END)
        if description is not None:
            self.description_entry.insert('1.0', str(description[0][0]))

    @staticmethod
    def fix_hour(hour):
        """
        Add a starting 0 to hours lower than 10
        :param hour: the hour
        :return: String (hour with preceding 0 if lower than 10)
        """
        if int(hour) < 10:
            return f"0{hour}"
        return f"{hour}"

    @staticmethod
    def treeview_sort_column(tree_view, col, reverse):
        """
        Sorts a tree view by a selected column
        :param tree_view: the tree view
        :param col: the selected column
        :param reverse: type of sorting
        :return: None
        """

        rows = [(tree_view.set(k, col), k) for k in tree_view.get_children('')]
        rows.sort(reverse=reverse)

        for index, (val, k) in enumerate(rows):
            tree_view.move(k, '', index)

        tree_view.heading(col, command=lambda: MeetingScheduler.treeview_sort_column(tree_view, col, not reverse))
