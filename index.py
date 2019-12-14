from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

Window.clearcolor = (.98, .98 ,.98, 1)

class MainScreen(Screen):
    main_window = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        print(self.main_window)

# SideBar
class Menu(BoxLayout):
    pass

class MainLayout(BoxLayout):
    pass

class AnotherScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "second"

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        return presentation

if __name__ == "__main__":
    MainApp().run()