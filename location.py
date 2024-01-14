import streamlit as st
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import json

import requests
from bs4 import BeautifulSoup

import time


from datetime import datetime




#text to speech
from gtts import gTTS
from io import BytesIO

#mapping

import folium
from streamlit_folium import st_folium


_=""" Interesting but not here
st.write(
    f"User agent is _{streamlit_js_eval(js_expressions='window.navigator.userAgent', want_output=True, key='UA')}_")

st.write(f"Screen width is _{streamlit_js_eval(js_expressions='screen.width', want_output=True, key='SCR')}_")

st.write(
    f"Browser language is _{streamlit_js_eval(js_expressions='window.navigator.language', want_output=True, key='LANG')}_")

st.write(
    f"Page location is _{streamlit_js_eval(js_expressions='window.location.origin', want_output=True, key='LOC')}_")


"""

# Copying to clipboard only works with a HTTP connection

#copy_to_clipboard("Text to be copied!", "Copy something to clipboard (only on HTTPS)", "Successfully copied",
   #               component_key="CLPBRD")

# Share something using the sharing API
#create_share_link(dict(
#    {'title': 'streamlit-js-eval', 'url': 'https://github.com/aghasemi/streamlit_js_eval', 'text': "A description"}),
  #                "Share a URL (only on mobile devices)", 'Successfully shared', component_key='shdemo')



# Function to scrape Wikipedia information for a given location name
def scrape_wikipedia(location_name):
    wikipedia_url = f"https://en.wikipedia.org/wiki/{location_name.replace(' ', '_')}"
    response = requests.get(wikipedia_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.find("div", {"id": "mw-content-text"})
        paragraphs = content.find_all("p")
        wiki_info = "\n".join([p.get_text() for p in paragraphs if p.get_text()])
        return wiki_info
    else:
        return None






if st.checkbox("Check my location", value=True):
    loc = get_geolocation()
    if loc:

        gelocExpander = st.expander("Show geolocation data:")
        with gelocExpander:
            st.write(f"Your coordinates are {loc}")

        lat = loc['coords']['latitude']
        long = loc['coords']['longitude']
        altitude = loc['coords']['altitude']
        speed = loc['coords']['speed']
        timestamp = loc['timestamp'] / 1000
        formatted_time = datetime.utcfromtimestamp(timestamp).strftime('%H:%M:%S')

        st.write("Formatted Time:", formatted_time)


        if altitude != None:
            st.write("Altitude: ", altitude)

        if speed != None:
            st.write("Speed: ", speed)

        st.write("Latitude: ",lat)
        st.write("Longitude: ", long)


        #st.write(f"Your coordinates are Latitude: {latitude}, Longitude: {longitude}")


        st.subheader("")

        from geopy.geocoders import Nominatim ########################

        time.sleep(1)

        geolocator = Nominatim(user_agent="nearest-town-finder")
        location = geolocator.reverse((lat, long), exactly_one=True)
        if location:
            location_adress = location.address.split(",")
            location_adressExpander = st.expander("location_adress by Nominatim geolocator")
            with location_adressExpander:
                st.write("location_adress by Nominatim geolocator: ", location_adress)

            nearest_town = location.address.split(",")[3].strip()
            st.write("nearest_town:", nearest_town)

        st.subheader("")

        import reverse_geocoder as rg ################################
        coordinates = (lat, long)
        searchLokalInfo = rg.search(coordinates)
        if searchLokalInfo:

            searchLokalInfoExpander = st.expander("searchLokalInfo by reverse_geocoder")
            with searchLokalInfoExpander:
                st.write("searchLokalInfo by reverse_geocoder: ",searchLokalInfo)

            searchLokalInfo_name = [x.get('name') for x in searchLokalInfo]
            #st.write("searchLokalInfo_name: ", searchLokalInfo_name)
            Town = searchLokalInfo_name[0]
            st.write("Town: ", Town)

            searchLokalInfo_admin1 = [y.get('admin1') for y in searchLokalInfo]
            Admin1 = searchLokalInfo_admin1[0]
            st.write("Admin1: ", Admin1)

        _="""
        geolocator = Nominatim(user_agent="nearest-town-finder")
        location = geolocator.reverse((lat, long), exactly_one=True)
        if location:
            nearest_town2 = location.address.split(",")[2].strip()

            # Variante 3 - Test av search variante - funzt besser! name enthält stadt!
            coordinates = (lat, long)
            searchLokalInfo = rg.search(coordinates)

            #st.write("searchLokalInfo", searchLokalInfo)

            searchLokalInfo_name = [x.get('name') for x in searchLokalInfo]
            Town = searchLokalInfo_name[0]
            #st.write("Town:", Town)

        """

        # Create a map centered around the locations
        map = folium.Map(location=[lat,long], zoom_start=25)
        folium.Marker(
            [lat,long], popup=Town, tooltip=Town
        ).add_to(map)

        # Display the map
        st_data = st_folium(map, width=725)



        st.subheader("")

        if location:
            visaWiki = st.checkbox("Show Wikipedia Info", value=False,key="hej")
            wikiTextZumVorlesen = ""
            if visaWiki:

                nearest_town = st.selectbox("Choose location", options=location_adress, index=3)

                wiki_info1 = scrape_wikipedia(nearest_town)
                if wiki_info1 != None:
                    st.subheader(f"{nearest_town}")
                    st.write(wiki_info1)
                    wikiTextZumVorlesen = wiki_info1
                else:
                    st.info("Did not find " + nearest_town + " on Wikipedia")
                    wiki_info2 = scrape_wikipedia(Town)
                    if wiki_info2 != None:
                        st.subheader(f"{Town}")
                        st.write(wiki_info2)
                        wikiTextZumVorlesen = wiki_info2
                    else:
                        wiki_info3 = scrape_wikipedia(Admin1)
                        if wiki_info3 != None:
                            st.subheader(f"{Admin1}")
                            st.write(wiki_info3)
                            wikiTextZumVorlesen = wiki_info3
                        else:
                            st.warning("Did not find any info Wikipedia - try a different location")

                if wikiTextZumVorlesen != "":
                    textToSPeech = st.checkbox("Read Infos (Text-to-Speech")
                    if textToSPeech:
                        sound_file = BytesIO()
                        tts = gTTS(wikiTextZumVorlesen, lang='en')
                        tts.write_to_fp(sound_file)
                        st.audio(sound_file)
