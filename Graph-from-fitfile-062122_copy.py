#!/usr/bin/env python
# coding: utf-8

# Recreating Zwift ride powerplot
# Graph-from-fitfile-062122.py

import os
import datetime
from fitparse import FitFile    # https://github.com/dtcooper/python-fitparse
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from tqdm import tqdm
from smooth import smooth
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox, AnchoredText, AnchoredOffsetbox)
from matplotlib.text import Annotation
# from matplotlib.backends.backend_agg import RendererAgg

# Title of Streamlit app
st.title('Cycling Workout Graph')

# Import .fit file and convert to pandas dataframe
uploaded_file = st.file_uploader("Upload your workout file (.fit file format only):  ", type=['fit'], key='fitfile')
if uploaded_file:
    st.write(f'You uploaded file "{uploaded_file.name}"')
else: 
    st.write("Please upload your workout file to generate graph.")

# Enter FTP value to determine workout zones in graph
ftp = st.text_input(label="Enter FTP in watts (whole numbers only):  ", max_chars=3, key='ftp')
if ftp!="":
    st.write(f"\nYour FTP has been recorded as {ftp} watts.")
    ftp = float(ftp)
else:
    st.write("Please enter your ftp in the box; otherwise, graph will not display.")

# The code for converting .fit files into a pandas dataframe is from http://johannesjacob.com/analyze-your-cycling-data-python/.
# To install the python packages, type 'pip install pandas numpy fitparse matplotlib tqdm' on the command line.

# #### From Johannes Jacob's blog post (http://johannesjacob.com/2019/03/13/analyze-your-cycling-data-python/):  
# _"Now we are ready to import the workout file and transform the data into a 
# pandas dataframe. Unfortunately we have to use an ugly hack with this "while" 
# loop to avoid timing issues. Then we are looping through the file, append 
# the records to a list and convert the list to a pandas dataframe."_

def parse_fitfile(uploaded_file):
    fitfile = FitFile(uploaded_file)
    while True:
        try:
            fitfile.messages
            break
        except KeyError:
            continue
    workout = []
    for record in fitfile.get_messages('record'):
        r = {}
        for record_data in record:
            r[record_data.name] = record_data.value
        workout.append(r)
    df = pd.DataFrame(workout)
    
    return df

def workout_date_time_freq(df):
    # Get date
    timestamp = df['timestamp'][:1]
    date = np.datetime_as_string(timestamp, unit='D')
    date_str = str(date)
    date_str = date_str.strip("[")
    date_str = date_str.strip("]")
    date_str = date_str.strip("'")
    
    # Get workout length in minutes
    num_datapoints = int(len(df['timestamp']))
    workout_timelength = df['timestamp'][4674] - df['timestamp'][0]
    workout_seconds = int(workout_timelength.total_seconds())
    workout_minutes = workout_seconds/60

    # Compute frequency of data recording from number of seconds in workout divided by the number of data points
    rec_freq = round(workout_seconds/num_datapoints)
    freq = 60 / rec_freq

    return date_str, num_datapoints, freq

def df_clean_trim(df):
    #Drop unnecessary columns
    df_cleaned = df.drop(columns = ['altitude', 'cadence', 'compressed_speed_distance', 'cycle_length', 'distance', 
        'enhanced_altitude', 'enhanced_speed', 'grade', 'position_lat', 'position_long', 
        'resistance', 'temperature', 'time_from_course', 'timestamp'], axis=1, inplace=True)

    # Insert a column 'data_points' to enable selection of max hr and watts by index
    df_cleaned.insert(loc=0, column='data_points', value=np.arange(len(df)))
    df_cleaned.rename(columns = {'power':'watts'}, inplace = True)
    df_cleaned['watts'].fillna(0, inplace=True)

    return df_cleaned

def convert_to_arr(df_cleaned):
    workout_data = df_cleaned.to_records(index=False)
    watts = workout_data['watts']
    max_watts = max(watts)

    # Find maximum power value and time stamp
    minutes = workout_data['data_points']/freq
    max_watts_idx = np.argmax(workout_data['watts'])
    max_watts_timestamp = minutes[max_pwr_idx]

    # Find maximum heart rate value and time stamp
    hr = workout_data['heart_rate']
    max_hr = max(hr)
    max_hr_idx = np.argmax(workout_data['heart_rate'])
    max_hr_timestamp = minutes[max_hr_idx]

    return watts, max_watts, minutes, max_pwr_timestamp, hr, max_hr, max_hr_timestamp

# Run functions:
if uploaded_file:
    df = parse_fitfile(uploaded_file)
    date_str, num_datapoints, freq = workout_date_time_freq(df)
    df_cleaned = df_clean_trim(df)
    watts, max_watts, minutes, max_pwr_timestamp, hr, max_hr, max_hr_timestamp = convert_to_arr(df_cleaned)
    # Smooth power curve using helper function 'smooth.py'
    watts_smoothed = smooth(watts, window_len=10)

# Plot data
if uploaded_file:
    if ftp != None:
        fig, ax1 = plt.subplots(figsize=(18, 8))
        ax1.set_facecolor(color='#252525')
        ax1.set_xlabel("Time in Minutes", fontsize='large')
        ax1.set_ylabel("Watts", fontsize='large')
        ax1.tick_params(labelsize='large')

    # This expands the top of the graph to 60% beyond max watts
        if uploaded_file:
            ax1.set_ylim(top=max(watts)*1.80)

            # logic for color under the graph based on % of FTP (thanks to Jonas Häggqvist for this code)
            if ftp!="" and uploaded_file: 
                ftp = int(ftp)
                ax1.grid(which='major', axis='y', alpha=0.1, linewidth=1)
                plt.fill_between(minutes, watts_smoothed, where=watts_smoothed > 0.00*ftp, color='#646464')
                plt.fill_between(minutes, watts_smoothed, where=watts_smoothed > 0.60*ftp, color='#328bff')
                plt.fill_between(minutes, watts_smoothed, where=watts_smoothed > 0.75*ftp, color='#59bf59')
                plt.fill_between(minutes, watts_smoothed, where=watts_smoothed > 0.90*ftp, color='#ffcc3f')
                plt.fill_between(minutes, watts_smoothed, where=watts_smoothed > 1.05*ftp, color='#ff663a')
                plt.fill_between(minutes, watts_smoothed, where=watts_smoothed > 1.18*ftp, color='#ff340c')

        # Setting workout date annotation (thanks to Phil Daws for the code that helped me get started)
        # Note:  xy for the purposes of workout date label is set using 'data' for coordinates 
        xmin, xmax = ax1.get_xlim()
        ymin, ymax = ax1.get_ylim()
        xy = [xmax-(xmax*0.05), ymax-(ymax*0.05)]
        
        # Adding the workout date to the graph
        workout_date = Annotation(f'Workout date: {date_str}', xy=[xmax//2, ymax-(ymax*0.08)], 
                                  ha='center', color='white', fontweight='bold', fontsize='large')
        ax1.add_artist(workout_date)
        
        # Plot smoothed power, line color, and thickness
        if ftp!="" and uploaded_file: 
            plt.plot(minutes, watts_smoothed, color='white', linewidth=0.75)
        
            # Annotate max power 
            max_power = Annotation(f'{max_watts}w', xy=(max_pwr_timestamp, max_watts), xytext=(0, 15), 
                                   textcoords="offset pixels", ha='center', color='white', fontweight='bold', 
                                   fontsize='large', arrowprops=dict(arrowstyle='wedge', color='yellow'))
            ax1.add_artist(max_power)
            
            plt.vlines(x=max_pwr_timestamp, ymin=0, ymax=max_watts, color='white', linewidth=1.5)
            
        
            # Instantiate second y axis for heart rate graph
            ax2 = ax1.twinx()
            ax2.set_ylabel("Heart Rate", fontsize='large')    
            ax2.set_ylim(top=max(hr)*1.30)
        
            # Plot heart rate
            ax2.plot(minutes, hr, color='red', linewidth=0.75)
        
            # Annotate max heart rate
            max_hr_annt = Annotation(f'{max_hr}bpm', xy=(max_hr_timestamp, max_hr), xytext=(0, 15), 
                                   textcoords="offset pixels", ha='center', color='white', fontweight='bold', 
                                   fontsize='large', arrowprops=dict(arrowstyle='wedge', color='red'))
            ax2.add_artist(max_hr_annt)

        st.pyplot(fig)
        fig.savefig('workout_graph.png', transparent=False, dpi=80, bbox_inches="tight")

    else:
        st.write(f"\nThe graph cannot be drawn; no valid FTP was provided.")
        st.write(f"If you wish to try again, please have your FTP value ready and then reload this page.")

    with open("workout_graph.png", "rb") as file:
         btn = st.download_button(
                 label="Download image",
                 data=file,
                 file_name="workout_graph.png",
                 mime="image/png"
               )

