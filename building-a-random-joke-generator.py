# joke_app.py
# Joke Ninja Pro – Laugh Out Loud Generator!
# Streamlit + Free Joke API = Endless Fun!

import streamlit as st
import requests
import random

# Page Config
st.set_page_config(
    page_title="Joke Ninja Pro",
    page_icon="😂",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);}
    .stApp {background-color: #fff1eb;}
    h1 {color: #ff6b6b !important; text-align: center; font-family: 'Comic Sans MS';}
    .stButton > button {background: #ff6b6b; color: white; font-weight: bold; font-size: 1.5em; border-radius: 20px;}
    .joke-box {background: #fff; padding: 30px; border-radius: 20px; text-align: center; font-size: 1.8em; color: #333; box-shadow: 0 10px 20px rgba(0,0,0,0.1); margin: 20px 0;}
    .punchline {color: #ff6b6b; font-weight: bold;}
    .fav-btn {background: #ffd93d; color: black;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>😂 Joke Ninja Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#666;'>Click for a joke. Laugh. Repeat. Save favorites!</p>", unsafe_allow_html=True)

# Categories
CATEGORIES = ["Any", "Programming", "Misc", "Dark", "Pun", "Spooky", "Christmas"]

# Session State
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'current_joke' not in st.session_state:
    st.session_state.current_joke = None

# Sidebar
with st.sidebar:
    st.header("😂 Settings")
    category = st.selectbox("Category", CATEGORIES)
    blacklist = st.multiselect("Blacklist Flags", ["nsfw", "religious", "political", "racist", "sexist", "explicit"])

# Fetch Joke Function
def get_joke(category, blacklist):
    url = "https://v2.jokeapi.dev/joke/"
    url += category if category != "Any" else "Any"
    params = {
        "blacklistFlags": ",".join(blacklist) if blacklist else "",
        "format": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        if data["error"]:
            return "No joke found! Try different filters."
        if data["type"] == "single":
            return data["joke"]
        else:
            return f"{data['setup']}\n\n<span class='punchline'>{data['delivery']}</span>"
    except:
        return "Oops! Joke server is sleeping. Try again!"

# Generate Joke
if st.button("Tell Me a Joke! 😂", use_container_width=True):
  
    with st.spinner("Fetching a killer joke..."):
        joke = get_joke(category, blacklist)
        st.session_state.current_joke = joke
        st.rerun()

# Display Joke
if st.session_state.current_joke:
    st.markdown(f"<div class='joke-box'>{st.session_state.current_joke}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❤️ Save to Favorites"):
            if st.session_state.current_joke not in st.session_state.favorites:
                st.session_state.favorites.append(st.session_state.current_joke)
                st.success("Saved!")
            st.rerun()
    with col2:
        if st.button("🔄 New Joke"):
            st.session_state.current_joke = None
            st.rerun()

# Favorites
if st.session_state.favorites:
    st.markdown("### ❤️ Your Favorite Jokes")
    for i, joke in enumerate(reversed(st.session_state.favorites)):
        with st.expander(f"Joke #{len(st.session_state.favorites)-i}"):
            st.markdown(joke, unsafe_allow_html=True)
            if st.button("Remove", key=f"remove_{i}"):
                st.session_state.favorites.pop(len(st.session_state.favorites)-1-i)
                st.rerun()

    if st.button("Clear All Favorites"):
        st.session_state.favorites = []
        st.rerun()

# Share
if st.session_state.current_joke:
    share_text = st.session_state.current_joke.replace("<span class='punchline'>", "").replace("</span>", "")
    st.markdown(f"[Share on WhatsApp](https://wa.me/?text={share_text}) | [Copy Joke](javascript:navigator.clipboard.writeText('{share_text}'))")

# Premium
st.markdown("---")
st.info("**Premium ($1.99/mo):** AI-Generated Jokes, PDF Joke Book, Voice Jokes, Daily Jokes Email!")
if st.button("Unlock Pro"):
    st.balloons()

st.caption("Built with Streamlit + JokeAPI + uv | Laughter Guaranteed!")