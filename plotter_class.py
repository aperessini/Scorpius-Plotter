#!/usr/bin/env python
import os
import sys, pdb
import csv
import time
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shutil import copyfileobj, rmtree
import pdb

pwd = os.path.dirname(os.path.realpath(__file__))

CSV_EXT = '.csv'
TAB_EXT = '.tab'
DELIMS = ['CSV','TAB']

GRAPH_TYPE = ['line','bar'] #,'scatter']
INTERVALS = ['second', 'minute', 'hour', 'day']
PARSER = ['daily', 'weekly', 'monthly', 'N/A (produces single graph)']
INTERVALS_PER_DAY = {'second':86400,'minute':1440,'hour':24, 'day':1}
INTERVALS_PER_WEEK = {'second':604800,'minute':10080,'hour':168, 'day':7}
INTERVALS_PER_MONTH = {'second':2592000,'minute':43800,'hour':730, 'day':30}
timestr = time.strftime("%Y-%m-%d_%H%M")

def main():
#    plotter = PyPlotter()
#    plotter.run()
#    sys.exit(0)
    pass
    
class toPlot():
    # These values will be calculated when GUI boots up by plotter.py
    # Plotter will return list of input file to user
    # User will go through each graph one-by-one selecting options
    # Plotter will return a list of headers from each graph as well
    # Axes can be chosen from header list.     
    file = ''
    headers = []
    
    # When going through each file user will specify the following values
    # After this information is obtained the used can preview a demo graph 
    # After viewing preview they will be given option to change values or continue
    x_axis = ''
    y_axis = []
    y_label = {'label':'', 'fontsize':10}
    x_label = {'label':'', 'fontsize':10}
    legend = {'legend':False, 'location':'upper center', 'bbox_to_anchor':[0.44, -0.29], 'ncol':2, 'fontsize':9}
    graph_options = {'type':'line', 'stacked':False, 'title':'', 'alpha':0.7}
    interval_bxn_rows = '' # sec,min,hr,day,month,year
    parser = '' # daily/weekly/monthly/annual/ or None for a single graph    
    
    #JUST ADDED 5/6
    delimiter = ''
    
    # If they choose to edit their graph, they will be given the original options 
    # listed above, as well as additional parameters below
    graph_position = {'left':0, 'bottom':0, 'width':0, 'height':0}
    title_position = {'x_y':[], 'width':10, 'height':3}
    padding = {'left':0.125, 'right':0.9, 'bottom':0.1, 'top':0.9, 'wspace':0.2, 'hspace':0.2}
    
    # After selecting continue, the user should be prompted to check if they
    # want to make another graph from the same file, or move on to the next file.
    

class PyPlotter():
    def __init__(self):
        self.pltr = toPlot()
        self.input_dir = os.path.join(pwd, 'input')
        self.output_dir = os.path.join(pwd, 'output')
        self.err_dir = os.path.join(pwd, 'error_logs')
        self.err_file = os.path.join(self.err_dir, '%s.err' % timestr)
          
        plt.rcParams.update({'figure.max_open_warning': 0})  
        logging.basicConfig(filename=self.err_file, level=logging.DEBUG, format='%(asctime)s|%(levelname)s|%(message)s')
        
#        validInput = raw_input("Did you place the tab/csv files that you wish to graph in the input directory?\n%s\n (Y/N): " % str(self.input_dir))
#        if validInput.strip().lower() != 'y':
#            print("All input files must be placed in %s before running the demo. Goodbye!" % str(self.input_dir))
#            sys.exit(0)
            
        self.input_files = [x for x in os.listdir(self.input_dir) if x.endswith(".csv") or x.endswith(".tab")]
        logging.info(str(self.input_files))
        
    def run(self):
        for file in self.input_files:
            self.pltr = toPlot()
            self.pltr.y_axis = []
                                  
            os.system('cls')
            file = os.path.join(self.input_dir, file)
            self.normalizeCSV(file)
            self.choose_headers(file)
            self.get_labels(file)
            self.get_delimiter(file)
            self.get_type(file)
            self.get_interval(file)
            self.get_parser(file)
            self.parse_logs(file)
            self.plot_it_preview(file)
            self.finalize_graph(file)
    
    def choose_headers(self, file):
        menu = ["Select your x-axis for %s\n" % file,
                "Select your y-axis from %s\n" % file]
        error = "Sorry, %s, is not a valid option\n"
        error += "Enter the number of the header you want to graph,\n"   
        error += "or press 'q' to quit.\n"  
        self.pltr.headers = self.get_headers(file)
        self.get_input(file, menu, error, self.pltr.headers, 'choose_headers')
    
    def get_delimiter(self, file):
        menu = ["Select your delimiter for %s\n" % file]
        error = "Sorry, %s, is not a valid option\n" 
        error += "Enter the number of file-type,\n"   
        error += "or press 'q' to quit.\n"    
        self.get_input(file, menu, error, DELIMS, 'get_delimiter') 
    
    def get_type(self, file):
        menu = ["Select graph type for %s\n" % file]
        error = "Sorry, %s, is not a valid option\n" 
        error += "Enter the number of the graph type you want,\n"   
        error += "or press 'q' to quit.\n" 
        self.get_input(file, menu, error, GRAPH_TYPE, 'get_type')    
    
    def get_interval(self, file):
        menu = ["Select the time interval between the rows in %s\n" % file]
        error = "Sorry, %s, is not a valid option\n" 
        error += "Enter the number of the header you want to graph,\n"   
        error += "or press 'q' to quit.\n" 
        self.get_input(file, menu, error, INTERVALS, 'get_interval')
        
    def get_parser(self,file):
        menu = ["Select the time interval to parse the graphs from file %s" % file]
        error = "Sorry, %s, is not a valid option\n" 
        error += "Enter the time interval to parse each graph,\n"   
        error += "or press 'q' to quit.\n" 
        self.get_input(file, menu, error, PARSER, 'get_parser')
        
    def get_labels(self, file):
        menu = ["Choose a title for your x-axis",
                "Choose a title for your y-axis",
                "Choose a title for your graph"]
        for item in menu:
            os.system('cls')
            print item
            user_input = raw_input("\n>> ")
            user_input = user_input.strip()
            if 'x-axis' in item:
                self.pltr.x_label['label'] = user_input
            elif 'y-axis' in item:
                self.pltr.y_label['label'] = user_input            
            else: 
                self.pltr.graph_options['title'] = user_input
    
    def get_input(self, file, menu, error, special = None, func = None):
        msg = "(%s) %s\n"
        choice = 0 #len(menu)
        opt_count = 0
        while choice < len(menu): #> 0:
            os.system('cls')
            for option in menu:
                choice += 1 #-= 1
                print "CHOICE " + str(choice) + ': %s\n' % str(special[choice-1])
                os.system('cls')
                opt_count += 1
                print option
                num = 0
                for count, item in enumerate(special, 1):
                    print msg % (count, item)
                    num = count
                user_input = raw_input("\n>> ")
                user_input = user_input.strip()
                
                if user_input.lower() == 'q':
                    print 'Goodbye!'
                    sys.exit(0)
                elif int(user_input) < 1 or int(user_input) > num:  
                    if func == 'get_axis_names' or func == 'get_title':
                        print("FIX THIS")
                        sys.exit(1)
                    else:
                        print(error % user_input)
                        logging.error(error % user_input)
                        sys.exit(1)
                else:
                    count = int(user_input)
                    print 'You chose #%d %s\n' % (count, special[count-1])
                    if func == 'get_delimiter':
                        self.pltr.delimiter = special[count-1]
                    elif func == 'get_type':
                        self.pltr.graph_options['type'] = special[count-1]                        
                    elif func == 'get_interval':
                        self.pltr.interval_bxn_rows = special[count-1]                       
                    elif func == 'get_parser':
                        self.pltr.parser = special[count-1]
                    elif func == 'choose_headers':
                        if opt_count == 1:
                            self.pltr.x_axis = special[count-1].strip()
                        else:
                            self.pltr.y_axis.append(special[count-1].strip())
                            cont = 1
                            while(cont != 0):
                                print "Would you like to add another data set to the Y-axis?\n"
                                print "(1) Yes\n(2) No\n"
                                y_choice = raw_input("\n>> ")
                                y_choice = int(y_choice.strip())
                                if y_choice == 1:
                                    print option
                                    num = 0
                                    for count, item in enumerate(special, 1):
                                        print msg % (count, item)
                                        num = count
                                    user_input = raw_input("\n>> ")
                                    user_input = user_input.strip()
                                    
                                    if user_input.lower() == 'q':
                                        print 'Goodbye!'
                                        sys.exit(0)
                                    elif user_input == '':
                                        print "Sorry, %s is not a valid option, try again.\n" % str(y_choice)
                                        logging.error("Sorry, %s is not a valid option, try again.\n" % str(y_choice))
                                        sys.exit(1)
                                    elif int(user_input) < 1 or int(user_input) > num:
                                        print(error % user_input)
                                        logging.error(error % user_input)
                                        sys.exit(1)
                                    else:
                                        self.pltr.y_axis.append(special[int(user_input)-1].strip())
                                elif y_choice == 2:
                                    cont = 0
                                else:
                                    print "Sorry, %s is not a valid option, try again.\n" % str(y_choice)
                                    logging.error("Sorry, %s is not a valid option, try again.\n" % str(y_choice))
                                    sys.exit(1)
                                    
                    else: 
                        logging.error("Something went awry...")
                        sys.exit(1)
                
    def finalize_graph(self, file):
        menu = "Would you like to change the appearance of your graph? (Y/N)"
        flag = 1
        while flag != 0:
            os.system('cls')
            print menu
            user_input = raw_input("\n>> ")
            user_input = user_input.strip()
            if 'y' in user_input.lower():
                flag = 0
                # Give user options to alter graph appearance.
                pass
            elif 'n' in user_input.lower():
                flag = 0  
                fName = os.path.basename(file)   
                fName = fName.split('.')[0]
                self.make_graphs(fName)
            elif 'q' in user_input.lower():
                flag = 0
                print "Goodbye!"
                sys.exit(0)
            else: 
                print"\nSorry, %s is not a valid option,\n Enter Y/N or q to quit"
    
    def get_headers(self, fName, delim):
        with open(fName,'rU+') as f:
            headers = f.readline()
            #  The lines below:  if parse_dates is not specified as column 0,
            #  and index_col is set to False, then it will import the first column
            #  as a data column.
#            df = pd.read_csv(f, sep=delim, index_col=False)
#            sdfdf = pd.read_csv(f, sep=delim, parse_dates=[0], index_col=False)
        headers = headers.split(delim)
        headers = [x.strip('\xef\xbb\xbf') for x in headers if len(x.strip()) > 0]
        headers = [x.strip() for x in headers if len(x.strip()) > 0]
        return headers
        
    def normalizeCSV(self, file, delim):   
        fName = os.path.basename(file)   
#        fName = fName.split('.')[0]
        fName, fExtension = fName.split('.')
        try:
            log = csv.reader(open(file, 'rU+'))
            log = list(log)
            with open(file, 'rb+') as logFile:  
                for i, x in enumerate(logFile):
                    if i == 0:
                        header = x 
                        lng = len(header.split(delim))
                        errorStr = delim * (lng-2)  + '\n'
                    if i == 1:  
                        if len(x.split(delim)) == lng:
                            wFile = os.path.join(self.input_dir,'%s_CLEAN.csv' % (fName))
                            writeFile = open(wFile, 'wb+')
                            writeFile.write(header)                 
                            writeFile.write(x)
                        else:
                            err = str(log[i][0]) + errorStr
                            wFile = '%s_CLEAN.csv' % (fName)
                            writeFile = open(wFile, 'wb+')
                            writeFile.write(header)
                            writeFile.write(err)                  
                    elif i > 1:
                        if len(x.split(delim)) == lng:
                            writeFile.write(x)
                        else:
                            err = str(log[i][0]) + errorStr
                            writeFile.write(err)
                writeFile.close()
                # pdb.set_trace()
                wFile = os.path.join(self.input_dir,'%s_CLEAN.csv' % (fName))
                with open(file, 'wb') as output, open (wFile, 'rb') as input:
                    copyfileobj(input,output)
                os.remove(wFile)
        except Exception as e:
            print "Error normalizing %s.\n Error Message: %s" % (str(fName), str(e))
            logging.error("Error normalizing %s.\n Error Message: %s" % (str(self.err_dir), str(e)))
            sys.exit(1)
           
                
    def parse_logs(self,file):
        interval = self.pltr.interval_bxn_rows
        parser = self.pltr.parser 
        cut_off = 0
        fName = os.path.basename(file)  
        fName = fName.split('.')[0]
        
        if (self.pltr.parser) != '' and (self.pltr.parser) != 'N/A (produces single graph)':
            log_dir = os.path.join(self.output_dir,fName + '_' + parser + '_logs')
        else: 
            self.pltr.parser = ''
            log_dir = os.path.join(self.output_dir,fName + '_logs')
        
        if os.path.isdir(log_dir):
            pass 
        else:
            try:
                os.makedirs(log_dir)
            except Exception as e:
                print "Error creating %s directory.\n Error Message: %s" % (str(log_dir), str(e))
                logging.error("Error creating %s directory.\n Error Message: %s" % (str(self.err_dir), str(e)))
                sys.exit(1)

        if parser == 'daily':
            if interval == 'second': cut_off = INTERVALS_PER_DAY['second']
            elif interval == 'minute': cut_off = INTERVALS_PER_DAY['minute']
            elif interval == 'hour': cut_off = INTERVALS_PER_DAY['hour']
            elif interval == 'daily': cut_off = INTERVALS_PER_DAY['day']
            LIMIT = 1
        elif parser == 'weekly':
            if interval == 'second': cut_off = INTERVALS_PER_WEEK['second']
            elif interval == 'minute': cut_off = INTERVALS_PER_WEEK['minute']
            elif interval == 'hour': cut_off = INTERVALS_PER_WEEK['hour']
            elif interval == 'daily': cut_off = INTERVALS_PER_WEEK['day']
            LIMIT = 7
        
        elif parser == 'monthly':
            if interval == 'second': cut_off = INTERVALS_PER_MONTH['second']
            elif interval == 'minute': cut_off = INTERVALS_PER_MONTH['minute']
            elif interval == 'hour': cut_off = INTERVALS_PER_MONTH['hour']
            elif interval == 'daily': cut_off = INTERVALS_PER_MONTH['day']
            LIMIT = 30        
        else:
            LIMIT = cut_off = -1
        
        try:
            log = csv.reader(open(file, 'rU+'))
            log = list(log)
            with open(file, 'rU+') as logFile: 
                cut_off_count = 0
                day_count = 1
                for i, x in enumerate(logFile):
                    if i ==0:
                        header = x                        
                    if i == 1:
                        prevDate = log[i][0]
                        #pdb.set_trace()
                        prevDate = prevDate.replace(' ','_').replace(':','')
                        for item in log[i][0].split(' '):
                            if '-' in item:
                                prevDay = item
                        wFile = os.path.join(log_dir,'%s_%s.csv' % (fName,prevDay.replace('/','')))
                        writeFile = open(wFile, 'wb+')
                        writeFile.write(header)
                        writeFile.write(x) 
                    if i > 1:                
                        date = log[i][0]
                        date = date.replace(' ','_').replace(':','')
                        for item in log[i][0].split(' '):
                            if '-' in item:
                                currDay = item
                        if currDay != prevDay:
                            prevDay = currDay
                            day_count += 1
                        if (cut_off_count+1) != cut_off and day_count != LIMIT:
                            #append to existing log file 
                            wFile = os.path.join(log_dir,'%s_%s.csv' % (fName,prevDay.replace('/','')))
                            writeFile.write(x)
                            cut_off_count += 1
                            
                        else:
                            # write new logfile
                            writeFile.close()
                            prevDate = date 
                            wFile = os.path.join(log_dir,'%s_%s.csv' % (fName,prevDay.replace('/','')))
                            writeFile = open(wFile, 'wb+')
                            writeFile.write(header)
                            writeFile.write(x) 
                            cut_off_count = 0
                            day_count = 0                    
                writeFile.close()    
        
        except Exception as e:
            print "Error parsing %s.\n Error Message: %s" % (str(fName), str(e))
            logging.error("Error parsing %s.\n Error Message: %s" % (str(self.err_dir), str(e)))
            sys.exit(1)
        
    def plot_it_preview(self, file):
        fName = os.path.basename(file)  
        fName = fName.split('.')[0]

        #Plots graph based on x and y axis inputs
        #First col of the file has to be date/time for now
        if self.pltr.delimiter == 'CSV':
            delim = ','
        else:
            delim = '\t'
            
        df = pd.read_csv(file, sep=delim, skipinitialspace=True, parse_dates=[0])
        length = len(self.pltr.y_axis)
        #pdb.set_trace()
        
        if length == 1:
            plot_it = df[[self.pltr.x_axis, self.pltr.y_axis[0]]]
        else:
            to_plot = [self.pltr.x_axis]
            for count,y in enumerate(self.pltr.y_axis):
                to_plot.append(self.pltr.y_axis[count])
            plot_it = df[to_plot]
                
        plot_fig = plot_it.plot.line(stacked=self.pltr.graph_options['stacked'], title=self.pltr.graph_options['title'], x=self.pltr.x_axis, alpha=0.7)
        
        plot_fig.get_yaxis().get_major_formatter().set_scientific(True)
        
        # Shrink current axis's height by 10% on the bottom
        box = plot_fig.get_position()
        plot_fig.set_position([box.x0, box.y0 + box.height * 0.2, box.width * 0.2, box.height * 0.7])
        # Put a legend below current axis
        plot_fig.legend(loc='upper center', bbox_to_anchor=(0.44, -0.29), ncol=2,fontsize=8)
        plot_fig.set_ylabel(self.pltr.y_label['label'],fontsize=self.pltr.y_label['fontsize'])
        plot_fig.set_xlabel(self.pltr.x_label['label'],fontsize=self.pltr.x_label['fontsize'])
        
        
        fig = plot_fig.get_figure()
        fig = plt.gcf()
        fig.autofmt_xdate()
        fig.tight_layout(pad=3)
        fig.subplots_adjust(bottom=0.25)
        fig.savefig("%s_preview.png" % fName)
        plt.show()
        plt.close(fig)
        del df
     
    def make_graphs(self, fName):
        # pdb.set_trace()
        if len(self.pltr.parser)> 1:
            log_dir = os.path.join(self.output_dir,fName + '_' + self.pltr.parser + '_logs')
        else:
            log_dir = os.path.join(self.output_dir,fName + '_logs')
            
        file_list = os.listdir(log_dir)
        delim = self.pltr.delimiter
        for file in file_list:
            if file.endswith(delim.lower()):
                file = os.path.join(log_dir, file)
                self.plot_it(file)
     
    def plot_it(self, file):
        plotFile = file.replace('.csv','.png')
        #Plots graph based on x and y axis inputs
        #First col of the file has to be date/time for now
        if self.pltr.delimiter == 'CSV':
            delim = ','
        else:
            delim = '\t'
            
        df = pd.read_csv(file, sep=delim, skipinitialspace=True, parse_dates=[self.pltr.x_axis])
        if self.pltr.parser == 'daily': range = 1
        else: range = 0
        
        df[self.pltr.x_axis] = [str(d).split(' ')[range] for d in df[self.pltr.x_axis]]
        length = len(self.pltr.y_axis)
        
        if length == 1:
            plot_it = df[[self.pltr.x_axis, self.pltr.y_axis[0]]]
        else:
            to_plot = [self.pltr.x_axis]
            for count,y in enumerate(self.pltr.y_axis):
                to_plot.append(self.pltr.y_axis[count])
            plot_it = df[to_plot]
        
        if self.pltr.graph_options['type'] == 'line':
            plot_fig = plot_it.plot.line(stacked=self.pltr.graph_options['stacked'], title=self.pltr.graph_options['title'], x=self.pltr.x_axis, alpha=0.7)
        elif self.pltr.graph_options['type'] == 'scatter':
            pass # plot_fig = plot_it.plot.scatter(x=self.pltr.x_axis, y=self.pltr.y_axis, stacked=self.pltr.graph_options['stacked'], title=self.pltr.graph_options['title'],  alpha=0.7)
        elif self.pltr.graph_options['type'] == 'bar':
            plot_fig = plot_it.plot(kind='bar', x=self.pltr.x_axis, y=self.pltr.y_axis, stacked=self.pltr.graph_options['stacked'], title=self.pltr.graph_options['title'],alpha=0.7)
        
        plot_fig.get_yaxis().get_major_formatter().set_scientific(True)
        
        # Shrink current axis's height by 10% on the bottom
        box = plot_fig.get_position()
        plot_fig.set_position([box.x0, box.y0 + box.height * 0.2, box.width * 0.2, box.height * 0.7])
        # Put a legend below current axis
        plot_fig.legend(loc='upper center', bbox_to_anchor=(0.44, -0.29), ncol=2,fontsize=8)
        plot_fig.set_ylabel(self.pltr.y_label['label'],fontsize=self.pltr.y_label['fontsize'])
        plot_fig.set_xlabel(self.pltr.x_label['label'],visible=True,fontsize=self.pltr.x_label['fontsize']) 
        step = int(len(df[self.pltr.x_axis])/12)
        plt.xticks(df.index[0:-1:step], df[self.pltr.x_axis][0::step])
        
        fig = plot_fig.get_figure()
        fig = plt.gcf()
        fig.autofmt_xdate()
        fig.tight_layout(pad=3)
        fig.subplots_adjust(bottom=0.25)
        fig.savefig(plotFile)
        plt.close(fig)
        del df
        

if __name__ == "__main__":
#   main()
    plotter = PyPlotter()
    
#   plotter.run()
    sys.exit(0)
