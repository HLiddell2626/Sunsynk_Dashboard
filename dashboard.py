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

    #-------------- Sidebar: Forecasting Section --------------
    with st.sidebar.expander('Forecasting Options', expanded=False):
        # Selecting the timestamp column for X-axis and numeric column to predict (Y-axis)
        timestamp_columns = data.select_dtypes(include=["datetime"]).columns
        numeric_columns = data.select_dtypes(include=["float", "int"]).columns

        # Forecasting target: Selecting numeric column to forecast
        forecast_target = st.selectbox(
            "Select Column to Forecast (Target)",
            options=numeric_columns,
            help="Choose the numeric column to forecast."
        )

        # Forecasting feature: Selecting timestamp column as feature (independent variable)
        forecast_timestamp = st.selectbox(
            "Select Timestamp Column",
            options=timestamp_columns,
            help="Choose the timestamp column as feature for forecasting."
        )

        # Forecasting horizon (number of future points to predict)
        forecast_horizon = st.slider("Forecast Horizon", 1, 30, 10)

        # Selecting the plot type for the forecast (Line or Scatter)
        forecast_plot_type = st.radio(
            "Select Forecast Plot Type",
            options=["Scatter Plot", "Line Graph"],
            help="Choose between a scatter plot or a line graph for the forecast."
        )

        # Storing selected forecasting options in session state
        st.session_state.forecast_target = forecast_target
        st.session_state.forecast_timestamp = forecast_timestamp
        st.session_state.forecast_horizon = forecast_horizon
        st.session_state.forecast_plot_type = forecast_plot_type

        # Adding a button to generate the forecast inside the sidebar
        if st.button("Generate Forecast"):
            st.session_state.generate_forecast = True

    #-------------- Sidebar: Customisation Section --------------
    with st.sidebar.expander('Customisation Options', expanded=False):
        # Colour Customisation (for plots and the dashboard)
        primary_colour = st.color_picker("Select Primary Colour", "#1f77b4")
        secondary_colour = st.color_picker("Select Secondary Colour", "#ff7f0e")

        # Line and Marker Customisation
        line_width = st.slider("Line Width", 1, 10, 2)
        marker_size = st.slider("Marker Size", 5, 15, 8)

    #-------------- Main Body: Display Plot --------------
    if 'x_axis' in st.session_state and 'y_axis' in st.session_state:
        x_axis = st.session_state.x_axis
        y_axis = st.session_state.y_axis
        plot_type = st.session_state.plot_type

        if len(x_axis) > 0 and len(y_axis) > 0 and 'generate_plot' in st.session_state and st.session_state.generate_plot:
            # Adding a button to create the plot inside the sidebar
            # Filtering the data to include only the selected X and Y axis columns
            filtered_data = data[x_axis + y_axis]

            # Displaying the filtered dataset in the app
            st.subheader(f"Filtered Dataset: {', '.join(x_axis + y_axis)}")
            st.dataframe(filtered_data)

            # Creating a figure for the plot
            fig = go.Figure()

            # Looping through each combination of X and Y columns to add traces to the plot
            for x in x_axis:
                for y in y_axis:
                    random_marker_color = random_colour()  # Random colour for marker
                    random_line_color = random_colour()  # Random colour for line

                    if plot_type == "Scatter Plot":
                        # Adding scatter plot traces
                        fig.add_trace(
                            go.Scatter(
                                x=filtered_data[x],  # Use datetime columns directly for the x-axis
                                y=filtered_data[y],
                                mode='markers',
                                name=f"{x} vs {y}",  # Legend name for the trace
                                marker=dict(
                                    size=marker_size,  # Marker size
                                    color=random_marker_color  # Random colour for the marker
                                ),
                            )
                        )
                    elif plot_type == "Line Graph":
                        # Adding line graph traces
                        fig.add_trace(
                            go.Scatter(
                                x=filtered_data[x],  # Use datetime columns directly for the x-axis
                                y=filtered_data[y],
                                mode='lines',
                                name=f"{x} vs {y}",  # Legend name for the trace
                                line=dict(
                                    width=line_width,  # Line width
                                    color=random_line_color  # Random colour for the line
                                ),
                            )
                        )

            # Updating layout for better readability
            fig.update_layout(
                title="Comparison Plot",
                xaxis_title="X-axis",
                yaxis_title="Y-axis",
                legend_title="Series",
                hovermode="closest",  # Hover over points to show info
                template="plotly",
                xaxis=dict(
                    tickformat="%Y-%m-%d %H:%M:%S"  # Format timestamp to human-readable date
                )
            )

            # Displaying the plot in the main body
            st.plotly_chart(fig, use_container_width=True)

            # Resetting the plot generation flag
            st.session_state.generate_plot = False
        else:
            st.warning("Please select at least one column for both X-axis and Y-axis.")

    #-------------- Main Body: Display Forecasting Results --------------
    if 'forecast_target' in st.session_state and 'forecast_timestamp' in st.session_state and 'generate_forecast' in st.session_state and st.session_state.generate_forecast:
        forecast_target = st.session_state.forecast_target
        forecast_timestamp = st.session_state.forecast_timestamp
        forecast_horizon = st.session_state.forecast_horizon
        forecast_plot_type = st.session_state.forecast_plot_type

        # Preparing the data for forecasting by selecting the relevant timestamp and target columns
        data_for_forecasting = data[[forecast_timestamp, forecast_target]].dropna()

        # Creating a forecast DataFrame (this is just simulated data for now, using random values)
        forecast_df = pd.DataFrame({
            forecast_timestamp: pd.date_range(
                start=data_for_forecasting[forecast_timestamp].iloc[-1] + pd.Timedelta(days=1),
                periods=forecast_horizon,
                freq="D"  # Forecast daily intervals
            ),
            forecast_target: np.random.random(forecast_horizon)  # Random values for forecasted target
        })

        # Displaying the forecasted data table
        st.subheader("Forecasted Data")
        st.dataframe(forecast_df)

        # Creating a forecast plot
        fig = go.Figure()

        random_forecast_marker_color = random_colour()  # Random colour for forecast markers
        random_forecast_line_color = random_colour()  # Random colour for forecast lines

        if forecast_plot_type == "Scatter Plot":
            # Adding scatter plot for the forecast
            fig.add_trace(
                go.Scatter(
                    x=forecast_df[forecast_timestamp],
                    y=forecast_df[forecast_target],
                    mode='markers',
                    name=f"Forecasted {forecast_target}",
                    marker=dict(size=8, color=random_forecast_marker_color)
                )
            )
        elif forecast_plot_type == "Line Graph":
            # Adding line graph for the forecast
            fig.add_trace(
                go.Scatter(
                    x=forecast_df[forecast_timestamp],
                    y=forecast_df[forecast_target],
                    mode='lines',
                    name=f"Forecasted {forecast_target}",
                    line=dict(width=2, color=random_forecast_line_color)
                )
            )

        # Updating layout of the forecast plot
        fig.update_layout(
            title=f"{forecast_target} Forecast",
            xaxis_title=forecast_timestamp,
            yaxis_title=forecast_target,
            hovermode="closest",
            template="plotly",
            xaxis=dict(
                tickformat="%Y-%m-%d %H:%M:%S"  # Formatting timestamp to human-readable date
            )
        )

        # Displaying the forecast plot
        st.plotly_chart(fig, use_container_width=True)

        # Resetting the forecast generation flag
        st.session_state.generate_forecast = False

else:
    st.info("Please upload a CSV file to get started.") # error handling incase the .csv file is not recognised
