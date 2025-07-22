from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import requests
import os
print("API Key loaded:", os.getenv("OPENWEATHER_API_KEY"))
from streamlit_lottie import st_lottie
import time

# ------------- Configuration -------------
st.set_page_config(page_title="Weather Buddy ☁️", layout="centered")

# ------------- Load API Key -------------
api_key = os.getenv("OPENWEATHER_API_KEY")

# ------------- Load Lottie Animation -------------
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Failed to load animation from {url}, status code: {r.status_code}")
        return None
    return r.json()

# Weather condition emojis
def get_weather_emoji(condition):
    condition = condition.lower()
    if "rain" in condition:
        return "🌧️"
    elif "cloud" in condition:
        return "☁️"
    elif "clear" in condition:
        return "☀️"
    elif "snow" in condition:
        return "❄️"
    elif "storm" in condition:
        return "🌩️"
    return "🌈"

# Clothing suggestion
def clothing_tip(temp_c):
    if temp_c < 5:
        return "🧥 It's freezing! Bundle up!"
    elif temp_c < 15:
        return "🧣 A jacket or sweater is a good idea."
    elif temp_c < 25:
        return "👕 Perfect weather for a t-shirt!"
    else:
        return "🩳 Stay cool! It's quite hot."

# ------------- UI Header -------------
st.markdown("<h1 style='text-align: center;'>🌤️ Weather Buddy - Your Chatty Forecast Friend</h1>", unsafe_allow_html=True)
st.markdown("👋 Hello! I'm your weather assistant. Ask me about the weather in any city below!")

# ------------- User Input -------------
city = st.text_input("📍 Which city's weather would you like to check?", placeholder="e.g., London, Tokyo, New York")
unit = st.radio("🌡️ Choose temperature unit:", ["Celsius (°C)", "Fahrenheit (°F)"])

# ------------- Weather API Call -------------
def get_weather(city_name, use_metric=True):
    units = "metric" if use_metric else "imperial"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units={units}"
    return requests.get(url).json()

# ------------- Main Weather Logic -------------
if not api_key:
    st.error("🚨 API key is missing! Please set the 'OPENWEATHER_API_KEY' environment variable.")
elif city:
    with st.spinner("🔄 Fetching weather data..."):
        time.sleep(1)
        data = get_weather(city, unit == "Celsius (°C)")

    if data.get("cod") != 200:
        error_msg = data.get("message", "Unknown error")
        st.error(f"😕 Error: {error_msg}")
        st.code(data)  # Show full API response for debugging
    else:
        weather = data["weather"][0]["description"].title()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        emoji = get_weather_emoji(weather)
        unit_symbol = "°C" if unit == "Celsius (°C)" else "°F"

        # Show Lottie animation (using a working URL)
        anim_url = "https://assets3.lottiefiles.com/packages/lf20_jbrw3hcz.json"  # Working sunny animation
        lottie_anim = load_lottieurl(anim_url)
        if lottie_anim:
            st_lottie(lottie_anim, height=200)
        else:
            st.warning("⚠️ Animation could not be loaded.")

        # Weather Output
        st.markdown("---")
        st.markdown("### 🤖 Weather Bot says:")
        st.markdown(f"""
        > **📍 City:** {city.title()}  
        > **{emoji} Conditions:** {weather}  
        > **🌡️ Temperature:** {temperature} {unit_symbol}  
        > **💧 Humidity:** {humidity}%  
        > **🌬️ Wind Speed:** {wind_speed} m/s  
        """)

        # Clothing Suggestion
        temp_celsius = temperature if unit == "Celsius (°C)" else (temperature - 32) * 5/9
        st.info(clothing_tip(temp_celsius))

        st.success("🌈 Hope that helps! Stay safe and dress appropriately!")

# ------------- Surprise Me Button -------------
if st.button("🎁 Surprise Me!"):
    st.balloons()
    facts = [
        "🌍 Did you know? The highest temperature ever recorded on Earth was 56.7°C in Death Valley, California!",
        "☁️ Clouds can weigh more than a million pounds!",
        "❄️ The largest snowflake ever recorded was 15 inches wide!",
        "💨 A hurricane can release the energy of 10 atomic bombs per second!",
    ]
    st.info(f"**Fun Weather Fact:** {facts[int(time.time()) % len(facts)]}")

                                                  



