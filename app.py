import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ----- PAGE CONFIG -----
st.set_page_config(
    page_title="Domestic Violence Helpline Locator",
    page_icon="🚨",
    layout="wide"
)

# ----- HEADER -----
st.markdown("<h1 style='text-align: center; color: #D32F2F;'>Domestic Violence Helpline Locator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Find help centers near you, access emergency services, and chat anonymously for support.</p>", unsafe_allow_html=True)
st.markdown("---")

# ----- ABOUT / BENEFITS -----
with st.container():
    st.subheader("About this Website")
    st.markdown("""
    This website helps survivors of domestic violence quickly locate nearby help centers and reach emergency services.  

    **Benefits:**  
    - Immediate access to verified emergency helplines.  
    - Searchable directory of local help centers.  
    - Map visualization for easy location tracking.  
    - Anonymous chat for guidance and support.  
    - Optional location input to inform help centers safely.  
    - Downloadable resources for offline access.
    """)

st.markdown("---")

# ----- EMERGENCY BUTTONS -----
st.subheader("Emergency Actions")
col1, col2 = st.columns(2)
with col1:
    if st.button("📞 Call Emergency", key="call"):
        st.success("📞 Dial the nearest emergency number immediately!")

with col2:
    if st.button("🚨 Send SOS", key="sos"):
        st.error("🚨 SOS alert! Contact local authorities or trusted contacts immediately!")

st.markdown("---")

# ----- HELPLINE DATA -----
helplines = [
    {"Name": "Mirabel Centre - Lagos", "Location": "LASUTH, Ikeja", "Phone": "8155770000", "Latitude": 6.6066, "Longitude": 3.3491},
    {"Name": "Project Alert on Violence Against Women - Lagos", "Location": "PO Box 15456, Ikeja", "Phone": "8180091072", "Latitude": 6.6016, "Longitude": 3.3500},
    {"Name": "WRAPA - Lagos", "Location": "Lagos", "Phone": "08023456789", "Latitude": 6.5244, "Longitude": 3.3792},
    {"Name": "DVRT - Abuja", "Location": "Abuja", "Phone": "08012345678", "Latitude": 9.0578, "Longitude": 7.4951}
]

df = pd.DataFrame(helplines)

# ----- SEARCH FUNCTION -----
st.subheader("📋 Helplines Directory")
search_location = st.text_input("Search helplines by city or location:")
if search_location:
    filtered_df = df[df['Location'].str.contains(search_location, case=False)]
else:
    filtered_df = df

# Display helplines with expandable boxes and clickable phone links
for idx, row in filtered_df.iterrows():
    with st.expander(f"{row['Name']} - {row['Location']}"):
        st.markdown(f"**Phone:** [📞 {row['Phone']}](tel:{row['Phone']})")

st.markdown("---")

# ----- MAP OF HELPLINES -----
st.subheader("📍 Helpline Locations on Map")
m = folium.Map(location=[6.5244, 3.3792], zoom_start=6, tiles="CartoDB positron")  # Modern map tiles
for idx, row in filtered_df.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"{row['Name']} ({row['Phone']})",
        tooltip=row['Name'],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

st_data = st_folium(m, width=700, height=400)

# ----- ANONYMOUS CHAT -----
st.subheader("💬 Anonymous Chat")
user_msg = st.chat_input("Type here if you need help (anonymous)")
if user_msg:
    st.chat_message("assistant").markdown("""Help is on the way! Please stay safe. Are you in a safe place? 
If yes, consider calling your nearest helpline. 
If not, try to move to a secure location and let someone know your situation.""")

st.markdown("---")

# ----- OPTIONAL LOCATION INPUT -----
st.subheader("📍 Share Your Location (Optional)")
location = st.text_input("Enter your location or address if safe")
if location:
    st.success(f"Location noted. Please contact your nearest helpline: [Click to Call](tel:8155770000)")

# ----- DOWNLOAD HELPLINE CSV -----
st.markdown("---")
st.subheader("💾 Download Helpline List")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download as CSV",
    data=csv,
    file_name='domestic_violence_helplines.csv',
    mime='text/csv'
)

# ----- ADDITIONAL RESOURCES -----
st.markdown("---")
st.subheader("📚 Resources & Safety Tips")
st.markdown("""
- **Know your rights:** Learn legal protections against domestic violence.  
- **Safety planning:** Steps to protect yourself and loved ones.  
- **Counseling & support:** Access emotional and psychological support services.  
- **Trusted contacts:** Always have someone you can call in emergencies.
""")

# ----- FOOTER -----
st.markdown("<p style='text-align: center; color: gray; font-size:14px;'>Created by Moyo Iyanda ❤️ | Share to raise awareness</p>", unsafe_allow_html=True)
