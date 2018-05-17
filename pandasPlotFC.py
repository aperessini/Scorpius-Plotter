#  This is a demo program, written by team Scorpius for CS 467, Capstone
#  Team members:  John Carrabino, Aaron Peressini, Cheryl Freeman
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
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
from plotter_class import PyPlotter

class GraphSession(Widget):
    
    welcome_text = ("Welcome to Scorpius Plotter, a graphing application."
                    " You can select your input data, customize, preview, and"
                    " save your graphs.")
    prompt_for_filename = "Please select the file containing the data you wish to graph."
    prompt_for_x_axis = "Please select the column of data you wish to use for your graph's x-axis."
    prompt_for_y_ayis = "Please select the column of data you wish to use for your graph's y-ayis."
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
        """ Dynamically construct the next pop-up screen """
        self.cur_axis = axis

        #  This will hold all the other elements
        chooseAxisScreen = FloatLayout()

        #  Inside of the float layout, we'll have a grid layout
        headerButtons = GridLayout(
                cols=2, size_hint_y=0.7, size_hint_x=0.9, 
                pos_hint={'x': 0.05, 'top': 0.9})
        chooseAxisScreen.add_widget(headerButtons)

        #  and 2 labels which appear when the user doesn't make a selection
        x_axis_missing = Label(
                color = (1.0, .27, 0.0, 1.0), 
                pos_hint = {'x': 0.15, 'y': 0.01}, size_hint_y = 0.1, 
                size_hint_x = 0.5)
        chooseAxisScreen.add_widget(x_axis_missing)
        y_axis_missing = Label(color = (1.0, .27, 0.0, 1.0), 
                pos_hint = {'x': 0.15, 'y': 0.01}, size_hint_y = 0.1, 
                size_hint_x = 0.5)
        chooseAxisScreen.add_widget(y_axis_missing)

        #  and a "Next" button
        #  Thanks to https://stackoverflow.com/questions/12368390
        #  for help with the lambda
        #  Setting on_press is not passing a callback to the button,
        #  but actually executing the function.
        #  Passing in an unnamed lambda function will call the
        #  desired function when the on_press event is raised
        #  Thanks to https://stackoverflow.com/questions/16215045
        #  for help with the throw-away argument _
        nextButton = Button(
                text = 'Next', size_hint_y=0.15, size_hint_x=0.2, 
                pos_hint={'x': 0.79, 'y': 0.01}, 
                on_press = lambda _: self.ensureInput(
                    self.x_axis, self.prompt_for_x_axis, x_axis_missing, 'y')) 
        chooseAxisScreen.add_widget(nextButton)

#        print self.headers
        for header in self.headers:
            btn = Button(text=header)
            btn.bind(on_press=self.assign_header)
            headerButtons.add_widget(btn)
        content = chooseAxisScreen
        title = 'Select your ' + self.cur_axis + '-axis'
        self.popup = Popup(content=content, title=title, size_hint=(1.0, 1.0))
        self.popup.open()

    def ensureInput(
            self, data_needed, input_is_missing_msg, label_to_appear, 
            next_axis):
        if (data_needed != ''):
            if (data_needed == self.filename):
                self.headers = self.plotter.get_headers(self.filename)
                self.header_choices(next_axis)
                label_to_appear.text = ''
            elif (data_needed == self.x_axis):
                self.ids.sm.current = 'screenX'
                self.popup.dismiss() 
        else:
            label_to_appear.text = input_is_missing_msg

    def print_axis(self, axis):
        if axis == 'x':
            print self.x_axis
        elif axis == 'y':
            print self.y_axis


    def clear_previous_selections(self):
        """  We need this because a user might select a file and
             x-axis, then go back and change their data file.
             The previous axes chosen need to be erased.
        """
        self.headers = []
        self.filename = ''
        self.x_axis = ''
        self.y_axis = ''


    def create_graph(self, buttonClicked):  
        df = self.readFile(self)
        print df

#  I'd prefer to use the following line, but it doesn't work for
#  some reason.  I don't know why.  So using the text attribute
#  instead seems to be a workaround that functions.
#        if buttonClicked.id == 'line_graph':
        if buttonClicked.text == 'Line Graph':
            df.plot(x=[self.x_axis], y=[self.y_axis])
            plt.show()
        elif buttonClicked.text == 'Scatter Graph':
            #x = df[self.x_axis]
            #y = df[self.y_axis]
            #plt.scatter(x, y)
            df.plot.scatter(x=[self.x_axis], y=[self.y_axis]) #'Date/Time' is not in index error
            plt.show()
        elif buttonClicked.text == 'Bar Graph\n(hardcoded)':
            #  With thanks to stackoverflow 21331722
            df.groupby([df[' Loaded Class Count-hostname:port']]).count().plot(kind='bar')  #self.x_axis 
            plt.show()
        else:
            pass

    def readFile(self, df):
        return pd.read_csv(self.filename)
    
class GraphApp(App):
    def build(self):
        session = GraphSession()
        return session


if __name__ == "__main__":
    GraphApp().run()
