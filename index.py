#  -*- coding: utf-8 -*-

from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

Window.clearcolor = (.98, .98 ,.98, 1)

class Task(BoxLayout):
    def __init__(self, text):
        super().__init__()

        self.text = text

        self.orientation = "horizontal"
        self.size_hint = (1, None)
        self.height = 30

        self.lb = Label(text = self.text, color = (0, 0, 0, 1), size_hint = (None, None), size  = (380, 30), halign = "left")
        self.lb.text_size = (380, 30)

        self.func_1 = lambda x: self.edit_task()
        self.func_2 = lambda x: self.save_task()

        self.editButton = Button(text = "Edit", size_hint = (None, 1), width = 80)

        self.editButton.bind(on_press = self.func_1)

        self.add_widget(self.lb)
        self.add_widget(self.editButton)

    def edit_task(self):
        self.clear_widgets()
        self.editInput = TextInput(text = self.lb.text, size_hint = (None, None), size = (380, 30))

        self.editButton.text = "Save"

        self.editButton.unbind(on_press = self.func_1)
        self.editButton.bind(on_press = self.func_2)

        self.add_widget(self.editInput)
        self.add_widget(self.editButton)

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

# SideBar
class Menu(BoxLayout):
    pass

class MainScreen(Screen):
    input = ObjectProperty()
    box = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def add_task(self):
        if (self.input.text == ""):
            return

        self.box.add_widget(Task(self.input.text))

    def _finish_init(self, dt):
        pass

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

    def _finish_init(self, dt):
        pass

class ScreenManagement(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return presentation

if __name__ == "__main__":

    presentation = Builder.load_file("main.kv")

    MainApp().run()