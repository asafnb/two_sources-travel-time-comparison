import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache
def load_data():
    return pd.read_csv('data/merged_data.csv')

df = load_data()

# Adjust Timestamp
df['Timestamp'] = pd.to_datetime(df['Timestamp']) + pd.Timedelta(hours=2)

# Sidebar for user inputs
st.sidebar.header('User Input Options')
selected_date = st.sidebar.date_input("Select a Date", min_value=df['Timestamp'].dt.date.min(), max_value=df['Timestamp'].dt.date.max())
selected_segment = st.sidebar.selectbox("Select a Segment", options=df['SegmentCode'].unique())

# Filtering data based on selection
filtered_data = df[(df['Timestamp'].dt.date == selected_date) & (df['SegmentCode'] == selected_segment)]

# Display data
st.write(f"Travel Time Comparison for {selected_segment} on {selected_date}")
if not filtered_data.empty:
    fig = px.line(filtered_data, x='Timestamp', y=['Duration (seconds)', 'time'], markers=True,
                  labels={'value': 'Travel Time (seconds)', 'variable': 'Source'})
    st.plotly_chart(fig)
else:
    st.write("No data available for the selected date and segment.")
