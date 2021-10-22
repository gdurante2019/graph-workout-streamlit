
import os
import datetime
from fitparse import FitFile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import streamlit as st


# From Joe Nelson's streamlit script for predicting school student's age based on writing sample
# Repo:  jnels13/Screening-Childrens-Writing-Level-With-NLP

# this is the main function in which we define our webpage  
def main(): 
      # giving the webpage a title 
    #st.title("Graph of Workout Fitfile") 
      
    # here we define some of the front end elements of the web page like  
    # the font and background color, the padding and the text to be displayed 
    html_temp = """ 
    <div style ="background-color: #ff9551;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Graph of Workout Fitfile </h1> 
    <p> I created this app to create graphs of Zwift cycling workouts.  You will need to upload your 
    <p> fitfile (and profile picture if desired) and enter your FTP.  If you'd like for your name to be 
    <p> shown on the graph, please enter it in the appropriate box below.  
    <p>Code and contact info may be found on my github, <a href="https://github.com/gdurante2019?tab=repositories" target="_blank">HERE.</a>
    <p> 

    </div> 
    """
      
    # this line allows us to display the front end aspects we have  
    # defined in the above code 
    st.markdown(html_temp, unsafe_allow_html = True) 

    # to upload a file:
    uploaded_file = st.file_uploader("Choose a file")

	if uploaded_file is not None:
	    # To read file as bytes:
	    bytes_data = uploaded_file.getvalue()
	    st.write(bytes_data)
	
	    # To convert to a string based IO:
	    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
	    st.write(stringio)
	
	    # To read file as string:
	    string_data = stringio.read()
	    st.write(string_data)
	
	    # Can be used wherever a "file-like" object is accepted:
	    dataframe = pd.read_csv(uploaded_file)
	    st.write(dataframe)
      
   

    # the following lines create text boxes in which the user can enter  
    # the data required to make the prediction 
    text = st.text_input("STUDENT'S TEXT:", "Type or Paste Here") 

    result ="" 


