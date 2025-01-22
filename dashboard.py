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
