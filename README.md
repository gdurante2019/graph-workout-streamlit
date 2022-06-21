# Code for producing cycling workout summary graph
This repo houses code for a function that takes in a .fit file and returns a graph with a similar color scheme to Zwift workout summary graphs.  

_Note:_  these graphs are created from .fit files, not by Zwift, and no Zwift branding is implied or endorsed.  

## Purpose
The inspiration for this project comes from discussions with fellow Zwift enthusiasts who race in the Zwift Racing League on the Backpedal team and would like to share their workout summary graphs from Zwift rides in a simple, standardized way in chat discussions.  The utility of the graphs generated from this code is to make it easy for riders to understand, at a glance, the workout efforts of fellow riders.

## Usage
Users will upload workout fitfiles and enter their FTP. The resulting graph will contain smoothed power output, workout zones, a plot of heart rate during the workout, and max power and max heart rate annotations. Here's an example:

![image](https://github.com/gdurante2019/graph-workout-streamlit/blob/main/example-graph-hr-maxwatts-022022.png)


## Planned Feature Additions
* Deploying this code using Streamlit to allow everyone to generate a workout graph easily from a simple interface -- DONE.  The Streamlit app can be accessed at https://share.streamlit.io/gdurante2019/graph-workout-streamlit/main/Graph-from-fitfile-062122_copy.py.
* Option to add photo thumbnail with name caption -- This is on the back burner for now.
