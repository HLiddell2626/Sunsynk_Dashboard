# --------------------------------------------------
# --- Web Dashboard for .CSV Files  for Sunsynk ----
# --- By Harrison Liddell --------------------------
# --------------------------------------------------

# Importing required libraries
import streamlit as st  # Streamlit is used to create the web dashboard for interactive data visualization
import pandas as pd  # Pandas is used for data manipulation and analysis
import plotly.graph_objects as go  # Plotly is used for creating interactive visualizations (graphs and plots)
import numpy as np  # Numpy is used for numerical operations
import random  # Random is used to generate random colours for plot markers and lines

# Function to generate a random hex colour
def random_colour():
    """
    Generates a random hexadecimal colour code, to be used for plot markers and lines.
    """
    return f"#{random.randint(0, 0xFFFFFF):06x}"

# Setting the page layout
st.set_page_config(page_title="Sunsynk - .CSV Dashboard", layout="wide")

#-------------- Title of the Dashboard --------------
st.title("Sunsynk - .CSV Dashboard")

#-------------- Sidebar for user interaction --------------
st.sidebar.header("Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# Checking if a file is uploaded
if uploaded_file:
    #-------------- Loading and Displaying the Dataset --------------
    # Loading the uploaded CSV dataset into a DataFrame
    data = pd.read_csv(uploaded_file)

    # Displaying a preview of the dataset in the main body of the app
    st.header("Dataset Preview")
    st.dataframe(data.head())  # Displaying the first 5 rows of the dataset

    #-------------- Converting Timestamp Columns --------------
    # Looking for columns with object data type (likely timestamps) and attempting to convert them to datetime format
    timestamp_columns = data.select_dtypes(include=["object"]).columns
    for col in timestamp_columns:
        try:
            # Attempting to parse the timestamp format '2024-11-25_12-53-25'
            data[col] = pd.to_datetime(data[col], format="%Y-%m-%d_%H-%M-%S", errors='ignore')
        except Exception as e:
            pass  # If it cannot be converted, simply leave the column as is

    
else:
    st.info("Please upload a CSV file to get started.") # error handling incase the .csv file is not recognised
