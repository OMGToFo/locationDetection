#2024.09.15 update mit manueller Ortseingabe

import streamlit as st
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import json

import requests
from bs4 import BeautifulSoup

import time

from datetime import datetime
from datetime import date
from datetime import timedelta


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


from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter



#password secrets handling
import os
from dotenv import load_dotenv
load_dotenv(".env")

api_key =  os.getenv("googleMaps_api_key")
chargeMaps_api_key = os.getenv("ocm_api_key")
yelpApiKey = os.getenv("yelp_api_key")
X_RapidAPI_Key = os.getenv("X-RapidAPI-Key")



st.set_page_config(
    page_title="Simple Location Infos",
    page_icon="🧊",
    layout="wide",
)



#####Varible def #######
sound_fileCreated = False



#####get time #######################################

today = date.today()
todayString = str(today)

tomorrow = today + timedelta(1)




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



def get_lat_long_from_address(address):
   locator = Nominatim(user_agent='thomasTest')
   location = locator.geocode(address)

   return str(location.latitude) +"," + str(location.longitude)




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
    yelp_api_key = yelpApiKey
    yelp_api_url = 'https://api.yelp.com/v3/businesses/search'

    headers = {'Authorization': f'Bearer {yelp_api_key}'}
    params = {'latitude': latitude, 'longitude': longitude, 'categories': 'restaurants', 'limit': 5}

    response = requests.get(yelp_api_url, headers=headers, params=params)
    data = response.json()

    return data['businesses']


def get_nearby_charging_stations(latitude, longitude):
    # Use Open Charge Map API to get nearby EV charging stations
    # Replace 'YOUR_OCM_API_KEY' with your actual Open Charge Map API key
    ocm_api_key = chargeMaps_api_key
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



# Define the list of google type words
typeList = [
    "restaurant","accounting", "airport", "amusement_park", "aquarium", "art_gallery",
    "atm", "bakery", "bank", "bar", "beauty_salon", "bicycle_store",
    "book_store", "bowling_alley", "bus_station", "cafe", "campground",
    "car_dealer", "car_rental", "car_repair", "car_wash", "casino", "cemetery",
    "church", "city_hall", "clothing_store", "convenience_store", "courthouse",
    "dentist", "department_store", "doctor", "drugstore", "electrician",
    "electronics_store", "embassy", "fire_station", "florist", "funeral_home",
    "furniture_store", "gas_station", "gym", "hair_care", "hardware_store",
    "hindu_temple", "home_goods_store", "hospital", "insurance_agency",
    "jewelry_store", "laundry", "lawyer", "library", "light_rail_station",
    "liquor_store", "local_government_office", "locksmith", "lodging",
    "meal_delivery", "meal_takeaway", "mosque", "movie_rental", "movie_theater",
    "moving_company", "museum", "night_club", "painter", "park", "parking",
    "pet_store", "pharmacy", "physiotherapist", "plumber", "police", "post_office",
    "primary_school", "real_estate_agency", "POI", "roofing_contractor",
    "rv_park", "school", "secondary_school", "shoe_store", "shopping_mall", "spa",
    "stadium", "storage", "store", "subway_station", "supermarket", "synagogue",
    "taxi_stand", "tourist_attraction", "train_station", "transit_station",
    "travel_agency", "university", "veterinary_care", "zoo"
]



st.title("Simple Locationinfo")

#if st.checkbox("Check my location", value=True):
if 1 == 1:
    loc = get_geolocation()
    if loc:

        gelocExpander = st.expander("Show geolocation data of your location:")
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

        #Nomatim - extract the detected location adress
        actualLocation = (lat, long)
        # Initialize Nominatim API
        geolocator = Nominatim(user_agent="actualLocationAdress")

        # Get the location (address)
        ActuallocationAdress = geolocator.reverse(actualLocation, exactly_one=True)
        time.sleep(1)

        # Extract the address
        Actualaddress = ActuallocationAdress.address
        # Output the address
        #st.write(f"The address detected for yor location is: {Actualaddress}")

        actualLocationInput = st.text_input("  ", value=Actualaddress)

        if actualLocationInput != Actualaddress:
            #st.info(actualLocationInput)

            # Initialize geolocator
            geolocator = Nominatim(user_agent="geoapiThomasRouting")

            # Add rate limiter to avoid overwhelming the geocoding service
            geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

            newlocation = geolocator.geocode(actualLocationInput)
            st.write("Latitude: ",newlocation.latitude)
            st.write("Longitude: ",newlocation.longitude)
            lat = newlocation.latitude
            long = newlocation.longitude



        windowWidth = streamlit_js_eval(js_expressions='window.innerWidth', key='SCR_Test')
        #st.write("windowWidth: ",windowWidth)




        #st.write(f"Your coordinates are Latitude: {latitude}, Longitude: {longitude}")


        st.subheader("")

        locationInfoCol1, locationInfoCol2 = st.columns(2)

        from geopy.geocoders import Nominatim ########################

        time.sleep(1)

        geolocator = Nominatim(user_agent="nearest-town-finder")
        location = geolocator.reverse((lat, long), exactly_one=True)
        if location:
            location_adress = location.address.split(",")

            nearest_town = location.address.split(",")[3].strip()

            strasse = location.address.split(",")[1].strip()
            nr = location.address.split(",")[0].strip()

            location_adressExpander = locationInfoCol1.expander("location_adress by Nominatim")
            with location_adressExpander:
                st.write("location_adress by Nominatim geolocator: ", location_adress)
                st.write(strasse + " " + nr)
                st.write("nearest_town:", nearest_town)

        st.subheader("")

        import reverse_geocoder as rg ################################
        coordinates = (lat, long)
        searchLokalInfo = rg.search(coordinates)
        if searchLokalInfo:



            searchLokalInfo_name = [x.get('name') for x in searchLokalInfo]
            #st.write("searchLokalInfo_name: ", searchLokalInfo_name)
            Town = searchLokalInfo_name[0]


            searchLokalInfo_admin1 = [y.get('admin1') for y in searchLokalInfo]
            Admin1 = searchLokalInfo_admin1[0]

            searchLokalInfoExpander = locationInfoCol2.expander("searchLokalInfo by reverse_geocoder")
            with searchLokalInfoExpander:
                st.write("searchLokalInfo by reverse_geocoder: ",searchLokalInfo)
                st.write("Town: ", Town)
                st.write("Admin1: ", Admin1)



        st.subheader("")

        if location:
            togglecol1, togglecol2, togglecol3 = st.columns(3)

            visaWiki = togglecol1.toggle ("Show Wikipedia Info", value=True,key="hej")
            visaRestaurants = togglecol2.toggle("Show nearest restaurants (from Yelp)")
            visaChargingStations = togglecol3.toggle("Show nearby Charging Stations", value=False, key="hej igen")

            togglecol4, togglecol5, togglecol6 = st.columns(3)

            visaGooglePOI = togglecol4.toggle("Show POIs by Google", value=False, key="hey Google")
            if visaGooglePOI:
                eingabeCol1, eingabeCol2 = st.columns([1, 4])

                radiusEingabe = eingabeCol1.number_input("Radius (km)", value=1)
                radiusEingabe = radiusEingabe * 1000

                # Create a select box for the user to choose from the list
                selected_type = eingabeCol2.selectbox("Choose a type", typeList)



            visaBookingComHotel = togglecol5.toggle("Show Hotels from Booking.com", value=False, key="hey BookingCom")
            if visaBookingComHotel:
                st.divider()
                st.text("Settings for Hotel Bookings:")
                bookingCo1, bookingCol2, bookingCol3 = st.columns(3)
                numerOfAdults = bookingCo1.number_input("Number of adults", value=1)
                numerOfAdultsString = str(numerOfAdults)

                CheckInDate = bookingCol2.date_input("Check-In Date", today, key="end")
                CheckOutDate = bookingCol3.date_input("Check-Out Date", tomorrow, key="start")
                st.divider()








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
                    if actualLocationInput != actualLocation:
                        location_adress.insert(0,actualLocationInput)
                        nearest_town = st.selectbox("Choose location", options=location_adress, index=0)
                    else:
                        nearest_town = st.selectbox("Choose location", options=location_adress, index=3)

                if windowWidth >= 1000:
                    if actualLocationInput != actualLocation:
                        location_adress.insert(0,actualLocationInput)

                        nearest_town = st.sidebar.selectbox("Choose location", options=location_adress, index=0)
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
                    st.sidebar.info("Did not find " + nearest_town + " on Wikipedia")
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
                # Display nearby restaurants by Yelp
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
                    'UsageCost': [station['UsageCost'] for station in charging_stations],
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






            ########### Fetch POI Data from Google API ###############################

            if visaGooglePOI:

                # Function to fetch nearby POIs using Google Places API
                def get_nearby_POI(api_key, latitude, longitude, radius=radiusEingabe, types=selected_type):
                    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                    params = {
                        'location': f'{lat},{long}',
                        'radius': radius,
                        'types': types,
                        'key': api_key,
                    }
                    response = requests.get(base_url, params=params)
                    data = response.json()
                    return data.get('results', [])


                # Google Map Api
                # Create a list to store DataFrames for each POI
                POI_dfs = []

                # Create a DataFrame to store POI information
                columns = ['Name', 'Type', 'Price Level', 'Rating', 'Opening Hours']
                POI_df = pd.DataFrame(columns=columns)

                POIs = get_nearby_POI(api_key, lat, long)
                sorted_POIs = sorted(POIs, key=lambda x: x.get('name', 'N/A'))

                # Display the results and populate the DataFrame
                if POIs:

                    for idx, POI in enumerate(sorted_POIs):
                        name = POI.get('name', 'N/A')
                        r_type = ', '.join(POI.get('types', []))
                        price_level = POI.get('price_level', 'N/A')
                        rating = POI.get('rating', 'N/A')
                        lat = POI['geometry']['location']['lat']
                        lng = POI['geometry']['location']['lng']

                        # Add marker for each POI
                        folium.Marker(
                            location=[lat, lng],
                            popup=selected_type,
                            tooltip=f"{idx}. {selected_type} - {name}",
                            icon=folium.Icon(color='orange')
                        ).add_to(map)

                        # Extracting opening hours
                        opening_hours = POI.get('opening_hours', {}).get('weekday_text', 'N/A')

                        # st.write(f"- {name} ({r_type}): Rating - {rating}, Price Level - {price_level}")

                        # Append data to DataFrame
                        POI_df = pd.DataFrame([{
                            'Name': name,
                            'Type': r_type,
                            'Price Level': price_level,
                            'Rating': rating,
                            'Opening Hours': opening_hours,
                            'lat': lat,
                            'lng': lng

                        }])

                        # Add the DataFrame to the list
                        POI_dfs.append(POI_df)

                    # Concatenate the list of DataFrames into a single DataFrame
                    POI_df = pd.concat(POI_dfs, ignore_index=True)



                else:
                    st.warning("No Google Maps Api locations found nearby.")

            if visaBookingComHotel:  ##########################

                # API request setup
                url = "https://booking-com.p.rapidapi.com/v1/hotels/search-by-coordinates"

                querystring = {
                    "adults_number": numerOfAdultsString,
                    "checkin_date": CheckInDate,
                    "children_number": "1",
                    "locale": "en-gb",
                    "room_number": "1",
                    "units": "metric",
                    "filter_by_currency": "CHF",
                    "longitude": str(long),
                    "children_ages": "5,0",
                    "checkout_date": CheckOutDate,
                    "latitude": str(lat),
                    "order_by": "popularity",
                    "include_adjacency": "true",
                    "page_number": "0",
                    "categories_filter_ids": "class::2,class::4,free_cancellation::1"
                }

                headers = {
                    "x-rapidapi-key": X_RapidAPI_Key,
                    "x-rapidapi-host": "booking-com.p.rapidapi.com"
                }

                # Send the request
                response = requests.get(url, headers=headers, params=querystring)

                # st.info(response.status_code)

                if response.status_code == 200:

                    # Extract JSON data
                    data = response.json()

                    # Extract the required information for each hotel
                    hotels = data.get("result", [])

                    if (len(hotels)) == 0:
                        st.warning("Found no available hotels on booking.com")

                    if (len(hotels)) > 0:
                        # Define the columns and extract data
                        hotel_data = []
                        for hotel in hotels:
                            hotel_info = {
                                "hotel_name": hotel.get("hotel_name"),
                                "address": hotel.get("address"),
                                "min_total_price": hotel.get("min_total_price"),
                                "address_trans": hotel.get("address_trans"),
                                "city_name_en": hotel.get("city_name_en"),
                                "url": hotel.get("url"),
                                "city": hotel.get("city"),
                                "distance": hotel.get("distance"),
                                "review_score": hotel.get("review_score"),
                                "review_score_word": hotel.get("review_score_word"),
                                "latitude": hotel.get("latitude"),
                                "longitude": hotel.get("longitude"),

                            }
                            hotel_data.append(hotel_info)

                        # Convert to DataFrame
                        df = pd.DataFrame(hotel_data)

                        # Reorder the columns to have "hotel_name" as the first column
                        df = df[[
                            "hotel_name",
                            "address",
                            "min_total_price",
                            "address_trans",
                            "city_name_en",
                            "url",
                            "city",
                            "distance",
                            "review_score",
                            "review_score_word",
                            "latitude",
                            "longitude"
                        ]]

                        df.sort_values(by='distance', ascending=True)

                        # Display the DataFrame using Streamlit
                        # st.write(df)

                        # Create a Folium map centered around the average coordinates
                        # map_center = [df['latitude'].mean(), df['longitude'].mean()]
                        # mymap = folium.Map(location=map_center, zoom_start=12)

                        # Add markers to the map
                        # marker_cluster = MarkerCluster().add_to(mymap)

                        for index, row in df.iterrows():
                            # Create a popup with the hotel name and other details
                            # popup_text = f"<b>{row['hotel_name']}</b><br>Price: {row['min_total_price']} AED<br>Review: {row['review_score']} ({row['review_score_word']})"

                            # Add a marker for each hotel
                            folium.Marker(
                                location=[row['latitude'], row['longitude']],
                                # popup=folium.Popup(popup_text, max_width=300),
                                popup=f"{row['hotel_name']}<br>Review score: {row['review_score']}<br>Min Price: {row['min_total_price']}<br>Review: {row['review_score_word']}<br><a href='{row['url']}' target='_blank'>Hotel Link</a>",
                                tooltip=row["hotel_name"],
                                icon=folium.Icon(icon="hotel", prefix="fa")  # Using Font Awesome hotel icon
                            ).add_to(map)

                else:
                    st.warning("No hotels found.")







            # Display the map #####################
            st_data= st_folium(map, width=1200)


            if visaGooglePOI:
                # Display DataFrame
                # st.write("\n**Information DataFrame:**")
                if len(POI_df) > 1:
                    st.subheader(f"{selected_type}" + "s" + " at Destination - by Google Maps Api")
                    st.dataframe(POI_df)
                if len(POI_df) == 1:
                    st.subheader(f"{selected_type}" + " at Destination - by Google Maps Api")
                    st.dataframe(POI_df)



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


            if visaBookingComHotel:  ##########################
                st.subheader("")
                st.info("Nearby Hotels with available rooms:")
                st.dataframe(
                    df,
                    column_config={
                        "url": st.column_config.LinkColumn()
            }
        )