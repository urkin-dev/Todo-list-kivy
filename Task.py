from kivy.properties import ObjectProperty

from kivymd.uix.picker import MDDatePicker

from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import Screen

import sqlite3
import uuid
import datetime

class Task(BoxLayout):

    lb        = ObjectProperty()
    edit      = ObjectProperty()
    favorite  = ObjectProperty()
    checkbox  = ObjectProperty()
    time      = ObjectProperty()
    labelDate = ObjectProperty()

    def __init__(self, id, text, date, favoriteStatus):
        super().__init__()

        # DB connect
        self.conn = sqlite3.connect("./db/todo.db")
        self.c = self.conn.cursor()

        self.text = text
        self.date = date
        self.favoriteStatus = favoriteStatus
        if (self.favoriteStatus == 1):
            self.favorite.active = True
        
        # If new task -> create new row in DB
        if (id == 0):
            self.id = str(uuid.uuid4()) # Unique id
            self.c.execute("INSERT INTO tasks VALUES(?, ?, ?, ?)", [self.id, self.text, self.date, self.favoriteStatus])
            self.conn.commit()
        else:
            self.id = id    
        
        self.lb.text = text

        self.favorite.bind(active = self.add_to_favorites)
        self.checkbox.bind(active = self.done)
        self.edit.bind(active = self.edit_task)
        self.time.bind(on_press = self.show_datepicker)
        self.labelDate.text = self.date

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

        self.lb.text = self.editInput.text

        self.edit.unbind(active = self.save_task)
        self.edit.bind(active = self.edit_task)

        self.add_widget(self.checkbox)
        self.add_widget(self.lb)
        self.add_widget(self.labelDate)
        self.add_widget(self.edit)
        self.add_widget(self.favorite)
        self.add_widget(self.time)

        self.updateDB("name", self.lb.text)

    def add_to_favorites(self, checkbox, value):
        if (value):
            self.updateDB("favorite", 1)
        else:
            self.updateDB("favorite", 0)
        
    def done(self, checkbox, value):
        self.checkbox.unbind(active = self.done)
        self.lb.strikethrough = True
        self.lb.text = self.lb.text + " +10 Points"
        self.add_points(10)
        
        Clock.schedule_once(lambda x: self.parent.remove_widget(self), 1)

        # Delete task from db
        self.c.execute("DELETE FROM tasks WHERE id = ?", [self.id])
        self.conn.commit()

    def show_datepicker(self, instance):
        MDDatePicker(callback = self.get_date).open()
        
    def get_date(self, dt):
        if (dt < datetime.datetime.now().date()):
            return
        self.labelDate.text = dt.strftime("%b %d")
        self.updateDB("date", dt.strftime("%b %d"))

        # Update screen Today
        self.get_root_window().children[1].get_screen("Today").update()

    def updateDB(self, propName, value):
        sql = "UPDATE tasks SET {0} = ? WHERE id = ?".format(propName)
        self.c.execute(sql, [value, self.id])
        self.conn.commit()

    def add_points(self, value):
        today = datetime.datetime.now().day
        
        self.c.execute("UPDATE points SET points = points + 10 WHERE day = ?", [today])
        self.conn.commit()