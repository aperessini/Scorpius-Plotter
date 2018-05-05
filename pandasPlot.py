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
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Button(Widget):
    pass


class GraphSession(Widget):
    def __init__(self):
        super(GraphSession, self).__init__()

    graph_now =  ObjectProperty(None)

    def create_graph(self, buttonClicked):
        df = self.readFile(self)
#  I'd prefer to use the following line, but it doesn't work for
#  some reason.  I don't know why.  So using the text attribute
#  instead seems to be a workaround that functions.
#        if buttonClicked.id == 'line_graph':
        if buttonClicked.text == 'Click me to create a line graph':
            df.plot(x=['Date/Time'], y=[' Uptime-hostname:port'])
            plt.show()
        elif buttonClicked.text == 'Click me to create a scatter graph':
            df.plot.scatter(x=[' Used JVM Mem-hostname:port'], y=[' JVM Process Cpu Load-hostname:port'])
            plt.show()
        elif buttonClicked.text == 'Click me to create a bar graph':
            #  With thanks to stackoverflow 21331722
            df.groupby([df[' Loaded Class Count-hostname:port']]).count().plot(kind='bar')
            plt.show()
        else:
            pass

    def readFile(self, df):
        return pd.read_csv("input/Tomcat.csv")

class GraphApp(App):
    def build(self):
        session = GraphSession()
        return session


if __name__ == "__main__":
    GraphApp().run()
