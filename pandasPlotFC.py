#  This is a demo program, written by team Scorpius for CS 467, Capstone
#  Team members:  John Carrabino, Aaron Peressini, Cheryl Freeman
#  
#  The intent is, that this file will read in data from a hard-coded
#  data file, prompt the user for some data (possibly graph title
#  and/or axis titles), and then graph the data.  The goal is to
#  graph the data using pandas, using different columns of the data
#  file to do a scatter plot, a line plot, and a bar plot.
#  
#  Kivy is used to prompt the user.  The kivy file that accompanies this
#  contains the gui info.
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
from plotter_class import PyPlotter

#class Button(Widget):
 #   pass


class GraphSession(Widget):
    
    #asdf = PyPlotter()
    welcome_text = ("Welcome to Scorpius Plotter, a graphing application."
                    " You can select your input data, customize, preview, and"
                    " save your graphs.")
    x_axis = StringProperty('')
    y_axis = StringProperty('')

    def __init__(self):
        self.cur_axis = ''
        self.cwd = os.getcwd()
        self.headers = []
        self.filename = ''
        self.x_axis = ''
        self.y_axis = ''
        self.path = self.cwd + "\input"
        self.plotter = PyPlotter()
        super(GraphSession, self).__init__()

    #graph_now =  ObjectProperty(None)

    def assign_header(self, btn):
        if self.cur_axis == 'x':
            self.x_axis = btn.text
            print self.x_axis
            self.ids.sm.current = 'screenX'
        elif self.cur_axis == 'y':
            self.y_axis = btn.text
            print self.y_axis
            self.ids.sm.current = 'screenY'

    def header_choices(self, axis):
        #self.headers = [x.strip() for x in self.headers if len(x.strip()) > 0]
        self.cur_axis = axis
        layout = GridLayout(cols=2)
        print self.headers
        for header in self.headers:
            btn = Button(text=header)
            btn.bind(on_press=self.assign_header)
            layout.add_widget(btn)
        layout.add_widget(Button(text='Next', on_press=lambda *args: self.popup.dismiss()))
        content = layout
        title = 'Select your ' + self.cur_axis + '-axis'
        self.popup = Popup(content=content, title=title, size_hint=(0.9, 0.9))
        self.popup.open()

    def print_axis(self, axis):
        if axis == 'x':
            print self.x_axis
        elif axis == 'y':
            print self.y_axis


    def create_graph(self, buttonClicked):  
        #content = Button(text=self.filename)
        #popup = Popup(content=content)
        #popup.open()
        df = self.readFile(self)
        print df
#  I'd prefer to use the following line, but it doesn't work for
#  some reason.  I don't know why.  So using the text attribute
#  instead seems to be a workaround that functions.
#        if buttonClicked.id == 'line_graph':
        if buttonClicked.text == 'Click me to create a line graph':
            df.plot(x=[self.x_axis], y=[self.y_axis])
            plt.show()
        elif buttonClicked.text == 'Click me to create a scatter graph':
            #x = df[self.x_axis]
            #y = df[self.y_axis]
            #plt.scatter(x, y)
            df.plot.scatter(x=[self.x_axis], y=[self.y_axis]) #'Date/Time' is not in index error
            plt.show()
        elif buttonClicked.text == 'Click me to create a bar graph':
            #  With thanks to stackoverflow 21331722
            df.groupby([df[' Loaded Class Count-hostname:port']]).count().plot(kind='bar')  #self.x_axis 
            plt.show()
        else:
            pass

    def readFile(self, df):
        
        #content = FileChooserIconView(path=self.path)
        #popup = Popup(content=content)
        #popup.open()
        return pd.read_csv(self.filename)
    
class GraphApp(App):
    def build(self):
        session = GraphSession()
        return session


if __name__ == "__main__":
    GraphApp().run()
