import streamlit as st 
from googletrans import Translator
from languages import languages
import speech_recognition as sr
import requests
from geopy.geocoders import Nominatim
import osmnx as ox
import folium

# Initialize the translator object
translator = Translator()

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Function to switch language
def switch_language():
    if st.session_state.language == 'en':
        st.session_state.language = 'es'
    else:
        st.session_state.language = 'en'

# Language switch button
st.sidebar.button('Switch to Spanish' if st.session_state.language == 'en' else 'Switch to English', on_click=switch_language)

# Texts in both languages
texts = {
    'en': {
        'title': "Welcome to the Language Translation App",
        'text_input': "Enter the text to translate:",
        'text_in_spanish': "Text in Spanish:",
        'speak_to_translate': "Or speak to translate:",
        'listening': "Listening...",
        'you_said': "You said: ",
        'sorry': "Sorry, I could not understand the audio.",
        'request_error': "Could not request results; ",
        'select_target_language': "Select the target language:",
        'translate': "Translate",
        'transportation_info': "Transportation Information",
        'translate_transport_phrases': "Translate common phrases related to transportation.",
        'enter_transport_phrases': "Enter transportation phrases:",
        'translate_transport_phrases_button': "Translate Transportation Phrases",
        'marta_info': "Marta Information",
        'enter_marta_query': "Enter Marta information query:",
        'get_marta_info': "Get Marta Information",
        'failed_fetch': "Failed to fetch Marta information.",
        'error_occurred': "An error occurred: ",
        'educational_resources': "Educational Resources",
        'translate_educational_materials': "Translate educational materials or access educational resources.",
        'enter_educational_text': "Enter educational text:",
        'translate_educational_text_button': "Translate Educational Text",
        'communication_assistance': "Communication Assistance",
        'translate_communication_phrases': "Translate common phrases used in daily communication.",
        'enter_communication_phrases': "Enter communication phrases:",
        'translate_communication_phrases_button': "Translate Communication Phrases",
        'nearest_station': "Find Nearest Marta Station",
        'navigate_to_station': "Navigate to Nearest Marta Station"
    },
    'es': {
        'title': "Bienvenido a la Aplicación de Traducción de Idiomas",
        'text_input': "Ingrese el texto para traducir:",
        'text_in_spanish': "Texto en español:",
        'speak_to_translate': "O hable para traducir:",
        'listening': "Escuchando...",
        'you_said': "Dijiste: ",
        'sorry': "Lo siento, no pude entender el audio.",
        'request_error': "No se pudieron solicitar resultados; ",
        'select_target_language': "Seleccione el idioma de destino:",
        'translate': "Traducir",
        'transportation_info': "Información de Transporte",
        'translate_transport_phrases': "Traduce frases comunes relacionadas con el transporte.",
        'enter_transport_phrases': "Ingrese frases de transporte:",
        'translate_transport_phrases_button': "Traducir Frases de Transporte",
        'marta_info': "Información de Marta",
        'enter_marta_query': "Ingrese la consulta de información de Marta:",
        'get_marta_info': "Obtener Información de Marta",
        'failed_fetch': "No se pudo obtener información de Marta.",
        'error_occurred': "Ocurrió un error: ",
        'educational_resources': "Recursos Educativos",
        'translate_educational_materials': "Traduce materiales educativos o accede a recursos educativos.",
        'enter_educational_text': "Ingrese texto educativo:",
        'translate_educational_text_button': "Traducir Texto Educativo",
        'communication_assistance': "Asistencia en Comunicación",
        'translate_communication_phrases': "Traduce frases comunes utilizadas en la comunicación diaria.",
        'enter_communication_phrases': "Ingrese frases de comunicación:",
        'translate_communication_phrases_button': "Traducir Frases de Comunicación",
        'nearest_station': "Encuentra la estación Marta más cercana",
        'navigate_to_station': "Navegar a la estación Marta más cercana"
    }
}

# Display the logo image
st.image("marta_logo.png", use_column_width=True)

# Greeting
st.title(texts[st.session_state.language]['title'])

# Text input
st.subheader(texts[st.session_state.language]['text_input'])
source_text = st.text_area(texts[st.session_state.language]['text_in_spanish'])

# Speech input
st.write(texts[st.session_state.language]['speak_to_translate'])
if st.button('Record'):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write(texts[st.session_state.language]['listening'])
        audio = recognizer.listen(source, timeout=15)
        try:
            source_text = recognizer.recognize_google(audio, language='es-ES')
            st.write(f"{texts[st.session_state.language]['you_said']} {source_text}")
        except sr.UnknownValueError:
            st.write(texts[st.session_state.language]['sorry'])
        except sr.RequestError as e:
            st.write(f"{texts[st.session_state.language]['request_error']} {e}")

# Language selection
target_language = st.selectbox(texts[st.session_state.language]['select_target_language'], languages)

# Translation
translate = st.button(texts[st.session_state.language]['translate'])
if translate:
    out = translator.translate(source_text, dest=target_language)
    st.write(out.text)

# Additional Features
st.subheader(texts[st.session_state.language]['transportation_info'])
st.write(texts[st.session_state.language]['translate_transport_phrases'])
transport_phrases = st.text_area(texts[st.session_state.language]['enter_transport_phrases'])
if st.button(texts[st.session_state.language]['translate_transport_phrases_button']):
    out = translator.translate(transport_phrases, dest=target_language)
    st.write(out.text)

st.subheader(texts[st.session_state.language]['marta_info'])
marta_info = st.text_area(texts[st.session_state.language]['enter_marta_query'])
if st.button(texts[st.session_state.language]['get_marta_info']):
    try:
        response = requests.get(f"https://api.marta.com/info?query={marta_info}")
        if response.status_code == 200:
            marta_data = response.json()
            st.write(marta_data)
        else:
            st.write(texts[st.session_state.language]['failed_fetch'])
    except Exception as e:
        st.write(f"{texts[st.session_state.language]['error_occurred']} {e}")

st.subheader(texts[st.session_state.language]['educational_resources'])
st.write(texts[st.session_state.language]['translate_educational_materials'])
education_text = st.text_area(texts[st.session_state.language]['enter_educational_text'])
if st.button(texts[st.session_state.language]['translate_educational_text_button']):
    out = translator.translate(education_text, dest=target_language)
    st.write(out.text)

st.subheader(texts[st.session_state.language]['communication_assistance'])
st.write(texts[st.session_state.language]['translate_communication_phrases'])
communication_phrases = st.text_area(texts[st.session_state.language]['enter_communication_phrases'])
if st.button(texts[st.session_state.language]['translate_communication_phrases_button']):
    out = translator.translate(communication_phrases, dest=target_language)
    st.write(out.text)

# Find and navigate to the nearest Marta station
st.subheader(texts[st.session_state.language]['nearest_station'])
if st.button(texts[st.session_state.language]['navigate_to_station']):
    try:
        # Get user's current location
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode("Your Address Here")  # Replace with actual address or use geolocation API
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

            # Display the map
            st.write(f"Nearest Marta Station: {station_name}")
            st.write(f"[Navigate to {station_name}](https://www.openstreetmap.org/?mlat={station_lat}&mlon={station_lng}#map=18/{station_lat}/{station_lng})")
            st.components.v1.html(m._repr_html_(), height=500)
        else:
            st.write("No Marta stations found nearby.")
    except Exception as e:
        st.write(f"An error occurred: {e}")