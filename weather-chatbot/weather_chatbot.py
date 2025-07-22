import streamlit as st
import requests
import os  # For environment variables

# Set page config
st.set_page_config(page_title="Weather Buddy ☁️", layout="centered")

# Custom header
st.markdown(
    "<h1 style='text-align: center;'>🌤️ Weather Buddy - Your Chatty Forecast Friend</h1>",
    unsafe_allow_html=True
)

# Chatbot-style intro
st.markdown("👋 Hello! I'm your weather assistant. Ask me about the weather in any city below!")

# User input
city = st.text_input("📍 Which city's weather would you like to check?", placeholder="e.g., London, Tokyo, New York")

# ✅ Load API key securely from environment variable
api_key = os.getenv("OPENWEATHER_API_KEY")

# Show error if key is missing
if not api_key:
    st.error("🚨 API key is missing! Please set the 'OPENWEATHER_API_KEY' environment variable.")
else:
    # Function to get weather data
    def get_weather(city_name):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        response = requests.get(url)
        return response.json()

    # Handle input
    if city:
        with st.spinner("🔄 Fetching weather data..."):
            data = get_weather(city)

        if data.get("cod") != 200:
            error_msg = data.get("message", "Unknown error")
            st.error(f"😕 Error: {error_msg}")
            st.code(data)  # Show full response for debugging
        else:
            # Extract weather info
            weather = data["weather"][0]["description"].title()
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            # Chatbot-style reply
            st.markdown("---")
            st.markdown("### 🤖 Weather Bot says:")
            st.markdown(f"""
            > **📍 City:** {city.title()}  
            > **🌡️ Temperature:** {temperature} °C  
            > **🌥️ Conditions:** {weather}  
            > **💧 Humidity:** {humidity}%  
            > **🌬️ Wind Speed:** {wind_speed} m/s  
            """)
            st.success("🌈 Hope that helps! Stay safe and dress appropriately! 🧥☂️")


