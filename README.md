# Code for producing cycling workout summary graph
This repo houses code for a function that takes in a .fit file and returns a graph with a similar color scheme to Zwift workout summary graphs.  

_Note:_  these graphs are created from .fit files, not by Zwift, and no Zwift branding is implied or endorsed.  

*Newsflash!*  The code has been deployed to Streamlit as of June 21, 2022. 🧑‍💻 🥳 🎉   The app can be accessed at https://gdurante2019-graph-workout-str-graph-from-fitfile-062222-5a5ikb.streamlitapp.com/.

## Purpose
The inspiration for this project comes from discussions with fellow cycling enthusiasts who race in the Zwift Racing League on the Backpedal team and would like to share their workout summary graphs from Zwift rides in a simple, standardized way in chat discussions.  The utility of the graphs generated from this code is to make it easy for riders to understand, at a glance, the workout efforts of fellow riders.

## Usage
Users will upload workout fitfiles and enter their FTP. The resulting graph will contain smoothed power output, workout zones, a plot of heart rate during the workout, and max power and max heart rate annotations. Here's an example:

![image](https://github.com/gdurante2019/graph-workout-streamlit/blob/main/example_workout_graph.png)


## Planned Feature Additions
* Deploying this code using Streamlit to allow everyone to generate a workout graph easily from a simple interface -- DONE. 
* Option to add photo thumbnail with name caption -- This is on the back burner for now.
