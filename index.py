#  -*- coding: utf-8 -*-

from kivymd.app import MDApp

from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

from kivymd.uix.picker import MDDatePicker

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

Window.clearcolor = (.98, .98 ,.98, 1)
Window.size = (900, 600)


class Task(BoxLayout):
    def __init__(self, text):
        super().__init__()

        self.text = text

        self.orientation = "horizontal"
        self.size_hint = (1, None)
        self.height = 60

        self.lb = Label(text = self.text, color = (0, 0, 0, 1), size_hint = (None, None), size  = (390, 60), halign = "left", valign = "middle")
        self.lb.text_size = (390, 60)

        self.func_1 = lambda x: self.edit_task()
        self.func_2 = lambda x: self.save_task()

        self.editButton = Button(text = "Edit", size_hint = (None, None), width = 85, height = 30, pos_hint = {"x": 0, "y": .3})

        self.editButton.bind(on_press = self.func_1)

        self.favorite = CheckBox(size_hint = (None, None), size = (60, 30), pos_hint = {"x": 1, "y": .33})
        self.favorite.background_checkbox_normal = "./image/star(no active).png"
        self.favorite.background_checkbox_down = "./image/star(active).png"
        self.favorite.bind(active = self.add_to_favorites)

        self.add_widget(self.lb)
        self.add_widget(self.editButton)
        self.add_widget(self.favorite)

    def edit_task(self):
        self.clear_widgets()
        self.editInput = TextInput(text = self.lb.text, size_hint = (None, None), size = (390, 30), pos_hint = {"x": 0, "y": .3})

        self.editButton.text = "Save"

        self.editButton.unbind(on_press = self.func_1)
        self.editButton.bind(on_press = self.func_2)

        self.add_widget(self.editInput)
        self.add_widget(self.editButton)
        self.add_widget(self.favorite)

    def save_task(self):
        self.clear_widgets()

        if (self.editInput.text == ""):
            self.parent.remove_widget(self)
            return

        self.lb.text = self.editInput.text

        self.editButton.text = "Edit"

        self.editButton.unbind(on_press = self.func_2)
        self.editButton.bind(on_press = self.func_1)

        self.add_widget(self.lb)
        self.add_widget(self.editButton)
        self.add_widget(self.favorite)

    def add_to_favorites(self, checkbox, value):
        print(value)

# SideBar
class Menu(BoxLayout):
    pass

class MainScreen(Screen):
    input = ObjectProperty()
    box = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        self.box.add_widget(Task("Случайная задача"))

    def add_task(self):
        if (self.input.text == ""):
            return

        self.box.add_widget(Task(self.input.text))

    def show_datepicker(self):
        picker = MDDatePicker(callback = self.get_date)
        picker.open()

    def get_date(self, dt):
        print(dt)

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

class Calendar(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

class MainApp(MDApp):
    def build(self):
        return presentation

if __name__ == "__main__":

    presentation = Builder.load_file("main.kv")

    MainApp().run()