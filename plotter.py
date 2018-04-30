#!/usr/bin/env python
import os
import sys
import csv
import time
import logging
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from shutil import copyfileobj
import pdb

pwd = os.path.dirname(os.path.realpath(__file__))

CSV_EXT = '.csv'
TAB_EXT = '.tab'
DELIMS = ['CSV','TAB']

GRAPH_TYPE = ['line','scatter','bar']
INTERVALS = ['second', 'minute', 'hour', 'day', 'week', 'month', 'year']
timestr = time.strftime("%Y-%m-%d_%H%M")

def main():
    plotter = PyPlotter()
    plotter.run()
    sys.exit(0)
    
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
    
    # If they choose to edit their graph, they will be given the original options 
    # listed above, as well as additional parameters below
    graph_position = {'left':0, 'bottom':0, 'width':0, 'height':0}
    title_position = {'x_y':[], 'width':10, 'height':3}
    padding = {'left':0.125, 'right':0.9, 'bottom':0.1, 'top':0.9, 'wspace':0.2, 'hspace':0.2}
    
    # After selecting continue, the user should be prompted to check if they
    # want to make another graph from the same file, or move on to the next file.
    

class PyPlotter():
    def __init__(self):
        self.headers = dict()
        self.x_axis = list()
        self.y_axis = list()
        self.x_axis_names = list()
        self.y_axis_names = list()
        self.axis_titles = {'y':'Y', 'x':'X'}
        
        self.graph_type = 'line'
        self.delimiter = ''
        self.interval = ''        
    
        self.input_dir = os.path.join(pwd, 'input')
        self.output_dir = os.path.join(pwd, 'output')
        self.err_dir = os.path.join(pwd, 'error_logs')
        self.err_file = os.path.join(self.err_dir, '%s.err' % timestr)
        
        logging.basicConfig(filename=self.err_file, level=logging.DEBUG, format='%(asctime)s|%(levelname)s|%(message)s')
        logging.info("TEST")
        
        validInput = raw_input("Did you place the tab/csv files that you wish to graph in the input directory?\n%s\n (Y/N): " % str(self.input_dir))
        if validInput.strip().lower() != 'y':
            print("All graphs must be placed in %s before running the demo. Goodbye!" % str(self.input_dir))
            sys.exit(0)
            
        self.input_files = [x for x in os.listdir(self.input_dir) if x.endswith(".csv") or x.endswith(".tab")]
        logging.info(str(self.input_files))
        
    def run(self):
        for file in self.input_files:
            os.system('cls')
            file = os.path.join(self.input_dir, file)
            self.choose_headers(file)
            self.get_delimiter(file)
            self.get_type(file)
            self.get_interval(file)
    
    def choose_headers(self, file):
        menu = ["Select your x-axis for %s\n" % file,
                "Select your y-axis from %s\n" % file]
        error = "Sorry, %s, is not a valid option\n" % file
        error += "Enter the number of the header you want to graph,\n"   
        error += "or press 'q' to quit.\n"  
        headers = self.get_headers(file)
        self.get_input(file, menu, error, headers, 'choose_headers')
    
    def get_delimiter(self, file):
        menu = ["Select your delimiter for %s\n" % file]
        error = "Sorry, %s, is not a valid option\n" % file
        error += "Enter the number of file-type,\n"   
        error += "or press 'q' to quit.\n"    
        self.get_input(file, menu, error, DELIMS, 'get_delimiter') 
    
    def get_type(self, file):
        menu = ["Select graph type for %s\n" % file]
        error = "Sorry, %s, is not a valid option\n" % file
        error += "Enter the number of the graph type you want,\n"   
        error += "or press 'q' to quit.\n" 
        self.get_input(file, menu, error, GRAPH_TYPE, 'get_type')    
    
    def get_interval(self, file):
        menu = ["Select the time interval between the rows in %s\n" % file]
        error = "Sorry, %s, is not a valid option\n" % file
        error += "Enter the number of the header you want to graph,\n"   
        error += "or press 'q' to quit.\n" 
        self.get_input(file, menu, error, INTERVALS, 'get_interval')
        
    def get_input(self, file, menu, error, special = None, func = None):
        msg = "(%s) %s\n"
        choice = 0 #len(menu)
        opt_count = 0
        while choice < len(menu): #> 0:
            for option in menu:
                choice += 1
                print "CHOICE " + str(choice)
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
                    print error
                    logging.error(error)
                    sys.exit(1)
                else:
                    count = int(user_input)
                    print 'You chose #%d %s\n' % (count, special[count-1])
                    if func == 'get_delimiter':
                        self.delimiter = special[count-1]
                    elif func == 'get_type':
                        self.graph_type = special[count-1]                        
                    elif func == 'get_interval':
                        self.interval = special[count-1]
                    elif func == 'choose_headers':
                        if opt_count == 1:
                            self.x_axis = special[count-1]
                        else:
                            self.y_axis = special[count-1]
                    else: 
                        logging.error("Something went awry...")
                        sys.exit(1)
                
                
    
    def get_headers(self, fName):
        with open(fName,'r+') as f:
            headers = f.readline()
        headers = headers.split(',')
        headers = [x.strip() for x in headers if len(x.strip()) > 0]
        return headers 
        
    def normalizeCSVs(self, logFiles, outDir, inDir, errDir, delim):   
        for file in logFiles:
            if len(file.split('_')) == 1:
                if file.split('.')[-1] == 'csv':
                    fName = file.split('.csv')[0]                
                    try:
                        log = csv.reader(open(os.path.join(inDir,file), 'r+'))
                        log = list(log)
                        with open(os.path.join(inDir,file), 'r+') as logFile:        
                            i = 0
                            for x in logFile:
                                if i == 0:
                                    header = x 
                                    lng = len(header.split(','))
                                    
                                    errorStr = ',' * (lng-2)  + '\n'
                                if i == 1:  
                                    if len(log[i]) == lng:
                                        wFile = os.path.join(inDir,'%s_CLEAN.csv' % (fName))
                                        writeFile = open(wFile, 'w+')
                                        writeFile.write(header)                 
                                        writeFile.write(x)
                                    else:
                                        err = str(log[i][0]) + errorStr
                                        wFile = '%s_CLEAN.csv' % (fName)
                                        writeFile = open(wFile, 'w+')
                                        writeFile.write(header)
                                        writeFile.write(err)                  
                                elif i > 1:
                                    if len(log[i]) == lng:
                                        writeFile.write(x)
                                       
                                    else:
                                        err = str(log[i][0]) + errorStr
                                        writeFile.write(err)
                                i+=1
                            writeFile.close()
                            wFile = os.path.join(inDir,'%s_CLEAN.csv' % (fName))
                            with open(os.path.join(inDir,file), 'w') as output, open (wFile, 'r') as input:
                                copyfileobj(input,output)
                            os.remove(wFile)
                    except Exception as e:
                        errFile = os.path.join(errDir, '%s_Error.log' % file)
                        with open(errFile, 'w+') as err:
                            err.write("ERROR: %s" % sr(e))
                            err.write('%s file not located' % file)
            else:
                pass

    def parse_loge(self, logFiles, outDir, inDir, errDir):
        for file in logFiles:
            if len(file.split('_')) == 1:
                if file.split('.')[-1] == 'csv':
                    fName = file.split('.csv')[0]
                    logDir = os.path.join(outDir, fName + '_dailyLogs')
                    try:
                        os.makedirs(logDir)
                    except:
                        pass
                    try:
                        log = csv.reader(open(os.path.join(inDir,file), 'r+'))
                        log = list(log)
                        with open(os.path.join(inDir,file), 'r+') as logFile:  
                            i=0
                            for x in logFile:
                                if i ==0:
                                    header = x
                                    pass
                                if i == 1:
                                    prevDate = x.split(',')[0]
                                    prevDate = prevDate.split(' ')[0]
                                    wFile = os.path.join(logDir,'%s_%s.csv' % (fName,prevDate.replace('/','_')))
                                    writeFile = open(wFile, 'w+')
                                    writeFile.write(header)
                                    writeFile.write(x) 
                                if i > 1:                
                                    date = x.split(',')[0]
                                    date = date.split(' ')[0]
                                    if date == prevDate:
                                        wFile = os.path.join(logDir,'%s_%s.csv' % (fName,prevDate.replace('/','_')))
                                        writeFile.write(x)                                
                                    else:
                                        writeFile.close()
                                        prevDate = date 
                                        wFile = os.path.join(logDir,'%s_%s.csv' % (fName,prevDate.replace('/','_')))
                                        writeFile = open(wFile, 'w+')
                                        writeFile.write(header)
                                        writeFile.write(x) 
                                i+=1
                            writeFile.close()
                    except Exception as e:
                        errFile = os.path.join(errDir, '%s_Error.log' % file)
                        with open(errFile, 'w+') as err:
                            err.write("ERROR: %s" % sr(e))
                            err.write('%s file not located' % file)
            else:
                pass    
        
    def plot_it(self):
        pass


if __name__ == "__main__":
    main()