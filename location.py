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


from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz


import pandas as pd


st.set_page_config(
    page_title="Simple Location Infos",
    page_icon="🧊",
    layout="wide",
)



#####Varible def #######
sound_fileCreated = False


def get_timezone(lat, lon):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=lon, lat=lat)
    return timezone_str


def convert_timestamp_to_readable(timestamp, lat, lon):
    # Convert timestamp to seconds
    timestamp_seconds = timestamp / 1000

    # Detect timezone using latitude and longitude
    timezone_str = get_timezone(lat, lon)

    # Specify the timezone
    timezone = pytz.timezone(timezone_str)

    # Convert the timestamp to a datetime object in the detected timezone
    dt_object = datetime.utcfromtimestamp(timestamp_seconds).replace(tzinfo=pytz.utc).astimezone(timezone)

    # Format the datetime object as 'hh:mm:ss' in the detected timezone
    formatted_time = dt_object.strftime('%H:%M:%S')

    return formatted_time


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


def get_nearby_restaurants(latitude, longitude):
    # Use an API (e.g., Yelp) to get nearby restaurants based on coordinates
    # Replace 'YOUR_YELP_API_KEY' with your actual Yelp API key
    yelp_api_key = 'HIjFe3Ef0MKvDF7A0TJsdyMevXeYyQ_yuvLT89rZ5Nc6AcivbTF0J2qCl_4lVvO0QYTTnzQTfj-i9DOQG2328E48SoO-CT_Nl8hMpLvLZsMIuEUuUVfej2MzYYilZXYx'
    yelp_api_url = 'https://api.yelp.com/v3/businesses/search'

    headers = {'Authorization': f'Bearer {yelp_api_key}'}
    params = {'latitude': latitude, 'longitude': longitude, 'categories': 'restaurants', 'limit': 5}

    response = requests.get(yelp_api_url, headers=headers, params=params)
    data = response.json()

    return data['businesses']


def get_nearby_charging_stations(latitude, longitude):
    # Use Open Charge Map API to get nearby EV charging stations
    # Replace 'YOUR_OCM_API_KEY' with your actual Open Charge Map API key
    ocm_api_key = '2d4b6129-05b6-4dd8-8e06-66584b7a3bc0'
    ocm_api_url = 'https://api.openchargemap.io/v3/poi/'

    params = {
        'output': 'json',
        'latitude': lat,
        'longitude': long,
        'distance': 30,  # Search radius in kilometers
        'distanceunit': 'KM',
        'countrycode': 'CH',  # Replace with the appropriate country code
        'maxresults': 10  # Maximum number of results
    }

    headers = {'X-API-Key': ocm_api_key}

    response = requests.get(ocm_api_url, params=params, headers=headers)
    data = response.json()

    return data






st.title("Simple Locationinfo")

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


        timestamp = loc['timestamp']
        formatted_time = convert_timestamp_to_readable(timestamp, lat, long)

        st.write("Formatted Time:", formatted_time)


        if altitude != None:
            st.write("Altitude: ", altitude)

        if speed != None:
            st.write("Speed: ", speed)

        st.write("Latitude: ",lat)
        st.write("Longitude: ", long)

        windowWidth = streamlit_js_eval(js_expressions='window.innerWidth', key='SCR_Test')
        #st.write("windowWidth: ",windowWidth)





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

            strasse = location.address.split(",")[1].strip()
            nr = location.address.split(",")[0].strip()

            st.write(strasse + " " + nr)

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



        st.subheader("")

        if location:
            togglecol1, togglecol2, togglecol3 = st.columns(3)

            visaWiki = togglecol1.toggle ("Show Wikipedia Info", value=False,key="hej")
            visaRestaurants = togglecol2.toggle("Show nearest restaurants")
            visaChargingStations = togglecol3.toggle("Show nearby Charging Stations", value=False, key="hej igen")

            # Create a map centered around the location
            map = folium.Map(location=[lat, long], zoom_start=15)
            folium.Marker(
                [lat, long], popup=Town, tooltip=Town
            ).add_to(map)
            # Display the map
            #st_data = st_folium(map, width=600)


            wikiTextZumVorlesen = ""
            if visaWiki:

                if windowWidth < 1000:
                    nearest_town = st.selectbox("Choose location", options=location_adress, index=3)
                else:
                    nearest_town = st.sidebar.selectbox("Choose location", options=location_adress, index=3)


                wiki_info1 = scrape_wikipedia(nearest_town)
                if wiki_info1 != None:

                    if windowWidth < 1000:
                        st.subheader(f"{nearest_town}")
                        st.write(wiki_info1)
                    else:
                        st.sidebar.subheader(f"{nearest_town}")
                        st.sidebar.write(wiki_info1)

                    wikiTextZumVorlesen = wiki_info1
                else:
                    st.info("Did not find " + nearest_town + " on Wikipedia")
                    wiki_info2 = scrape_wikipedia(Town)
                    wikiTextZumVorlesen = wiki_info2
                    if wiki_info2 != None:
                        if windowWidth < 1000:
                            st.subheader(f"{Town}")
                            st.write(wiki_info2)
                        else:
                            st.sidebar.subheader(f"{Town}")
                            st.sidebar.write(wiki_info2)

                    else:
                        wiki_info3 = scrape_wikipedia(Admin1)
                        wikiTextZumVorlesen = wiki_info3

                        if wiki_info3 != None:
                            if windowWidth < 1000:
                                st.subheader(f"{Admin1}")
                                st.write(wiki_info3)
                            else:
                                st.sidebar.subheader(f"{Admin1}")
                                st.sidebar.write(wiki_info3)
                        else:
                            st.warning("Did not find any info Wikipedia - try a different location")

                if wikiTextZumVorlesen != "":
                    textToSPeech = st.checkbox("Read Infos (Text-to-Speech)")

                    if textToSPeech:
                        st.info("It may take some time before the audio is ready")
                        with st.spinner('Creating audio...'):
                            st.toast('Creating..', icon='😍')
                            sound_file = BytesIO()
                            tts = gTTS(wikiTextZumVorlesen, lang='en')
                            try:
                                tts.write_to_fp(sound_file)
                                sound_fileCreated = True
                            except:
                                st.warning("Could not generate audio")
                                sound_fileCreated = False
                        if sound_fileCreated == True:
                            st.success("Audiofile created")
                            st.audio(sound_file)




            if visaRestaurants:
                # Display nearby restaurants
                restaurants = get_nearby_restaurants(lat, long)

                # Create a Pandas DataFrame to store restaurant information
                restaurant_df = pd.DataFrame({
                    'Name': [restaurant['name'] for restaurant in restaurants],
                    'Phone': [restaurant['phone'] for restaurant in restaurants],
                    'Rating': [restaurant['rating'] for restaurant in restaurants],
                    'Location': [f"{restaurant['location']['address1']}, {restaurant['location']['city']}" for
                                 restaurant in restaurants],

                    'Distance': [restaurant['distance'] for restaurant in restaurants],

                    'Category': [f"{restaurant['categories'][0]['title']}" for
                                 restaurant in restaurants],

                    'Reviews on Yelp': [restaurant['review_count'] for restaurant in restaurants],

                    'Latitude': [f"{restaurant['coordinates']['latitude']}" for
                                 restaurant in restaurants],
                    'Longitude': [f"{restaurant['coordinates']['longitude']}" for
                                 restaurant in restaurants],

                })

                restaurant_df.sort_values(by=['Distance'], inplace=True)




                # Add markers for each restaurant
                for i, row in restaurant_df.iterrows():
                    folium.Marker(
                        location=[row['Latitude'], row['Longitude']],
                        popup=f"{row['Name']} - Rating: {row['Rating']}",
                        icon=folium.Icon(color='red'),
                        tooltip=f"{row['Name']} - {row['Category']} - Rating: {row['Rating']}",
                    ).add_to(map)





                # Display the map in Streamlit
                #st_Restaurang_data = st_folium(restaurant_map, width=725)




            if visaChargingStations:

                map_center = (lat, long)

                # Get nearby EV charging stations
                charging_stations = get_nearby_charging_stations(lat, long)


                    

               #alle infos vom api st.write(charging_stations)

                # Create a Pandas DataFrame to store charging station information
                charging_station_df = pd.DataFrame({
                    'Name': [station['AddressInfo']['Title'] for station in charging_stations],
                    'Location': [f"{station['AddressInfo']['AddressLine1']}, {station['AddressInfo']['Town']}" for
                                 station in charging_stations],
                    'Latitude': [station['AddressInfo']['Latitude'] for station in charging_stations],
                    'Longitude': [station['AddressInfo']['Longitude'] for station in charging_stations],
                    'Distance': [station['AddressInfo']['Distance'] for station in charging_stations],
                    'KW': [station['Connections'][0]['PowerKW'] for station in charging_stations],
                    #'Operational': [station['Connections'][0]['StatusType'] for station in charging_stations],
                    'AccessComments': [station['AddressInfo']['AccessComments'] for station in charging_stations],
                    #'AccessComments': [station['AddressInfo']['AccessComments'] for station in charging_stations],
                    #'ID_Test': [station['Connections'][0]['StatusType']['ID'] for station in charging_stations],
                })

                charging_station_df.sort_values(by=['Distance'], inplace=True)



                charging_map = folium.Map(location=map_center, zoom_start=12)
                # Add markers for charging stations
                for i, row in charging_station_df.iterrows():
                    folium.Marker(
                        location=[row['Latitude'], row['Longitude']],
                        popup=f"{row['Name']}\n{row['Location']}\n - KW: {row['KW']}",
                        tooltip=f"{row['Name']}\n{row['Location']}\n  - KW:  {row['KW']}",
                        icon=folium.Icon(color='green', icon='plug')  # Green marker for charging stations
                    ).add_to(map)


                # Display the map in Streamlit
                #st_charging_data = st_folium(charging_map, width=725)


            # Display the map
            st_data= st_folium(map, width=1200)

            if visaRestaurants:
                st.subheader("")
                st.subheader("Nearest Restaurants (from Yelp)")
                st.write(restaurant_df)

                # Alle infos in der Api: st.write(restaurants)

            if visaChargingStations:
                st.subheader("")

                # Display the DataFrame
                st.subheader("Nearby Charging Stations:")
                st.write(charging_station_df)

                chargingApiInfo = st.toggle("Show Open Charging Map API Info")
                if chargingApiInfo:
                    st.sidebar.write(charging_stations)
