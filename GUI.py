import tkinter as tk
from tkinter import filedialog
import kivy
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
        if isinstance(btn,Button):
            self.post_path = filedialog.askopenfilename()
            btn.text = self.post_path.replace("/","\\").replace(os.getcwd(),"").replace("\\","")
            print(str(self.post_path).replace("/","\\").replace(os.getcwd(),"").replace("\\",""))
    
    def open_detail_file(self,btn):
        if isinstance(btn,Button):
            self.details_path = filedialog.askopenfilename()
            btn.text = self.details_path.replace("/","\\").replace(os.getcwd(),"").replace("\\","")
            print(str(self.details_path).replace("/","\\").replace(os.getcwd(),"").replace("\\",""))
    
    @mainthread
    def create_row(self, *args):
        print("Inside create_row")        
        # Get the id of the window
        posts_container = self.ids.testing
        
        # Create box layout
        details = BoxLayout(size_hint_y=None,height=30,pos_hint={'top': 1})
        posts_container.add_widget(details)                        
        
        # Details
        index = Label(text=str(args[0]+1),size_hint_x=.1,color=(.06,.45,.45,1))
        name = Label(text=args[1],size_hint_x=.1,color=(.06,.45,.45,1))
        Message = Label(text='0.00',size_hint_x=.2,color=(.06,.45,.45,1))
        Link = Label(text='0.00',size_hint_x=.1,color=(.06,.45,.45,1))
        Img_Path = Label(text='0.00',size_hint_x=.1,color=(.06,.45,.45,1))
        Vid_Path = Label(text='0.00',size_hint_x=.1,color=(.06,.45,.45,1))
        Vid_Title =Label(text='0.00',size_hint_x=.1,color=(.06,.45,.45,1))
        DateTime =Label(text=args[2],size_hint_x=.2,color=(.06,.45,.45,1))
        Status =Label(text=args[3],size_hint_x=.1,color=(.06,.45,.45,1))
        
        # Add Widget
        details.add_widget(index)
        details.add_widget(name)
        details.add_widget(Message)
        details.add_widget(Link)
        details.add_widget(Img_Path)
        details.add_widget(Vid_Path)
        details.add_widget(Vid_Title)
        details.add_widget(DateTime)
        details.add_widget(Status)

    def start_new_thread(self,btn):
    	threading.Thread(target=self.publish_post, args=(btn,)).start()
    	

    def publish_post(self,btn):
        if isinstance(btn,Button):
            threads=[]
            posts_container = self.ids.testing
            
            # post_to_wall(self.details_path,self.post_path)
            # Get the users details from csv file
            details_df = pd.read_csv(self.details_path)

            email = details_df.loc[0][0]
            password = details_df.loc[0][1]
            client_id= details_df.loc[0][2]

            # Get access token
            access_token = get_user_access_token(email,password,client_id)

            # Load post data
            post_df= pd.read_csv(self.post_path).fillna(value= '')

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

                if 'id' in status_dict.keys():
                    print('Success')
                    Status='Success'
                else:
                    print(status_dict['error']['message'])
                    Status='Error'
                
                # Update in main thread
                self.create_row(index,row[0],row[-1],Status)
                # t = threading.Thread(target=self.create_row, args=[index,row[0],row[-1],Status])
                # t.start()
                # threads.append(t)
                # details = BoxLayout(size_hint_y=None,height=30,pos_hint={'top': 1})
                # posts_container.add_widget(details)                        
                # index = Label(text=str(index+1),size_hint_x=.1,color=(.06,.45,.45,1))
                # name = Label(text=row[0],size_hint_x=.1,color=(.06,.45,.45,1))
                # Message = Label(text='0.00',size_hint_x=.2,color=(.06,.45,.45,1))
                # Link = Label(text='0.00',size_hint_x=.1,color=(.06,.45,.45,1))
                # Img_Path = Label(text='0.00',size_hint_x=.1,color=(.06,.45,.45,1))
                # Vid_Path = Label(text='0.00',size_hint_x=.1,color=(.06,.45,.45,1))
                # Vid_Title =Label(text='0.00',size_hint_x=.1,color=(.06,.45,.45,1))
                # DateTime =Label(text=row[-1],size_hint_x=.2,color=(.06,.45,.45,1))
                # Status =Label(text=Status,size_hint_x=.1,color=(.06,.45,.45,1))
                

                # details.add_widget(index)
                # details.add_widget(name)
                # details.add_widget(Message)
                # details.add_widget(Link)
                # details.add_widget(Img_Path)
                # details.add_widget(Vid_Path)
                # details.add_widget(Vid_Title)
                # details.add_widget(DateTime)
                # details.add_widget(Status)
            # for thread in threads:
            #     thread.join()
                
       
            
    
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