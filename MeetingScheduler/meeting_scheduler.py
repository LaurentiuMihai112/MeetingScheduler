import tkinter as tk


class MeetingScheduler:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Meeting Scheduler')
        self.window.resizable(0, 0)
        self.window.geometry('1200x750')
        self.window.configure(bg='#E3F6FF')
        self.buttons_frame = tk.Frame()
        self.buttons_frame.pack(side='top')
        self.add_button = tk.Button(self.buttons_frame, text='Add person', activebackground='#4B93B7',
                                    bg='#64CBFF', padx=10, pady=10,
                                    command=self.add_command)
        self.add_button.grid(row=0, column=1, padx=10, pady=10)
        self.schedule_meeting_button = tk.Button(self.buttons_frame, text='New meeting', activebackground='#4B93B7',
                                                 bg='#64CBFF', padx=10, pady=10,
                                                 command=self.schedule_meeting_command)
        self.schedule_meeting_button.grid(row=0, column=3, padx=10, pady=10)
        self.view_meetings_button = tk.Button(self.buttons_frame, text='View meetings', activebackground='#4B93B7',
                                              bg='#64CBFF', padx=10, pady=10,
                                              command=self.view_meetings_command)
        self.view_meetings_button.grid(row=0, column=5, padx=10, pady=10)
        self.export_button = tk.Button(self.buttons_frame, text='Export', activebackground='#4B93B7',
                                       bg='#64CBFF', padx=10, pady=10,
                                       command=self.export_command)
        self.export_button.grid(row=0, column=7, padx=10, pady=10)
        self.import_button = tk.Button(self.buttons_frame, text='Import', activebackground='#4B93B7',
                                       bg='#64CBFF', padx=10, pady=10,
                                       command=self.import_command)
        self.import_button.grid(row=0, column=9, padx=10, pady=10)
        self.content_frame = None
        self.window.mainloop()

    def add_command(self):
        try:
            self.content_frame.destroy()
        except Exception:
            print("No content to destroy")
        self.content_frame = tk.Frame()
        # add command logic

    def schedule_meeting_command(self):
        try:
            self.content_frame.destroy()
        except Exception:
            print("No content to destroy")
        self.content_frame = tk.Frame()
        # schedule meeting logic

    def view_meetings_command(self):
        try:
            self.content_frame.destroy()
        except Exception:
            print("No content to destroy")
        self.content_frame = tk.Frame()
        # view meetings logic

    def export_command(self):
        try:
            self.content_frame.destroy()
        except Exception:
            print("No content to destroy")
        self.content_frame = tk.Frame()
        # export logic

    def import_command(self):
        try:
            self.content_frame.destroy()
        except Exception:
            print("No content to destroy")
        self.content_frame = tk.Frame()
        # export logic
