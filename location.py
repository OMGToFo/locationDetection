import streamlit as st
import geocoder
from geopy.geocoders import Nominatim


def get_user_location():
    try:
        # Using geocoder to get the user's location
        location = geocoder.ip('me').latlng
        return location
    except Exception as e:
        st.error(f"Error fetching location: {e}")
        return None


def get_nearest_city(latitude, longitude):
    geolocator = Nominatim(user_agent="location-detector")
    location = geolocator.reverse((latitude, longitude), language='en')

    # Extracting the city name from the address
    city = None
    if location and location.raw.get('address', {}).get('city'):
        city = location.raw['address']['city']
    elif location and location.raw.get('address', {}).get('town'):
        city = location.raw['address']['town']
    elif location and location.raw.get('address', {}).get('village'):
        city = location.raw['address']['village']

    return city if city else "Unknown"


def main():
    st.title("Location Detector App")

    if st.button("Get My Location"):
        location = get_user_location()
        if location:
            st.success(f"Your location: Latitude {location[0]}, Longitude {location[1]}")

            nearest_city = get_nearest_city(location[0], location[1])
            st.info(f"Nearest city: {nearest_city}")


if __name__ == "__main__":
    main()
