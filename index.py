#  -*- coding: utf-8 -*-

from kivymd.app import MDApp

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.uix.picker import MDDatePicker
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

from kivy.uix.boxlayout import BoxLayout

from Task import Task

import datetime
from calendar import monthrange

import sqlite3

Window.clearcolor = (.98, .98 ,.98, 1)

class MainScreen(Screen):

    input     = ObjectProperty()
    box       = ObjectProperty()
    dateLabel = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._finitsh_init)

    def _finitsh_init(self, dt):
        # Assign label current date
        self.dateLabel.text = str(datetime.datetime.now().date().strftime("%b %d, %Y"))
        self.dt = datetime.datetime.now().date()

        self.conn = sqlite3.connect("./db/todo.db")
        self.c = self.conn.cursor()

        self.update()

    def add_task(self):
        # If input haven't text
        if (self.input.text == ""):
            return

        self.box.add_widget(Task(0, self.input.text, self.dt.strftime("%b %d"), 0))
        self.input.text = ""

        # Update Today screen
        today = self.manager.get_screen("Today")
        today.update()

        # Update Important_tasks screen
        imp = self.manager.get_screen("Important_tasks")
        imp.update()

    def show_datepicker(self):
        picker = MDDatePicker(callback = self.get_date)
        picker.open()

    def get_date(self, dt):
        if (dt < datetime.datetime.now().date()):
            return

        self.dt = dt
        self.dateLabel.text = self.dt.strftime("%b %d, %Y")

    def update(self):
        self.box.clear_widgets()
        for task in self.c.execute("SELECT * FROM tasks"):
            day = task[2].split(" ")[1]
            today = int(datetime.datetime.now().day)
            delta = int(day) - today

            # If the task has expired
            if (delta < 0):
                print("Here")
                self.c.execute("DELETE FROM tasks WHERE id = ?", [task[0]])
                self.c.execute("UPDATE points SET points = points - 10 WHERE day = ?", [today])
                continue
            print("here")

            self.box.add_widget(Task(task[0], task[1], task[2], task[3]))


class Today(Screen):

    input = ObjectProperty()
    box   = ObjectProperty()
    date  = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.currentDate = datetime.datetime.now().date().strftime("%b %d")
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        self.date.text = self.currentDate
        self.conn = sqlite3.connect("./db/todo.db")
        self.c = self.conn.cursor()

    def add_task(self):
        if (self.input.text == ""):
            return

        self.box.add_widget(Task(0, self.input.text, self.currentDate, 0))
        
        self.input.text = ""

        # Update main screen
        main = self.manager.get_screen("Tasks")
        main.update()
        
        # Update Important_tasks screen
        imp = self.manager.get_screen("Important_tasks")
        imp.update()
    
    def update(self):
        self.box.clear_widgets()
        for task in self.c.execute("SELECT * FROM tasks WHERE date = ?", [self.currentDate]):
            self.box.add_widget(Task(task[0], task[1], task[2], task[3]))

class Important_tasks(Screen):

    important_box = ObjectProperty()
    expiring_box = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        self.update()

    def update(self):
        self.conn = sqlite3.connect("./db/todo.db")
        self.c = self.conn.cursor()
        self.today = int(datetime.datetime.now().day)

        self.important_box.clear_widgets()
        for task in self.c.execute("SELECT * FROM tasks WHERE favorite = ?", [1]):
            self.important_box.add_widget(Task(task[0], task[1], task[2], task[3]))

        self.expiring_box.clear_widgets()
        for task in self.c.execute("SELECT * FROM tasks"):
            day = task[2].split(" ")[1]
            delta = int(day) - self.today

            if (delta < 5):
                self.expiring_box.add_widget(Task(task[0], task[1], task[2], task[3]))
            
            

class Statistics(Screen):
    box = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dt = datetime.datetime.now()

        Clock.schedule_once(self._build_graph)

        self.conn = sqlite3.connect("./db/todo.db")
        self.c = self.conn.cursor()
    
    def _build_graph(self, dt = None):
        self.plt = plt
        self.plt.figure(num=None, figsize=(1, 1), dpi=70, facecolor='w', edgecolor='k')        
        self.plt.title(self.dt.strftime("%Y %B"))
        self.plt.ylabel('Points')
        self.plt.xlabel("Days")

        self.s = []
        self.days = []

        for day in range(monthrange(self.dt.year, self.dt.month)[1]):
            self.days.append(day + 1)

        for tp in self.c.execute("SELECT * FROM points").fetchall():
            self.s.append(tp[1])

        x = range(len(self.s))
        self.ax = self.plt.gca()
        self.ax.bar(x, self.s, align = "edge")
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(self.days)

        self.box.add_widget(FigureCanvasKivyAgg(self.plt.gcf()))

    def updateStats(self):
        self.box.clear_widgets()
        self._build_graph()

    def update(self):
        pass

class Menu(BoxLayout):
    
    def updateScreen(self, screenName):
        screenName = str(screenName)
        # Get ScreenManager
        sm = self.get_root_window().children[0]
        # Change screen
        sm.current = screenName

        # Update current screen
        sm.get_screen(screenName).update()



class ScreenManagement(ScreenManager):
    pass

class MainApp(MDApp):
    def build(self):
        pass

if __name__ == "__main__":
    
    MainApp().run()