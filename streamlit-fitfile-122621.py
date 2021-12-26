#!/usr/bin/env python
# coding: utf-8

# # Recreating Zwift ride powerplot

# ## Import .fit file and convert to pandas dataframe
# 
# The code for importing .fit files and converting to a pandas dataframe is from http://johannesjacob.com/analyze-your-cycling-data-python/.
# To install the python packages, type 'pip install pandas numpy fitparse matplotlib tqdm' on the command line.
# 

# In[1]:


import os
import datetime
from fitparse import FitFile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


# In[3]:


filename = input("Type filename, including .fit extension:  ")
# 2021-10-05-10-54-32.fit
# Race_day_2_Giro_Della_Donna_video_up_.fit

fitfile = FitFile(filename)


# From Johannes Jacob's blog post:  
# _"Now we are ready to import the workout file and transform the data into a 
# pandas dataframe. Unfortunately we have to use an ugly hack with this "while" 
# loop to avoid timing issues. Then we are looping through the file, append 
# the records to a list and convert the list to a pandas dataframe."_

# In[4]:


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


# In[5]:


df


# In[6]:


df.tail(1)


# ## Get date of workout from column 'timestamp' 

# In[7]:


timestamp = df['timestamp'].tail(1).values
timestamp


# In[8]:


date = np.datetime_as_string(timestamp, unit='D')
date


# In[9]:


date_str = str(date)
type(date_str)
print(date_str)


# In[10]:


date_str = date_str.strip("[")
date_str = date_str.strip("]")
date_str = date_str.strip("'")
print(date_str)


# ##  Remove unnecessary columns

# In[11]:


df.columns


# I'd like to keep the following columns only:
# * cadence
# * heart_rate
# * power
# * speed
# 

# In[12]:


df_subset = pd.DataFrame(df, columns=['cadence', 'heart_rate', 'power', 'speed'])
df_subset


# In[13]:


df_subset['power'].isna().value_counts()


# In[14]:


len(df_subset)


# ##  Insert a column 'time_unit' 

# _**Note:  Zwift records workout data once every second.  Using .fit files with data recorded more or less frequently will result in an incorrect number of minutes on the x-axis of the graph.**_

# In[15]:


df_subset.insert(loc=0, column='time_unit', value=np.arange(len(df_subset)))


# In[16]:


df_subset


# In[17]:


df_subset.rename(columns = {'power':'watts'}, inplace = True)


# In[18]:


df_subset


# In[19]:


df_subset['watts'].max()


# In[57]:


df_subset.loc[df_subset['watts'] == "NaN"]


# In[21]:


df_subset['watts'].fillna(0, inplace=True)


# ##  Obtain FTP value from user to determine workout zones in graph

# In[22]:


import numpy as np
import matplotlib.pyplot as plt
from smooth import smooth


# In[23]:


ftp = None

# Ben Pitt ftp for file example:  345 W

# set up try / except loop:
n = 0
while n < 3: 
    try:
        ftp = int(input("Enter FTP in watts (whole numbers only):  "))
        print(f"\nYour FTP has been recorded as {ftp} watts.")
        break
    except ValueError:
        n += 1
        print("\nYour FTP value cannot contain letters, be left blank, or be entered as a decimal value. \n")


# In[25]:


# convert df to numpy array

workout_data = df_subset.to_records(index=False)


# In[26]:


workout_data


# In[27]:


watts = workout_data['watts']
time = workout_data['time_unit']


# In[28]:


watts


# In[30]:


max_watts = max(watts)
max_watts


# In[31]:


y_top = max(watts)*1.20
y_top


# In[33]:


watts_smoothed = smooth(watts, window_len=25)
print(len(watts_smoothed))
watts_smoothed


# ##  Give user the opportunity to enter how often .fit file data is recorded, in seconds (default is once per second, as on Zwift)

# In[34]:


# Workout .fit file recorded by Zwift?

zwift_or_not = input("Was your .fit file recorded by Zwift, and/or did you device record the workout in 1-second increments?  \nEnter 'y' for yes or 'n' for no. ")


# In[35]:


zwift_or_not


# In[36]:


if zwift_or_not=='y' or zwift_or_not=='':
    rec_freq = 1
    print(f"\nThe default recording frequency has been set to {rec_freq} second.")

    
# If .fit file not recorded by Zwift, how frequently was data recorded, in seconds?

if zwift_or_not=='n':
    # default recording frequency to start with:
    rec_freq = 1
    
    # set up try / except loop:
    n = 0
    while n < 3: 
        try:
            rec_freq = int(input("Please enter the frequency that your workout data was recorded, in seconds.  \nEntry must be in numbers >0 and <=60, e.g., '1' for once per second, '5' to represent data recorded once every 5 seconds, '10' to signify once every 10 seconds, etc.   "))
            print(f"\nThe recording frequency has been set to {rec_freq} second(s).")
            break
        except ValueError:
            n += 1
            print()
        if n == 3:
            print(f"\nThe recording frequency has been set to {rec_freq} second(s).")


# In[37]:


rec_freq


# ##  Convert workout x-axis time values to minutes

# In[38]:


# converting recording data into minutes  
# freq represents how many rows of data are contained in 1 minute of workout time
# For example, if data is recorded every 5 seconds, then there will be 12 rows of data 
# per every one minute of workout time

freq = 60 / rec_freq
freq


# In[39]:


minutes = workout_data['time_unit']/freq
print(minutes)


# ## Allow user to upload image and enter name if desired, then draw graph

# In[42]:


# Upload image, e.g., "example_image.png"
# Ben Pitt image:  ben-pitt-giro-della-donna.png

img_name = input("If you wish to upload a thumbnail image in the upper right hand corner of the graph, please enter the name of it here:  ")


# In[43]:


from PIL import Image

im = Image.open(img_name)
im


# In[44]:


print(im.format, im.size, im.mode)


# In[45]:


width, height = im.size
width, height


# In[46]:


# print("The image is {} pixels wide and {} pixels tall".format(width, height))


# In[48]:


# is width < 200 or height > 100?

if height > 100:
    height_reduce_factor = height / 100
    new_height = int(height / height_reduce_factor)
    new_width = int(width / height_reduce_factor)

if width > height:
    width_reduce_factor = width / 200
    new_width = int(width / width_reduce_factor)
    new_height = int(height / width_reduce_factor)
    
#     print("Width rescaled to {}; height rescaled to {}".format(new_width, new_height))


# In[50]:


im = im.resize((new_width, new_height))


# In[51]:


im


# In[52]:


# print(im.format, im.size, im.mode)


# In[53]:


im.size[0], im.size[1]


# In[54]:


name = input("If you wish to have your name displayed under the picture you uploaded, please enter it here: ")


# In[59]:


from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox, AnchoredText, AnchoredOffsetbox)
from matplotlib.text import Annotation


if ftp != None:
    figsize = (18, 8)    
    img, ax = plt.subplots(figsize=figsize)
    ax.set_facecolor(color='#252525')
    ax.set_xlabel("Time in Minutes", fontsize='large')
    ax.set_ylabel("Watts", fontsize='large')
    ax.tick_params(labelsize='large')

    # This expands the top of the graph to 20% beyond max watts
    ax.set_ylim(top=max(watts)*1.20)

    # logic for color under the graph based on % of FTP (thanks to Jonas Häggqvist for this code)
    ax.grid(which='major', axis='y', alpha=0.1, linewidth=1)
    plt.fill_between(minutes, watts_smoothed, where=watts_smoothed > 0.00*ftp, color='#646464')
    plt.fill_between(minutes, watts_smoothed, where=watts_smoothed > 0.60*ftp, color='#328bff')
    plt.fill_between(minutes, watts_smoothed, where=watts_smoothed > 0.75*ftp, color='#59bf59')
    plt.fill_between(minutes, watts_smoothed, where=watts_smoothed > 0.90*ftp, color='#ffcc3f')
    plt.fill_between(minutes, watts_smoothed, where=watts_smoothed > 1.05*ftp, color='#ff663a')
    plt.fill_between(minutes, watts_smoothed, where=watts_smoothed > 1.18*ftp, color='#ff340c')

    # Setting the image and location (thanks to Phil Daws for the code that helped me get started)
    # Note:  xy for the purposes of workout date label is set using 'data' for coordinates 
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    xy = [xmax-(xmax*0.05), ymax-(ymax*0.05)]
    
    # Adding the workout date to the graph
    workout_date = Annotation(f'Workout date: {date_str}', xy=[xmax//2, ymax-(ymax*0.08)], 
                              ha='center', color='white', fontweight='bold', fontsize='large')
    ax.add_artist(workout_date)
    
    # Upload image, e.g., "example_image.png"
    if img_name != '':

        imagebox = OffsetImage(im, zoom=1)
        imagebox.image.axes = ax
        
        # setting image box location using xycoords='figure fraction'
        xy = [0.8, 0.8]

        ab = AnnotationBbox(imagebox, xy, xycoords='figure fraction', 
                            frameon=True, box_alignment = (1,1))
        ax.add_artist(ab)       

        # Annotate image with a text box 
        txt = TextArea(name, textprops=dict(color="white", fontsize='large', ha='center',
                                            fontweight='bold', fontstyle='italic'))

        ab = AnnotationBbox(txt, xy, xybox=(-im.size[0]/3,-im.size[1]-12), 
                            xycoords='figure fraction', boxcoords="offset points", 
                            frameon=False, box_alignment=(1, 1), annotation_clip=False, 
                            fontsize='large')
        ax.add_artist(ab)
        
    # Setting plot line color and thickness
    
    plt.plot(minutes, watts_smoothed, color='white', linewidth=1.0)

    plt.show()

else:
    print(f"\nThe graph cannot be drawn; no valid FTP was provided.")
    print(f"If you wish to try again, please have your FTP value ready and then reload this page.")


# In[ ]:



