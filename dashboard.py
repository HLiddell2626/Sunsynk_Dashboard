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

    #-------------- Sidebar: Plotting Section --------------
    with st.sidebar.expander('Plotting Options', expanded=False):
        # Identifying numeric and datetime columns for plotting
        numeric_columns = data.select_dtypes(include=["float", "int"]).columns
        datetime_columns = data.select_dtypes(include=["datetime"]).columns

        # Combining the numeric and datetime columns for easier selection in the dropdown
        available_columns = list(numeric_columns) + list(datetime_columns)

        if len(available_columns) > 0:
            # If no search terms are set, initialise them to an empty string
            if 'x_search' not in st.session_state:
                st.session_state.x_search = ""
            if 'y_search' not in st.session_state:
                st.session_state.y_search = ""

            # Allowing the user to search for columns for the X-axis and Y-axis
            x_search = st.text_input("Search and filter X-axis columns:", st.session_state.x_search)
            y_search = st.text_input("Search and filter Y-axis columns:", st.session_state.y_search)

            # Updating the session state with the new search query
            st.session_state.x_search = x_search
            st.session_state.y_search = y_search

            # Filtering available columns based on the search query
            x_options = [col for col in available_columns if x_search.lower() in col.lower()]
            y_options = [col for col in available_columns if y_search.lower() in col.lower()]

            # Providing multi-select dropdowns for selecting columns for X and Y axes
            x_axis = st.multiselect(
                "Search and select columns for X-axis:",
                options=x_options,
                help="Start typing to search for column names."
            )
            y_axis = st.multiselect(
                "Search and select columns for Y-axis:",
                options=y_options,
                help="Start typing to search for column names."
            )

            # Storing selected options in the session state to persist them across interactions
            st.session_state.x_axis = x_axis
            st.session_state.y_axis = y_axis

            # Providing a radio button to choose the plot type (scatter or line graph)
            plot_type = st.radio(
                "Select Plot Type",
                options=["Scatter Plot", "Line Graph"],
                help="Choose between a scatter plot or a line graph."
            )

            # Storing the selected plot type in session state
            st.session_state.plot_type = plot_type

            # Adding a button to generate the plot inside the sidebar
            if st.button("Generate Plot"):
                st.session_state.generate_plot = True
        else:
            st.warning("The dataset must have at least one numeric or datetime column for plotting.")

else:
    st.info("Please upload a CSV file to get started.") # error handling incase the .csv file is not recognised
