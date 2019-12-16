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

Window.clearcolor = (.98, .98 ,.98, 1)

class MainScreen(Screen):
    main_window = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_task(self):
        self.container = BoxLayout(orientation = "horizontal", size_hint = (1, None), height = 40)
        self.lb = Label(text = self.task_text.text, color = (0, 0, 0, 1), size_hint = (.7, 1), )
        self.rm = Button(text = "Delete task", size_hint = (.3, 1))

        self.container.add_widget(self.lb)
        self.container.add_widget(self.rm)
        self.box.add_widget(self.container)


# SideBar
class Menu(BoxLayout):
    pass

class AnotherScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ScreenManagement(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return presentation

if __name__ == "__main__":

    presentation = Builder.load_file("main.kv")

    MainApp().run()