Scorpius Team
Cheryl Freeman, John Carrabino, Aaron Peressini

Python Data Plotter


# Overview

The Scorpius Python Data Plotter is a program with a graphical user interface that allows a user to select a data file, axes, titles, and graph type and then create a graph based on those selections. The program handles several common data file delimiters and has line, scatter, and bar graph capabilities. With the amazing graphical user interface, users can modify their selections at any point throughout the process before creating and displaying their graph.

# Installation

1. Extract the Scorpius.zip package
2. Open up the extracted package folder and launch “Miniconda2-latest-Windows-x86_64.exe” to install MiniConda2 onto your system.
3. During installation the following window will pop up, select the first checkbox in order to add Anaconda to the system PATH environment variable, this will allow you to use the “conda” command from the command line after installation.           
4. After successfully installing MiniConda2 on your system, open a command line,  and “cd” into the Scorpius project directory(NOTE: Windows Powershell will not work, it needs to be a command line).
5. Once in the Scorpius project dir enter the following command: 
“create -f scorpius.yml -n scorpius”
    * This will create a new Conda environment and install the pandas/matplotlib/kivy modules used for our project in that new environment.
  
6. Before running the program, you must enter your Conda environment by executing the following command: “activate scorpius”
    * This will activate your scorpius environment, you will know that your environment is activated if it prepends your command line with ({CONDA_ENV})
    * An example of what this will look like is given at the end of the installation instructions.
  
7. When you are done using the program you can simply exit out of the command line, and if you want to keep your command line window open you can simply deactivate the environment by executing the command: “deactivate” After running that command the command line will revert to normal. 
Here is an example of what the command line will look like after activating/deactivating your Conda environment,


# User Instructions

## Command Line Interface

Follow the installation instructions above.
Open a command line in the folder where the project files are located.
Type activate scorpius to activate the miniconda environment.
Type python plotter.py to execute the Command Line program.
The program will prompt the user to see if all of the log files that they want to graph are in the input directory. Enter “Y” to continue.
Now the plotter script will read in the first file and list off all of the headers for the user to choose which column they want on the x-axis.
After choosing the x-axis, the script will then enter a loop listing all of the headers and giving the user the option to add as many data sets to the y-axis as they want. 
After the x & y axes are selected the program will prompt the user to label them, as well as create a title for their graph.
Once all labels are selected the user will then be prompted to select what the delimiter of the input file is (comma, tab, etc.).
After selecting the delimiter the user will then select which type of graph they wish to make (currently only produces line graphs).
After selecting the graph type the user is then prompted to select the interval in between rows (seconds, minutes, hours, days, etc.)
Once all of the above information has been selected the script will then display a preview graph.
After exiting out of the preview window the script will give the user the option to go back and modify their graph (Currently this is not implemented, so selecting “Y” will not actually allow you to modify a graph). 
After selecting that they are satisfied with their graph the plotter will then graph the parsed log files in the output directory.  
Repeat starting at step 6 until all files in input directory have been graphed. 
After the program exits all graphs and parsed log files will be located within the output directory. 

## GUI
We have provided the following input files for you to use with our application:  
ball.csv, a small file describing Newtonian motion of a ball being thrown
ball.txt, the same file but with a tab delimiter instead
jan_atp_matches_2018.csv, a list of the Association of Tennis Professional’s matches in the first half of January 2018
FY-2011-13-Oakland_Budget_Dept-Unit-Fund_0.csv, a list of budget requests for the city of Oakland
output.txt, a tab-delimited file recording multi-threaded performance versus cache line padding
You are welcome to use your own input files, also, but they must meet certain criteria in order to avoid crashing the program:
They must have only one line of column headings
Each data column must have exactly one column heading
The data file can be located outside of the input directory (found in the same directory as our application), but some notifications to the user will show an incorrect path to the file.
They must be delimited by one of the following:  comma, tab, semicolon, or spaces (with no interior spaces in the column headings if spaces are the delimiters)

To start the application
Activate the scorpius miniconda environment, as described under “Installation”
type python pandasPlotFC.py at the prompt

To construct a line graph, using a numerical or non-numerical x-axis
Click “Next”

Select the data input file “ball.csv”, then click “Next”

Accept the default delimiter (comma) by clicking “Next”

Select “time” as the x-axis column, then click “Next”

Confirm your x-axis selection by clicking “Next”

Select “position” as the y-axis, and click “Next”

Confirm your selection by clicking “Next”

Enter your desired graph title and axes titles, or accept the defaults by clicking “Next”

Select “Line Graph”

A line graph will be displayed.  Focus will return back to the Scorpius Plotter application, but you will be unable to change your data file selection or header selection until you close the graph.

To construct a scatter graph (numerical x-axis required)
Follow steps 1-3, from above.  In step 4, select “output.txt” as your input file.
Select “Cache Line Padding” as your x-axis, and “6 threads” as your y-axis, as shown below.


Confirm your selections, select your graph and axes titles, then select “Scatter Graph”



To construct a bar graph, using a numerical x-axis
Activate the scorpius miniconda environment, as described under “Installation”
type python pandasPlotFC.py at the prompt
Click “Next”
Select the data input file “ball.txt”, then click “Next”
Accept the default delimiter (tab) by clicking “Next”
Select “position” as the x-axis column, then click “Next”
Confirm your x-axis selection by clicking “Next”
Select “velocity” as the y-axis, and click “Next”
Confirm your selection by clicking “Next”
Enter your desired graph title and axes titles, or accept the defaults by clicking “Next”
Select “Bar Graph”
A bar graph will be displayed.

To construct a bar graph, using a non-numerical x-axis
Activate the scorpius miniconda environment, as described under “Installation”
type python pandasPlotFC.py at the prompt
Click “Next”
Select the data input file “jan_atp_matches_2018.csv”, then click “Next”
Accept the default delimiter (comma) by clicking “Next”
Select “winner_name” as the x-axis column. Notice that you are informed that your x-axis selection is non-numeric, as shown below:

Click “Next”, and then confirm your x-axis selection by clicking “Next” again.
This time, because your x-axis selection is non-numeric, some of the y-axis selection buttons will be disabled (with an informative message displayed).  Select “winner_ht” as the y-axis, and click “Next”

Confirm your selection by clicking “Next”
Enter your desired graph title and axes titles, or accept the defaults by clicking “Next”
Select “Bar Graph”
A bar graph will be displayed.

To construct a bar graph, performing simple statistics on the x-axis data
Activate the scorpius miniconda environment, as described under “Installation”
type python pandasPlotFC.py at the prompt
Click “Next”
Select the data input file “FY-2011-13-Oakland_Budget_Dept-Unit-Fund_0.csv”, then click “Next”
Accept the default delimiter (comma) by clicking “Next”
Select “Department” as the x-axis column, then click “Next”.  Notice that you are informed that your x-axis selection is non-numeric, as shown below:

Confirm your selection by clicking “Next”
This time, because your x-axis selection is non-numeric, some of the y-axis selection buttons will be disabled (with an informative message displayed).  Click the checkbox at the top, to use a “Count” of your x-axis choice instead of selecting a y-axis data column.

	When you click the checkbox, the previously-available data columns are disabled.

Click “Next”, and in the next screen confirm your selection by clicking “Next”
Enter your desired graph title and axes titles, or accept the defaults by clicking “Next”
Select “Bar Graph”
A bar graph will be displayed.


