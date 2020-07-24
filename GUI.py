import tkinter as tk
from tkinter import filedialog
import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ListProperty, ObjectProperty
from kivy.graphics import Rectangle, Color
from random import random
from Facebook_automation import main as post_to_wall



class MyFloat(FloatLayout):    
    
    def __init__(self, **kwargs):
    	super().__init__(**kwargs)

    	self.post_path=None
    	self.details_path=None

    def foo(self):
        pass
    
    def open_post_file(self,btn):
        if isinstance(btn,Button):
 	       	self.post_path = filedialog.askopenfilename()
 	       	print(self.post_path)
    
    def open_detail_file(self,btn):
        if isinstance(btn,Button):
 	       	self.details_path = filedialog.askopenfilename()
 	       	print(self.details_path)

    def publish_post(self,btn):
        if isinstance(btn,Button):
        	post_to_wall(self.details_path,self.post_path)
 	       	
   	
            
    
    def show_load_list(self):
        pass

class GUI(App):

    def build(self):
        # return a Button() as a root widget
        layout = MyFloat()

        return layout

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    GUI().run()