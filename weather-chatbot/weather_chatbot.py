from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import requests
import os
import time
from streamlit_lottie import st_lottie

# -------------------- Page Config --------------------

# -------------------- Styling --------------------
import streamlit as st

st.set_page_config(page_title="Weather Buddy ☁️", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .main, .block-container {
        background-color: rgba(0, 76, 153, 0.55);
        padding: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        color: #f0f8ff !important;  /* Slightly brighter white-blue */
        font-weight: 800;  /* Strong boldness */
        text-shadow: 0 0 5px rgba(0,0,0,0.85);  /* Dark shadow for crisp contrast */
    }

    h1, h2, h3, h4, h5, h6, .stMarkdown, .stText {
        color: #e6f2ff !important; /* Very light bluish white */
        font-weight: 900 !important;  /* Extra bold headings */
        text-shadow: 0 0 6px rgba(0,0,0,0.9); /* Strong black shadow for clarity */
    }

    input, .st-bw, .st-dn, .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.25);
        color: #f0f8ff !important;
        border: none;
        font-weight: 900;  /* Bold input text */
        text-shadow: 0 0 4px rgba(0,0,0,0.7);
    }

    input::placeholder {
        color: #d0e7ff !important;
        font-weight: 800;
        text-shadow: none;
    }

    input:hover, .st-bw:hover, .st-dn:hover {
        transform: scale(1.02);
        border: 1px solid #33cfff;
    }

    .stRadio > div {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 0.5em;
        color: #e6f2ff;
        font-weight: 800;
        text-shadow: 0 0 3px rgba(0,0,0,0.7);
    }

    .stButton button {
        background-color: #33cfff;
        color: #f0f8ff;
        border: none;
        border-radius: 6px;
        padding: 0.5em 1.2em;
        transition: background-color 0.3s ease;
        font-weight: 900;
        letter-spacing: 0.03em;
        text-shadow: 0 0 3px rgba(0,0,0,0.7);
    }

    .stButton button:hover {
        background-color: #00aaff;
    }
    </style>
""", unsafe_allow_html=True)        


# Example UI content (replace this part with your actual app logic)
# -------------------- API Key --------------------
api_key = os.getenv("OPENWEATHER_API_KEY")

# -------------------- Emoji Function --------------------
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

# -------------------- Clothing Suggestion --------------------
def clothing_tip(temp_c):
    if temp_c < 5:
        return "🧥 It's freezing! Bundle up!"
    elif temp_c < 15:
        return "🧣 A jacket or sweater is a good idea."
    elif temp_c < 25:
        return "👕 Perfect weather for a t-shirt!"
    else:
        return "🩳 Stay cool! It's quite hot."

# -------------------- Animation Loader --------------------
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# -------------------- Get Weather --------------------
def get_weather(city_name, use_metric=True):
    units = "metric" if use_metric else "imperial"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units={units}"
    return requests.get(url).json()

# -------------------- UI Header --------------------
st.markdown("<h1 style='text-align: center;'>🌤️ Weather Buddy</h1>", unsafe_allow_html=True)
st.markdown("👋 Hello! I'm your friendly weather assistant. Ask me about any city!")

# -------------------- User Input --------------------
city = st.text_input("📍 Which city's weather would you like to check?", placeholder="e.g., London, Tokyo, New York")
unit = st.radio("🌡️ Choose temperature unit:", ["Celsius (°C)", "Fahrenheit (°F)"])

# -------------------- Weather Logic --------------------
if not api_key:
    st.error("🚨 API key is missing! Please set the 'OPENWEATHER_API_KEY' environment variable.")
elif city:
    st.toast(f"👋 Nice choice! Let's see what's happening in {city.title()}...", icon="☁️")

    with st.spinner("🔄 Fetching weather data..."):
        time.sleep(1)
        data = get_weather(city, unit == "Celsius (°C)")

    if data.get("cod") != 200:
        error_msg = data.get("message", "Unknown error")
        st.error(f"😕 Error: {error_msg}")
        st.code(data)  # Optional: for debugging
    else:
        weather = data["weather"][0]["description"].title()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        emoji = get_weather_emoji(weather)
        unit_symbol = "°C" if unit == "Celsius (°C)" else "°F"

        # Show Lottie animation (sunny as default)
        anim_url = "https://assets3.lottiefiles.com/packages/lf20_jbrw3hcz.json"
        lottie_anim = load_lottieurl(anim_url)
        if lottie_anim:
            st_lottie(lottie_anim, height=200)
        else:
            st.warning("⚠️ Animation could not be loaded.")

        # Output Weather Data
        st.markdown("---")
        st.markdown("### 🤖 Weather Bot says:")
        st.markdown(f"""
        > 📍 **City:** `{city.title()}`  
        > {emoji} **Condition:** `{weather}`  
        > 🌡️ **Temperature:** `{temperature} {unit_symbol}`  
        > 💧 **Humidity:** `{humidity}%`  
        > 🌬️ **Wind Speed:** `{wind_speed} m/s`
        """)

        # Suggest Clothes
        temp_celsius = temperature if unit == "Celsius (°C)" else (temperature - 32) * 5 / 9
        st.info(clothing_tip(temp_celsius))
        st.success("🌈 Hope that helps! Stay safe and dress appropriately!")

# -------------------- Fun Button --------------------
if st.button("🎁 Surprise Me!"):
    st.balloons()
    facts = [
        "🌍 The highest temperature ever recorded on Earth was 56.7°C in Death Valley!",
        "☁️ Clouds can weigh more than a million pounds!",
        "❄️ The largest snowflake recorded was 15 inches wide!",
        "💨 A hurricane can release the energy of 10 atomic bombs per second!",
    ]
    st.info(f"*Fun Weather Fact:* {facts[int(time.time()) % len(facts)]}")
