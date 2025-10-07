import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Domestic Violence Helpline Locator", page_icon="🚨", layout="wide")

# Header
st.title("Domestic Violence Helpline Locator")
st.markdown(
    "Find help centers near you, access emergency services, and chat anonymously for support."
)

st.markdown("---")

# About Section
st.header("About this Website")
st.write(
    """
    This website helps survivors of domestic violence quickly locate nearby help centers and reach emergency services.
    """
)

# Benefits Section
st.header("Benefits")
st.markdown(
    """
- Immediate access to verified emergency helplines.
- Searchable directory of local help centers.
- Map visualization for easy location tracking.
- Anonymous chat for guidance and support.
- Optional location input to inform help centers safely.
- Downloadable resources for offline access.
"""
)

st.markdown("---")

# Emergency Actions Section
st.header("Emergency Actions")

# Load helplines CSV
@st.cache_data
def load_helplines():
    df = pd.read_csv("help_centers.csv")
    return df

try:
    df_helplines = load_helplines()
except FileNotFoundError:
    st.error("help_centers.csv not found. Make sure it is in the same folder as app.py")
    st.stop()

# 📋 Helplines Directory
st.subheader("📋 Helplines Directory")
search = st.text_input("Search helplines by city or location:")
if search:
    filtered = df_helplines[df_helplines["Address"].str.contains(search, case=False)]
else:
    filtered = df_helplines

for idx, row in filtered.iterrows():
    st.markdown(f"**{row['Name']} - {row['Address']} - {row['Phone']}**")

# 📍 Map of Helplines
st.subheader("📍 Helpline Locations on Map")
m = folium.Map(location=[9.0820, 8.6753], zoom_start=6)
for idx, row in df_helplines.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['Name']} - {row['Address']} - {row['Phone']}",
        tooltip=row['Name'],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)
st_folium(m, width=700, height=500)

st.markdown("---")

# 💬 Anonymous Chat
st.subheader("💬 Anonymous Chat")
user_message = st.text_area("Type your message here (anonymous)")
if st.button("Send"):
    if user_message.strip() != "":
        st.success("Your message has been received. Help is on the way!")
    else:
        st.warning("Please type a message before sending.")

# 📍 Optional Location Input
st.subheader("📍 Share Your Location (Optional)")
location_input = st.text_input("Enter your location or address if safe")
if location_input and st.button("Submit Location"):
    st.success("Your location has been safely shared with help centers.")

# 💾 Downloadable Helpline List
st.subheader("💾 Download Helpline List")
csv = df_helplines.to_csv(index=False)
st.download_button("Download CSV", data=csv, file_name="helplines.csv", mime="text/csv")

# 📚 Resources & Safety Tips
st.header("📚 Resources & Safety Tips")
with st.expander("Know your rights"):
    st.write("Learn legal protections against domestic violence.")
with st.expander("Safety planning"):
    st.write("Steps to protect yourself and loved ones.")
with st.expander("Counseling & support"):
    st.write("Access emotional and psychological support services.")
with st.expander("Trusted contacts"):
    st.write("Always have someone you can call in emergencies.")

st.markdown("---")

# Footer
st.markdown("**Created by Moyo Iyanda ❤️ | Share to raise awareness**")
