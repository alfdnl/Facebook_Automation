## Windows Initialisation
from win32api import GetSystemMetrics
from kivy.config import Config

print("Width =", GetSystemMetrics(0))
print("Height =", GetSystemMetrics(1))

# Adjust the position of the window
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top',  30) 
  
# fix the width of the window  
Config.set('graphics', 'width', GetSystemMetrics(0))
# fix the height of the window  
Config.set('graphics', 'height', GetSystemMetrics(1)-70)  

# Imports
import tkinter as tk
from tkinter import filedialog
import kivy
from kivymd.app import MDApp
import os
kivy.require('1.11.1')
from kivy.clock import Clock, mainthread
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import ListProperty, ObjectProperty
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from random import random
from Facebook_automation import *
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
import pandas as pd
import json
import threading


class MyFloat(FloatLayout):    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.post_path=None
        self.details_path=None

    def foo(self):
        pass
    
    def open_post_file(self,btn):
        # if isinstance(btn,Button):
        # print("Enter")
        self.post_path = filedialog.askopenfilename()
        if self.post_path is not '':
            btn.text = os.path.basename(self.post_path)
            print(btn.text)                        
        else:
            btn.text='Select Post File'
            print("No file choosen")    
    
    def open_detail_file(self,btn):
        # if isinstance(btn,Button):
        self.details_path = filedialog.askopenfilename()
        if self.details_path is not '':
            btn.text = os.path.basename(self.details_path)
            print(btn.text)
        else:
            btn.text='Select Details File'
            print("No file choosen")
    
    @mainthread
    def create_row(self, *args):
        print("Inside create_row")

        # Get the id of the window
        posts_container = self.ids.testing

        # Create box layout
        details = BoxLayout(size_hint_y=None,height=30,pos_hint={'top': 1})
        posts_container.add_widget(details)                        
        
        # Details
        index = Label(text=str(args[0]+1),size_hint_x=.1,color=(0,0,0,1))
        name = Label(text=args[1],size_hint_x=.2,color=(0,0,0,1))
        post_id = Label(text=args[4],size_hint_x=.2,color=(0,0,0,1))        
        DateTime =Label(text=args[2],size_hint_x=.2,color=(0,0,0,1))
        Status =Label(text=args[3],size_hint_x=.2,color=(0,0,0,1))
        remarks =Label(text=args[-1],size_hint_x=.4,color=(0,0,0,1))
        
        # Add Widget
        details.add_widget(index)
        details.add_widget(name)
        details.add_widget(post_id)        
        details.add_widget(DateTime)
        details.add_widget(Status)
        details.add_widget(remarks)

    def start_new_thread(self,btn):
        threading.Thread(target=self.publish_post, args=(btn,)).start()
        

    def publish_post(self,btn):
        if isinstance(btn,Button):
            threads=[]
            template = ['page_name','message/description/caption','link','img _path','vid_path','vid_title','Date & Time']
            posts_container = self.ids.testing
            posts_container.clear_widgets()
            
            # Get the users details from csv file
            print("Inside publish post {}",self.details_path)
            details_df = pd.read_csv(self.details_path)

            email = details_df.loc[0][0]
            password = details_df.loc[0][1]
            client_id= details_df.loc[0][2]

            # Get access token
            
            access_token = get_user_access_token(email,password,client_id)
            if access_token == 'None':
	            self.show_popup1()
	            return

            # Load post data
            try:
            	post_df= pd.read_csv(self.post_path).fillna(value= '')
            	if list(post_df) != template:
            		print("Wrong Template")
            		self.show_popup3()
            		return

            except:
            	self.show_popup2()
            	return

            # Loop through the data and post it on FB
            for index, row in post_df.iterrows():
                print()
                if row[2].strip() == '':
                    print("masuk")
                    link = None
                else:
                    link = row[2]
                if row[3].strip() == '':
                    IMG_PATH = None
                else:
                    IMG_PATH = row[3]
                if row[4].strip() == '':
                    VID_PATH = None
                else:
                    VID_PATH = row[4]
                if row[5].strip() == '':
                    VID_TITLE = None
                else:
                    VID_TITLE = row[5]
                
                # print(index,type(row[-1]))
                # print(row[5])
                
                page_access_token,page_id = get_page_access_token(access_token,row[0])
                
                # print(page_access_token,page_id)                        
                # print(link)
                status = post_to_wall(page_id,row[1],page_access_token,row[-1],link,VID_PATH,IMG_PATH,VID_TITLE)
                print(status)
                status_dict = json.loads(status)
                post_id= "None"
                remarks= ""

                if 'id' in status_dict.keys():
                    print('Success')
                    print(status_dict['id'].replace(page_id+"_",""))
                    Status='Scheduled'
                    post_id = status_dict['id'].replace(page_id+"_","")
                else:
                    print(status_dict['error']['message'])
                    remarks= status_dict['error']['message'].replace("(#100) ","")
                    print(remarks)
                    Status='Error'
                
                # Update in main thread
                self.create_row(index,row[0],row[-1],Status,post_id,remarks)
  
    def show_popup1(self):
        floatL = FloatLayout(size=(300, 300))
        btn = Button(text ='Invalid Username/Password',
        			background_color =(1, 1, 1, 1),
                    size_hint =(.3, .2), 
                    pos_hint ={'x':.35, 'y':.4 })
        floatL.add_widget(btn)
        popupWindow = Popup(title="Error", content= floatL, size_hint=(None,None),size=(400,400))
        popupWindow.open()

    def show_popup2(self):
        floatL = FloatLayout(size=(300, 300))
        btn = Button(text ='Post Template file is not chosen',
        			background_color =(1, 1, 1, 1),
                    size_hint =(.3, .2), 
                    pos_hint ={'x':.35, 'y':.4 })
        floatL.add_widget(btn)
        popupWindow = Popup(title="Error", content= floatL, size_hint=(None,None),size=(400,400))
        popupWindow.open()

    def show_popup3(self):
        floatL = FloatLayout(size=(300, 300))
        btn = Button(text ='The Template chosen is not correct',
        			background_color =(1, 1, 1, 1),
                    size_hint =(.3, .2), 
                    pos_hint ={'x':.35, 'y':.4 })
        floatL.add_widget(btn)
        popupWindow = Popup(title="Error", content= floatL, size_hint=(None,None),size=(400,400))
        popupWindow.open()


        

class GUI(MDApp):

    def build(self):
        self.title="FB Post Scheduler"
        self.icon = 'icon.png'
        layout = MyFloat()         
        return layout    

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    GUI().run()