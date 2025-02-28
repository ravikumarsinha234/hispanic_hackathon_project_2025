from flask import Flask, request, jsonify
from googletrans import Translator
from geopy.geocoders import Nominatim
import osmnx as ox
import folium

app = Flask(__name__)

# Initialize the translator object
translator = Translator()

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    source_text = data.get('source_text')
    target_language = data.get('target_language')
    
    if not source_text or not target_language:
        return jsonify({'error': 'Missing source_text or target_language'}), 400
    
    try:
        translated = translator.translate(source_text, dest=target_language)
        return jsonify({'translated_text': translated.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/nearest_station', methods=['POST'])
def nearest_station():
    data = request.json
    address = data.get('address')
    
    if not address:
        return jsonify({'error': 'Missing address'}), 400
    
    try:
        # Get user's current location
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(address)
        user_location = (location.latitude, location.longitude)

        # Find the nearest Marta station using OSM
        tags = {'railway': 'station', 'subway': 'yes'}
        nearest_stations = ox.geometries_from_point(user_location, tags, dist=5000)

        if not nearest_stations.empty:
            nearest_station = nearest_stations.iloc[0]
            station_name = nearest_station['name']
            station_lat = nearest_station.geometry.centroid.y
            station_lng = nearest_station.geometry.centroid.x

            # Create a map with Folium
            m = folium.Map(location=user_location, zoom_start=14)
            folium.Marker([station_lat, station_lng], popup=station_name).add_to(m)
            folium.Marker(user_location, popup="Your Location", icon=folium.Icon(color='red')).add_to(m)

            # Generate HTML for the map
            map_html = m._repr_html_()

            return jsonify({
                'station_name': station_name,
                'station_lat': station_lat,
                'station_lng': station_lng,
                'map_html': map_html
            })
        else:
            return jsonify({'error': 'No Marta stations found nearby'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)