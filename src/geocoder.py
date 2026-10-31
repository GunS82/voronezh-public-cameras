from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

geolocator = Nominatim(user_agent="VoronezhCamParser/1.0")

def geocode_address(address, city="Воронеж"):
    try:
        location = geolocator.geocode(f"{city}, {address}", timeout=5)
        if location:
            return location.latitude, location.longitude
        
        # fallback: try just the address without city context if it already contains it
        if city.lower() not in address.lower():
            return None, None
        
        location = geolocator.geocode(address, timeout=5)
        if location:
            return location.latitude, location.longitude
            
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error for {address}: {e}")
        pass
    
    return None, None

def enhance_with_coords(camera):
    if camera.get('lat') is None or camera.get('lng') is None:
        lat, lng = geocode_address(camera['title'])
        if lat and lng:
            camera['lat'] = lat
            camera['lng'] = lng
            print(f"Found coords for {camera['title']}: {lat}, {lng}")
        time.sleep(1) # respect Nominatim usage policy
    return camera
