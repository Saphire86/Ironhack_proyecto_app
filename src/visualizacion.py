# visualization.py
import streamlit as st
import folium
from streamlit_folium import st_folium

provinces_comunas = {
    "Chacabuco": ["Colina", "Lampa", "Til Til"],
    "Cordillera": ["Pirque", "Puente Alto", "San José de Maipo"],
    "Maipo": ["Buin", "Calera de Tango", "Paine", "San Bernardo"],
    "Melipilla": ["Alhué", "Curacaví", "María Pinto", "Melipilla", "San Pedro"],
    "Santiago": [
        "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central",
        "Huechuraba", "Independencia", "La Cisterna", "La Granja", "La Florida",
        "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo",
        "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén",
        "Providencia", "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta", "Renca",
        "San Miguel", "San Joaquín", "San Ramón", "Santiago", "Vitacura"
    ],
    "Talagante": ["El Monte", "Isla de Maipo", "Padre Hurtado", "Peñaflor", "Talagante"]
}

comuna_coordinates = {
    "Colina": [-33.2102, -70.6692],
    "Lampa": [-33.2883, -70.8720],
    "Tiltil": [-33.0806, -70.9243],
    "Pirque": [-33.6692, -70.5684],
    "Puente Alto": [-33.5869, -70.5671],
    "San José de Maipo": [-33.6404, -70.3314],
    "Buin": [-33.7303, -70.7464],
    "Calera de Tango": [-33.6221, -70.7830],
    "Paine": [-33.8234, -70.7343],
    "San Bernardo": [-33.5695, -70.7376],
    "Alhué": [-34.0383, -71.1112],
    "Curacaví": [-33.4067, -71.1284],
    "María Pinto": [-33.5327, -71.1342],
    "Melipilla": [-33.6886, -71.2139],
    "San Pedro": [-33.9497, -71.4330],
    "Cerrillos": [-33.4978, -70.7164],
    "Cerro Navia": [-33.4232, -70.7403],
    "Conchalí": [-33.3837, -70.6749],
    "El Bosque": [-33.5657, -70.6728],
    "Estación Central": [-33.4660, -70.7034],
    "Huechuraba": [-33.3655, -70.6505],
    "Independencia": [-33.4137, -70.6658],
    "La Cisterna": [-33.5257, -70.6606],
    "La Granja": [-33.5361, -70.6239],
    "La Florida": [-33.5363, -70.5822],
    "La Pintana": [-33.5659, -70.6321],
    "La Reina": [-33.4490, -70.5503],
    "Las Condes": [-33.4119, -70.5685],
    "Lo Barnechea": [-33.3534, -70.5086],
    "Lo Espejo": [-33.5171, -70.6901],
    "Lo Prado": [-33.4257, -70.7501],
    "Macul": [-33.4895, -70.5968],
    "Maipú": [-33.5114, -70.7696],
    "Ñuñoa": [-33.4506, -70.5907],
    "Pedro Aguirre Cerda": [-33.4931, -70.6761],
    "Peñalolén": [-33.4841, -70.5573],
    "Providencia": [-33.4340, -70.6105],
    "Pudahuel": [-33.4458, -70.7653],
    "Quilicura": [-33.3612, -70.7319],
    "Quinta Normal": [-33.4246, -70.7019],
    "Recoleta": [-33.3974, -70.6431],
    "Renca": [-33.4034, -70.7213],
    "San Miguel": [-33.5007, -70.6514],
    "San Joaquín": [-33.4975, -70.6287],
    "San Ramón": [-33.4274, -70.4843],
    "Santiago": [-33.4624, -70.6491],
    "Vitacura": [-33.3867, -70.5688],
    "El Monte": [-33.6936, -71.0118],
    "Isla de Maipo": [-33.7509, -70.8983],
    "Padre Hurtado": [-33.5719, -70.8068],
    "Peñaflor": [-33.5985, -70.8734],
    "Talagante": [-33.6844, -70.9248]
}

def show_comuna_map():
    # Check if in Streamlit app context
    if "know" not in st.session_state:
        st.session_state['know'] = None
    if 'comuna_selected' not in st.session_state:
        st.session_state['comuna_selected'] = None
    if 'show_map' not in st.session_state:
        st.session_state['show_map'] = False

    button_col1, button_col2 = st.columns(2)
    with button_col1:
        if st.button("Sé la provincia"):
            st.session_state['know'] = 'province'
    with button_col2:
        if st.button("Sé la comuna"):
            st.session_state['know'] = 'comuna'

    if st.session_state['know'] == 'province':
        province_selected = st.selectbox("Seleccione una provincia:", options=list(provinces_comunas.keys()))
        comunas = provinces_comunas[province_selected]
        st.session_state['comuna_selected'] = st.selectbox("Seleccione una comuna:", options=comunas)
    elif st.session_state['know'] == 'comuna':
        all_comunas = [comuna for sublist in provinces_comunas.values() for comuna in sublist]
        st.session_state['comuna_selected'] = st.selectbox("Seleccione una comuna:", options=all_comunas)

    if st.session_state['comuna_selected'] and st.button("Encontrar en el mapa"):
        st.session_state['show_map'] = True

    if st.session_state['show_map']:
        comuna = st.session_state['comuna_selected']
        if comuna in comuna_coordinates:
            centro = comuna_coordinates[comuna]
            m = folium.Map(location=centro, zoom_start=12)
            folium.Marker(location=centro, popup=comuna).add_to(m)
            st_folium(m, width=700, height=500)
        else:
            st.warning("Coordenadas no disponibles para la comuna seleccionada.")