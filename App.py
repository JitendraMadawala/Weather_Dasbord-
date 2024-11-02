import streamlit as st
import requests
import pandas as pd

# API request for the weather data, including ⁠ current_weather=true ⁠
resp = requests.get("https://api.open-meteo.com/v1/forecast?latitude=6.9355&longitude=79.8487&current_weather=true&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum&timezone=Asia/Colombo")
value = resp.json()

# Streamlit app layout
st.write("Made by Jiendra")
st.title("Jitendra Weather Dashboard")
st.subheader("Asia/Colombo")
st.image("lotus-tower.jpg", width=500)

# Current weather metrics
col1, col2, col3 = st.columns(3)
if 'current_weather' in value:
    col1.metric("Temperature", f"{value['current_weather']['temperature']} °C")
    col2.metric("Wind", f"{value['current_weather']['windspeed']} km/h")
    col3.metric("Humidity", f"{value['current_weather'].get('relative_humidity', 'N/A')}%")
else:
    st.error("Current weather data is not available.")

# Video section
st.video('https://www.youtube.com/watch?v=zUNEFefftt8')

# Sidebar with location details
st.sidebar.write("Location Details")
st.sidebar.write(f"Latitude: {value['latitude']}")
st.sidebar.write(f"Longitude: {value['longitude']}")

# Sidebar selection box for data visualization
option = st.sidebar.selectbox(
    "Pick a data option",
    ("Sunrise", "Sunset", "Precipitation", "Max Temperature"),
    index=0,
)

# Prepare daily data for display
daily_data = value['daily']
dates = daily_data['time']

# Creating DataFrames for the selected data
sunrise_df = pd.DataFrame({'Date': dates, 'Sunrise': daily_data['sunrise']})
sunset_df = pd.DataFrame({'Date': dates, 'Sunset': daily_data['sunset']})
precipitation_df = pd.DataFrame({'Date': dates, 'Precipitation (mm)': daily_data['precipitation_sum']})
max_temp_df = pd.DataFrame({'Date': dates, 'Max Temperature (°C)': daily_data['temperature_2m_max']})

# Display the selected data option
st.caption("This is the prediction for the next 7 days:")
if option == "Sunrise":
    st.line_chart(sunrise_df.set_index('Date'))
elif option == "Sunset":
    st.line_chart(sunset_df.set_index('Date'))
elif option == "Precipitation":
    st.line_chart(precipitation_df.set_index('Date'))
elif option == "Max Temperature":
    st.line_chart(max_temp_df.set_index('Date'))