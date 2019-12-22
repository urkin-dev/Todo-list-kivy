from kivy.properties import ObjectProperty

from kivymd.uix.picker import MDDatePicker

from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

class Task(BoxLayout):

    lb       = ObjectProperty()
    edit     = ObjectProperty()
    favorite = ObjectProperty()
    checkbox = ObjectProperty()
    time     = ObjectProperty()

    def __init__(self, text, date):
        super().__init__()

        self.text = text
        self.date = date
        self.lb.text = self.text

        self.favorite.bind(active = self.add_to_favorites)
        self.checkbox.bind(active = self.done)
        self.edit.bind(active = self.edit_task)
        

    def edit_task(self, checkbox, value):
        self.clear_widgets()
        self.editInput = TextInput(text = self.lb.text, size_hint = (1, None), height = 30, pos_hint = {"x": 0, "y": .25}, allow_copy = True)

        self.edit.unbind(active = self.edit_task)
        self.edit.bind(active = self.save_task)

        self.add_widget(self.editInput)
        self.add_widget(self.edit)
        self.add_widget(self.favorite)
        self.add_widget(self.time)

    def save_task(self, checkbox, value):
        self.clear_widgets()

        if (self.editInput.text == ""):
            self.parent.remove_widget(self)
            return

        self.lb.text = self.editInput.text

        self.edit.unbind(active = self.save_task)
        self.edit.bind(active = self.edit_task)

        self.add_widget(self.checkbox)
        self.add_widget(self.lb)
        self.add_widget(self.edit)
        self.add_widget(self.favorite)
        self.add_widget(self.time)

    def add_to_favorites(self, checkbox, value):
        print(value)

    def done(self, checkbox, value):
        self.lb.strikethrough = True
        self.lb.text = self.lb.text + " +10 Points"
        Clock.schedule_once(lambda x: self.parent.remove_widget(self), 2)

    def show_datepicker(self):
        picker = MDDatePicker(callback = self.get_date)
        picker.open()

    def get_date(self, dt):
        self.date = dt