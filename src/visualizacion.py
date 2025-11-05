import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import seaborn as sns

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

path= "/Users/saraynes.gs/Documents/Ironhack/BigData/Dia 34 - Streamlit_/tu-repo-streamlit/data/pisos_chile_limpio_streamlit.csv"
df = pd.read_csv(path)
df = df.drop(columns="id")

def show_comuna_map():
    if "know" not in st.session_state:
        st.session_state['know'] = None
    if 'comuna_selected' not in st.session_state:
        st.session_state['comuna_selected'] = None
    if 'show_map' not in st.session_state:
        st.session_state['show_map'] = False
    if 'show_stats' not in st.session_state:
        st.session_state['show_stats'] = False

    # User makes selection regarding knowledge of province or comuna
    button_col1, button_col2 = st.columns(2)
    with button_col1:
        if st.button("Sé la provincia", key="province_button"):
            st.session_state['know'] = 'province'
    with button_col2:
        if st.button("Sé la comuna", key="comuna_button"):
            st.session_state['know'] = 'comuna'

    # Dropdown logic for province or comuna
    if st.session_state['know'] == 'province':
        province_selected = st.selectbox("Seleccione una provincia:", options=list(provinces_comunas.keys()), key="province_selectbox")
        comunas = provinces_comunas[province_selected]
        st.session_state['comuna_selected'] = st.selectbox("Seleccione una comuna:", options=comunas, key="comuna_selectbox_province")
    elif st.session_state['know'] == 'comuna':
        all_comunas = [comuna for sublist in provinces_comunas.values() for comuna in sublist]
        st.session_state['comuna_selected'] = st.selectbox("Seleccione una comuna:", options=all_comunas, key="comuna_selectbox_all")

    # Map display logic
    if st.session_state['comuna_selected'] and st.button("Encontrar en el mapa", key="find_map_button"):
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

    # Button to show statistics
    if st.session_state['comuna_selected'] and st.button("Resumen de oferta", key="show_stats_button"):
        st.session_state['show_stats'] = True

    if st.session_state['show_stats']:
        show_comuna_statistics(df, st.session_state['comuna_selected'])

def show_comuna_statistics(all_data, comuna_selected):
    st.subheader(f"Resumen de las ofertas en la comuna: {comuna_selected}")

    # Transform selected comuna for consistency with data
    comuna_selected = comuna_selected.lower()

    # Filter data for the selected comuna
    comuna_data = all_data[all_data['comuna'] == comuna_selected]

    if comuna_data.empty:
        st.write("No hay ofertas en esta comuna")
    else:
        st.write("Seleccione una característica para ver su distribución:")
        
        # Using Streamlit's container to hold buttons
        with st.container():

                if st.button("Precios", key="precios_button"):
                    show_boxplots(all_data, comuna_data, 'precio', comuna_selected)

                if st.button("Gastos Comunes", key="gastos_comunes_button"):
                    show_boxplots(all_data, comuna_data, 'gastos_comunes', comuna_selected)

                if st.button("Superficie Total", key="superficie_total_button"):
                    show_boxplots(all_data, comuna_data, 'superficie_total', comuna_selected)

def show_boxplots(all_data, comuna_data, variable, comuna_selected):
    # Create boxplots for all comunas together
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='comuna', y=variable, data=all_data, ax=ax, color='skyblue')
    ax.set_title(f"Boxplot de {variable} para todas las comunas")
    
    # Rotate x-axis labels
    plt.xticks(rotation=90)
    plt.xlabel('Comuna')
    plt.ylabel(variable.capitalize())

    # Display the plot
    st.pyplot(fig)