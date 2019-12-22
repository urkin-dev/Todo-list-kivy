#  -*- coding: utf-8 -*-

from kivymd.app import MDApp

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.uix.picker import MDDatePicker
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

from Task import Task

import datetime

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

    def add_task(self):
        # If input haven't text
        if (self.input.text == ""):
            return

        # If time was chosen
        if (hasattr(self, "dt")):
            self.box.add_widget(Task(self.input.text, self.dt))
        else:
            self.box.add_widget(Task(self.input.text, datetime.datetime.now().date()))

    def show_datepicker(self):
        picker = MDDatePicker(callback = self.get_date)
        picker.open()

    def get_date(self, dt):
        self.dt = dt
        self.dateLabel.text = self.dt.strftime("%b %d, %Y")

class Today(Screen):

    input = ObjectProperty()
    box   = ObjectProperty()
    date  = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        currentDate = datetime.datetime.now().date()
        self.date.text = currentDate.strftime("%d %B")

    def add_task(self):
        if (self.input.text == ""):
            return

        self.box.add_widget(Task(self.input.text))

class Statistics(Screen):
    box = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._build_graph)
    
    def _build_graph(self, dt):
        plt.title("2019 December")
        plt.ylabel('Points')
        plt.xlabel("Days")
        
        s = [10, 30, 50, 30, 10, 10, 0, 50, 10, 30, 50, 30, 10, 10, 0, 50]
        days = ["07", "08", "09", "10", "11", "12", "13", "14", "07", "08", "09", "10", "11", "12", "13", "14"]
        x = range(len(s))
        ax = plt.gca()
        ax.bar(x, s, align = "edge")
        ax.set_xticks(x)
        ax.set_xticklabels(days)

        self.box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

class ScreenManagement(ScreenManager):
    pass

class MainApp(MDApp):
    def build(self):
        pass

if __name__ == "__main__":
    MainApp().run()