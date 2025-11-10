#!/usr/bin/env python
# coding: utf-8

# # Recreating Zwift ride powerplot

# ## Import .fit file and convert to pandas dataframe

# In[2]:


import os
import datetime
from fitparse import FitFile    # https://github.com/dtcooper/python-fitparse
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm
from smooth import smooth
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox, AnchoredText, AnchoredOffsetbox)
from matplotlib.text import Annotation


# ## Title of Streamlit app

# In[3]:


st.title('Workout Graph in Zwift Style')


# ##  Obtain FTP value from user to determine workout zones in graph

# In[4]:


# set up try / except loop:
n = 01
while n < 3: 
    try:
        ftp = int(input("Enter FTP in watts (whole numbers only):  "))
        print(f"\nYour FTP has been recorded as {ftp} watts.")
        break
    except ValueError:
        n += 1
        print("\nYour FTP value cannot contain letters, be left blank, or be entered as a decimal value. \n")


# ## Have user enter file name / upload file

# The code for importing .fit files and converting to a pandas dataframe is from http://johannesjacob.com/analyze-your-cycling-data-python/.
# To install the python packages, type 'pip install pandas numpy fitparse matplotlib tqdm' on the command line.
# 

# In[5]:


filename = input("Type filename, including .fit extension:  ")
# 2021-10-05-10-54-32.fit

fitfile = FitFile(filename)


# #### From Johannes Jacob's blog post (http://johannesjacob.com/2019/03/13/analyze-your-cycling-data-python/):  
# _"Now we are ready to import the workout file and transform the data into a 
# pandas dataframe. Unfortunately we have to use an ugly hack with this "while" 
# loop to avoid timing issues. Then we are looping through the file, append 
# the records to a list and convert the list to a pandas dataframe."_

# In[6]:


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


# In[7]:


df = parse_fitfile(filename)


# In[8]:


column_list = list(df.columns)


# ##  Remove unnecessary columns and remove null values

# In[9]:


def df_clean_trim(df):
    # Set up new dataframe with only necessary columns
    # First, check to see if heart rate data is present
    if ('heart_rate' in column_list):
        df_cleaned = df[['heart_rate', 'power', 'timestamp']].copy()
        # Insert a column 'data_points' to enable selection of max hr and watts by index
        df_cleaned.insert(loc=0, column='data_points', value=np.arange(len(df)))
        df_cleaned.rename(columns = {'power':'watts'}, inplace = True)
        df_cleaned.fillna({'watts': 0}, inplace=True)
        df_cleaned.fillna({'heart_rate': 0}, inplace=True)
    else:
        df_cleaned = df[['power', 'timestamp']].copy()
        # Insert a column 'data_points' to enable selection of max hr and watts by index
        df_cleaned.insert(loc=0, column='data_points', value=np.arange(len(df)))
        df_cleaned.rename(columns = {'power':'watts'}, inplace = True)
        df_cleaned.fillna({'watts': 0}, inplace=True)

    return df_cleaned


# In[10]:


df_cleaned = df_clean_trim(df)


# ## Get date of workout and length of workout in seconds/minutes 

# In[11]:


def workout_date_time_freq(df):
    # Get date
    df1 = df.copy()
    timestamp = df1['timestamp'][:1]
    date = np.datetime_as_string(timestamp, unit='D')
    date_str = str(date)
    date_str = date_str.strip("[")
    date_str = date_str.strip("]")
    date_str = date_str.strip("'")

    # Get workout length in minutes
    num_datapoints = int(len(df1['timestamp']))
    workout_timelength = df1['timestamp'][num_datapoints-1] - df1['timestamp'][0]
    workout_seconds = int(workout_timelength.total_seconds())
    workout_minutes = workout_seconds/60

    # Compute frequency of data recording from number of seconds in workout divided by the number of data points
    rec_freq = round(workout_seconds/num_datapoints)
    freq = 60 / rec_freq

    return date_str, num_datapoints, workout_minutes, rec_freq, freq


# In[12]:


date_str, num_datapoints, workout_minutes, rec_freq, freq = workout_date_time_freq(df_cleaned)


# ## Convert dataframe to NumPy array

# In[13]:


def convert_to_arr(df_cleaned):
    workout_data = df_cleaned.to_records(index=False)
    watts = workout_data['watts']
    max_watts = max(watts)

    # Find maximum power value and time stamp
    minutes = workout_data['data_points']/freq
    max_watts_idx = np.argmax(workout_data['watts'])
    max_watts_timestamp = minutes[max_watts_idx]

    # Find maximum heart rate value and time stamp
    hr = workout_data['heart_rate']
    max_hr = max(hr)
    max_hr_idx = np.argmax(workout_data['heart_rate'])
    max_hr_timestamp = minutes[max_hr_idx]

    return watts, max_watts, minutes, max_pwr_timestamp, hr, max_hr, max_hr_timestamp


# In[14]:


workout_data = df_cleaned.to_records(index=False)


# In[15]:


watts = workout_data['watts']


# In[16]:


max_watts = int(max(watts))


# ## Smooth power curve

# In[17]:


# using helper function 'smooth.py'

watts_smoothed = smooth(watts, window_len=10)


# ##  Convert workout x-axis time values to minutes

# In[18]:


# converting recording data into minutes  
# freq represents how many rows of data are contained in 1 minute of workout time
# For example, if data is recorded every 5 seconds, then there will be 12 rows of data 
# per every one minute of workout time

freq = 60 / rec_freq


# In[19]:


minutes = workout_data['data_points']/freq


# ## Find maximum power value and time stamp

# In[20]:


max_pwr_idx = np.argmax(workout_data['watts'])


# In[21]:


max_pwr_timestamp = round(minutes[max_pwr_idx], ndigits=3)


# In[22]:


workout_data[max_pwr_idx]


# ## Find maximum heart rate value and time stamp

# Note:  if no heart rate data is available, this section will be skipped, as will the heart rate graphing section

# In[23]:


# Function to find max HR & time stamp, if applicable

def max_hr_stamp(workout_data):
    if ('heart_rate' in column_list):
        print('File contains HR data')
        hr = workout_data['heart_rate']
        max_hr = int(max(hr))
        max_hr_idx = np.argmax(workout_data['heart_rate'])
        max_hr_timestamp = minutes[max_hr_idx]
    else:
        print('File does not contain HR data')
        hr = 0
        max_hr = 0
        max_hr_idx = 0
        max_hr_timestamp = 0
    return hr, max_hr, max_hr_idx, max_hr_timestamp


# In[24]:


hr, max_hr, max_hr_idx, max_hr_timestamp = max_hr_stamp(workout_data)


# ## Plot data

# In[25]:


import matplotlib 
matplotlib.use('qtagg')

if ftp != None:
    figsize = (28, 12)    
    img, ax1 = plt.subplots(figsize=figsize)
    ax1.set_facecolor(color='#252525')
    ax1.set_xlabel("Minutes", fontsize=22.0)
    ax1.set_ylabel("Watts", fontsize=22.0)
    ax1.tick_params(labelsize=22.0)

    # This expands the top of the graph to 80% beyond max watts
    ax1.set_ylim(top=max(watts)*1.80)

    # logic for color under the graph based on % of FTP (thanks to Jonas Häggqvist for this code)
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
                              ha='center', color='white', fontweight='bold', fontsize=22.0)
    ax1.add_artist(workout_date)

    # Plot smoothed power, line color, and thickness
    plt.plot(minutes, watts_smoothed, color='white', linewidth=1.25)

    # Annotate max power 
    max_power = Annotation(f'{max_watts}w', xy=(max_pwr_timestamp, max_watts), xytext=(0, 15), 
                           textcoords="offset pixels", ha='center', color='white', fontweight='bold', 
                           fontsize=22.0, arrowprops=dict(arrowstyle='wedge', color='yellow'))
    ax1.add_artist(max_power)

    plt.vlines(x=max_pwr_timestamp, ymin=0, ymax=max_watts, color='white', linewidth=1.5)

    # Add HR data to graph
    if ('heart_rate' in column_list):
        # Instantiate second y axis for heart rate graph
        ax2 = ax1.twinx()
        ax2.set_ylabel("Heart Rate", fontsize=22.0)    
        ax2.set_ylim(top=max(hr)*1.20)
        ax2.tick_params(labelsize=22.0)

        # Plot heart rate
        ax2.plot(minutes, hr, color='red', linewidth=1.2)

        # Annotate max heart rate
        max_hr_annt = Annotation(f'{max_hr}bpm', xy=(max_hr_timestamp, max_hr), xytext=(0, 15), 
                               textcoords="offset pixels", ha='center', color='white', fontweight='bold', 
                               fontsize=22.0, arrowprops=dict(arrowstyle='wedge', color='red'))
        ax2.add_artist(max_hr_annt)

    plt.show()

else:
    print(f"\nThe graph cannot be drawn; no valid FTP was provided.")
    print(f"If you wish to try again, please have your FTP value ready and then reload this page.")


# In[26]:


import matplotlib 
# matplotlib.use('qtagg')

if ftp != None:
    figsize = (28, 12)    
    img, ax1 = plt.subplots(figsize=figsize)
    ax1.set_facecolor(color='#252525')
    ax1.set_xlabel("Minutes", fontsize=22.0)
    ax1.set_ylabel("Watts", fontsize=22.0)
    ax1.tick_params(labelsize=22.0)

    # This expands the top of the graph to 80% beyond max watts
    ax1.set_ylim(top=max(watts)*1.80)

    # logic for color under the graph based on % of FTP (thanks to Jonas Häggqvist for this code)
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
                              ha='center', color='white', fontweight='bold', fontsize=22.0)
    ax1.add_artist(workout_date)

    # Plot smoothed power, line color, and thickness
    plt.plot(minutes, watts_smoothed, color='white', linewidth=1.25)

    # Annotate max power 
    max_power = Annotation(f'{max_watts}w', xy=(max_pwr_timestamp, max_watts), xytext=(0, 15), 
                           textcoords="offset pixels", ha='center', color='white', fontweight='bold', 
                           fontsize=22.0, arrowprops=dict(arrowstyle='wedge', color='yellow'))
    ax1.add_artist(max_power)

    plt.vlines(x=max_pwr_timestamp, ymin=0, ymax=max_watts, color='white', linewidth=1.5)

    # Add HR data to graph
    if ('heart_rate' in column_list):
        # Instantiate second y axis for heart rate graph
        ax2 = ax1.twinx()
        ax2.set_ylabel("Heart Rate", fontsize=22.0)    
        ax2.set_ylim(top=max(hr)*1.20)
        ax2.tick_params(labelsize=22.0)

        # Plot heart rate
        ax2.plot(minutes, hr, color='red', linewidth=1.2)

        # Annotate max heart rate
        max_hr_annt = Annotation(f'{max_hr}bpm', xy=(max_hr_timestamp, max_hr), xytext=(0, 15), 
                               textcoords="offset pixels", ha='center', color='white', fontweight='bold', 
                               fontsize=22.0, arrowprops=dict(arrowstyle='wedge', color='red'))
        ax2.add_artist(max_hr_annt)

    plt.show()

else:
    print(f"\nThe graph cannot be drawn; no valid FTP was provided.")
    print(f"If you wish to try again, please have your FTP value ready and then reload this page.")


# In[ ]:





# In[ ]:




