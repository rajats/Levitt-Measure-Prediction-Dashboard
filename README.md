## Levitt's Measure Dasboard
Dashboard: [Levitt's Measure Dashboard](https://levittmeasure.herokuapp.com/)
  
 Michael Levitt, a professor of structural biology in Stanford, 
 also a Nobel laurette in Chemistry, defined a very simple measure, 
 using which he predicted the progression and eventual end of the 
 Covid 19 epidemic for many regions and countries, and (most of) 
 his predictions turned out to be surprisingly accurate, 
 given the simplicity of his metric.

Levitt's measure H(t) for day t for COVID-19 is a very simple 
measure, it is defined as:  
 H(t) = X(t) / X(t-1)   
where X(t) is the cumulative number of COVID-19 cases on day t. 
When the value of H(t) approximately equals 1 (we have taken 1.0001), 
then the situation will be better and the number of new cases 
per day will become considerably low.  
In the dashboard, one can see when Levitt's measure reaches a 
value of around 1.0001 for India or selected Indian 
State/UT/District, which will effectively mean when the 
situation will be under control. One can also adjust the 
start date to improve the fit of the regression line as the 
R-squared of the regression line is also shown.  
More information on Levitt's measure can be found 
here: [Conceptual basis of the Levitt measure](https://drive.google.com/file/d/1bnZ1tLP1hOJJ2GeQFEMTK5cPjEdHvyf2/view)

## Setup Instructions
1. Make sure you have installed Python 3.6, [pip3](https://pip.pypa.io/en/latest/) and [virtualenv](http://www.virtualenv.org/en/latest/).
2. Clone the repo - `https://github.com/rajats/Levitt-Measure-Prediction-Dashboard.git` and cd into
  the `Levitt-Measure-Prediction-Dashboard` directory. 
3. Create a virtual environment with Python 3 and install dependencies:

     ```bash
     $ virtualenv venv --python=/path/to/python3
     $ source venv/bin/activate
     $ pip install -r requirements
     ```
4. Run `python main.py` to start the development server.

## Setup Instructions (PyCharm)
1. Open Pycharm and click on VCS.
2. Click on Get from Version Control.
3. In the popup URL enter `https://github.com/rajats/Levitt-Measure-Prediction-Dashboard.git`
4. Press `Ctrl+Alt+S` to open the project **Settings/Preferences**.
5. Select **Project <project name> | Python Interpreter**. Click 
the settings icon and select Add. 
6. In the left-hand pane of the Add Python Interpreter dialog, 
select Virtualenv Environment.
7. Specify the location of the new virtual environment in 
the text field.
8. Choose the base interpreter from the list as Python 3.x and 
click OK.
9. Click terminal and run `pip install -r requirements.txt`
10. Click on play button or run `python main.py` in the terminal 
to start the development server.  
More information on configuring virtual environment in PyCharm 
can be found here: [Configure a virtual environment](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)

