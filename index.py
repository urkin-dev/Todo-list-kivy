#  -*- coding: utf-8 -*-

from kivymd.app import MDApp

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivymd.uix.picker import MDDatePicker
from kivy.uix.image import Image

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

Window.clearcolor = (.98, .98 ,.98, 1)


class Task(BoxLayout):

    lb = ObjectProperty()
    editBtn = ObjectProperty()
    favorite = ObjectProperty()
    imageEdit = ObjectProperty()

    def __init__(self, text):
        super().__init__()

        self.text = text
        self.lb.text = self.text

        self.func_1 = lambda x: self.edit_task()
        self.func_2 = lambda x: self.save_task()

        self.favorite.bind(active = self.add_to_favorites)

        self.editBtn.bind(on_press = self.func_1)

    def edit_task(self):
        self.clear_widgets()
        self.editInput = TextInput(text = self.lb.text, size_hint = (1, None), height = 30, pos_hint = {"x": 0, "y": .3})

        self.editBtn.text = "Save"
        self.imageEdit.source = "./image/save.png"

        self.editBtn.unbind(on_press = self.func_1)
        self.editBtn.bind(on_press = self.func_2)

        self.add_widget(self.editInput)
        self.add_widget(self.editBtn)
        self.add_widget(self.favorite)

    def save_task(self):
        self.clear_widgets()

        if (self.editInput.text == ""):
            self.parent.remove_widget(self)
            return

        self.lb.text = self.editInput.text

        self.editBtn.text = "Edit"
        self.imageEdit.source = "./image/edit.png"

        self.editBtn.unbind(on_press = self.func_2)
        self.editBtn.bind(on_press = self.func_1)

        self.add_widget(self.lb)
        self.add_widget(self.editBtn)
        self.add_widget(self.favorite)

    def add_to_favorites(self, checkbox, value):
        print(value)

class MainScreen(Screen):
    input = ObjectProperty()
    box = ObjectProperty()

    def add_task(self):
        if (self.input.text == ""):
            return

        self.box.add_widget(Task(self.input.text))

    def show_datepicker(self):
        picker = MDDatePicker(callback = self.get_date)
        picker.open()

    def get_date(self, dt):
        self.dt = dt
        print(self.dt)

class Today(Screen):
    input = ObjectProperty()
    box = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def add_task(self):
        if (self.input.text == ""):
            return

        self.box.add_widget(Task(self.input.text))

    def show_datepicker(self):
        picker = MDDatePicker(callback = self.get_date)
        picker.open()

    def get_date(self, dt):
        print(dt)

    def _finish_init(self, dt):
        pass

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