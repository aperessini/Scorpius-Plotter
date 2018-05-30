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
from kivy.uix.checkbox import CheckBox
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
import pdb
import difflib
import datetime
from plotter_class import PyPlotter

class GraphSession(Widget):
    
    welcome_text = ("Welcome to Scorpius Plotter, a graphing application."
                    " You can select your input data, customize, preview, and"
                    " save your graphs.")
    prompt_for_filename = "Please select the file containing the data you wish to graph."
    prompt_for_x_axis = "Please select the column of data you wish to use for your graph's x-axis."
    prompt_for_y_axis = "Please select the column of data you wish to use for your graph's y-axis."
    disabled_explanation = "A scatter graph will not work with your non-numeric x-axis values."
    x_axis = StringProperty('')
    y_axis = StringProperty('')
    delim = StringProperty('')
    filename = StringProperty('')
    graph_title = StringProperty('')
    x_axis_title = StringProperty('')
    y_axis_title = StringProperty('')

    def __init__(self):
        self.cur_axis = ''
        self.cwd = os.getcwd()
        self.headers = []
        self.filename = ''
        self.x_axis = ''
        self.y_axis = ''
        self.delim = ''
        self.path = self.cwd + "\input"
        self.plotter = PyPlotter()
        super(GraphSession, self).__init__()

    def assign_header(self, btn):
        with open(self.filename, 'rU+') as f:
            df = pd.read_csv(f, sep=self.delim, index_col=False)
        btn.color = [.3, .9, .5, 1]
        non_numeric_label = self.non_numeric_axis
        buttons = self.headerButtons.children[:]
        for x in buttons:
            if x != btn:
                x.color = [0, 0, 0, 1]
        if self.cur_axis == 'x':
            self.x_axis = btn.text.encode('ascii')
#            print df[self.x_axis].dtype
            if df[self.x_axis].dtype == 'object':
                non_numeric_label.text = 'This is a non-numeric data column'
                self.ids.scatter_button.disabled = True
                self.ids.disabled_explanation.text = self.disabled_explanation
            else:
                non_numeric_label.text = ''
                self.ids.scatter_button.disabled = False
                self.ids.disabled_explanation.text = ''
            #print self.x_axis
            self.ids.sm.current = 'screenX'
        elif self.cur_axis == 'y':
            self.y_axis = btn.text.encode('ascii')
            #print self.y_axis
            self.ids.sm.current = 'screenY'

    def header_choices(self, axis):
        """ Dynamically construct the next pop-up screen """
        self.cur_axis = axis

        #  This will hold all the other elements
        self.chooseAxisScreen = FloatLayout()

        #  Inside of the float layout, we'll have a grid layout
        self.headerButtons = GridLayout(
                cols=2, size_hint_y=0.7, size_hint_x=0.9, 
                pos_hint={'x': 0.05, 'top': 0.9})
        self.chooseAxisScreen.add_widget(self.headerButtons)

        #  and a label which appears when the user doesn't make a selection
        self.axis_missing = Label(
                color = (1.0, .27, 0.0, 1.0), 
                pos_hint = {'x': 0.15, 'y': 0.01}, size_hint_y = 0.1, 
                size_hint_x = 0.5)
        self.chooseAxisScreen.add_widget(self.axis_missing)

        
        #  and a label which appears when the user selects a non-numeric
        #  axis
        self.non_numeric_axis = Label(
                color = (1.0, .27, 0.0, 1.0), 
                pos_hint = {'x': 0.15, 'y': 0.01}, size_hint_y = 0.1, 
                size_hint_x = 0.5)
        self.chooseAxisScreen.add_widget(self.non_numeric_axis)

        #  Set arguments for the Next button on_press
        if (axis == 'x'):
            self.data_needed = 'x'
            self.next_axis = 'y'
        elif (axis == 'y'):
            self.data_needed = 'y'
            self.next_axis = None

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
                    self.data_needed, self.axis_missing, self.next_axis))
        self.chooseAxisScreen.add_widget(nextButton)

#        print self.headers
        for header in self.headers:
            btn = Button(text=header)
            btn.bind(on_press=self.assign_header)   
            self.headerButtons.add_widget(btn)
        content = self.chooseAxisScreen
        title = 'Select your ' + self.cur_axis + '-axis'
        self.popup = Popup(content=content, title=title, size_hint=(1.0, 1.0))
        self.popup.open()

    def ensureInput(
            self, data_needed, label_to_appear, next_axis):
        if (data_needed == 'file'):
            contents_needed = self.filename
            input_is_missing_msg = self.prompt_for_filename
        elif (data_needed == 'x'):
            contents_needed = self.x_axis
            input_is_missing_msg = self.prompt_for_x_axis
        elif (data_needed == 'y'):
            contents_needed = self.y_axis
            input_is_missing_msg = self.prompt_for_y_axis
        else:
            print "Weird"

        if (contents_needed != ''):
            if (data_needed == 'file'):
                self.ids.sm.current = 'screenDelim'
            elif (data_needed == 'x'):
                self.ids.sm.current = 'screenX'
                self.popup.dismiss() 
            elif (data_needed == 'y'):
                self.ids.sm.current = 'screenY'
                self.popup.dismiss()
            else:
                print "not sure"
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
        self.delim = ''


    def create_graph(self, buttonClicked):  
        #
        # Trying to figure out why selecting Date/Time as x-axis
        # gives a KeyError with a scatter plot 5/21/2018
        #
        self.readFile()
        df = self.df
        print df.iloc[:,0].name
        print df.iloc[:,0]

        # THANK YOU : https://stackoverflow.com/questions/15891038/change-data-type-of-columns-in-pandas
        for x in df.columns:
            if df[x].dtype != 'datetime64[ns]':
                #print df[x].dtype
                df[x] = pd.to_numeric(df[x], errors='ignore') 
            else:
                for y in df[x]:
                    #print y
                    y = y.to_pydatetime() 
                    #print type(y)

        #df = df.apply(pd.to_numeric, errors='ignore')
        #pdb.set_trace()
        
        #if(df.columns[0] == self.x_axis):
        #    print 'poophead'
        
                

        if buttonClicked == self.ids.line_graph:
            #  Thanks to https://stackoverflow.com/questions/21487329/
            #  for the following code to set titles
            graph = df.plot(x=[self.x_axis], y=[self.y_axis])
        
        elif buttonClicked == self.ids.scatter_button:
            #Still does not work for datetime object; researching workarounds 5/23/2018; See: https://github.com/pandas-dev/pandas/issues/8113
            graph = df.plot.scatter(x=self.x_axis, y=self.y_axis) #'Date/Time' is not in index error
        
        elif buttonClicked == self.ids.bar_button:
            #  With thanks to stackoverflow 21331722
#            df.groupby([df[' Loaded Class Count-hostname:port']]).count().plot(kind='bar')  #self.x_axis 
            graph = df.plot.bar(x=self.x_axis, y=self.y_axis)

        else:
            pass
        graph.set(xlabel=self.x_axis_title, ylabel=self.y_axis_title, title=self.graph_title)
        plt.show()

    def readFile(self):
        #  This function cleans the data and puts it back in the same file
#        self.plotter.normalizeCSV(self.filename, self.delim)
        self.df = pd.read_csv(self.filename, names=self.headers, header=0, skipinitialspace=True, index_col=False, usecols=range(0, len(self.headers)), sep=self.delim, parse_dates=[0])
    
    def recordDelimiterChoice(self, grid):
#  Thanks to https://stackoverflow.com/questions/610883
        for x in grid:
            try:
                if x.active:
                    self.delim = x.name
            except AttributeError:
                pass
#        print 'The delimiter right now is ' + self.delim
        #  This function cleans the data and puts it back in the same file
        self.plotter.normalizeCSV(self.filename, self.delim)
        self.headers = self.plotter.get_headers(self.filename, self.delim)
        self.header_choices('x')


    def activateDefaultDelimiter(self, radioButtons):
        _, fileExtension = self.filename.split('.')
        if (fileExtension.upper() == 'CSV'):
            for item in radioButtons:
                try:
                    if item.name == ',':
                        item.active = True
                    else:
                        item.active = False
                except AttributeError:
                    pass
        else:
            for item in radioButtons:
                try:
                    if item.name == '\t':
                        item.active = True
                    else:
                        item.active = False
                except AttributeError:
                    pass

    def updateTextScreen(self):
        graph_hint = self.y_axis + ' versus ' + self.x_axis
        self.ids.gTitle.text = ''
        self.ids.gTitle.hint_text = str(graph_hint)
        self.ids.xTitle.text = ''
        self.ids.xTitle.hint_text = str(self.x_axis)
        self.ids.yTitle.text = ''
        self.ids.yTitle.hint_text = str(self.y_axis)


    def recordTitles(self, gridChildren):
        for item in gridChildren:
            try:
                if item.text == '':
                    item.text = item.hint_text
                if item.name == 'graph title':
                    self.graph_title = item.text
                elif item.name == 'x axis title':
                    self.x_axis_title = item.text
                elif item.name == 'y axis title':
                    self.y_axis_title = item.text
                else:
                    print 'Weird!!!'
            except AttributeError:
                pass
        self.ids.sm.current = 'screen3'

class GraphApp(App):
    def build(self):
        self.icon = 'scorpion.png'
        self.title = 'Scorpius Plotter'
        print matplotlib.__version__
        session = GraphSession()
        return session


if __name__ == "__main__":
    GraphApp().run()
