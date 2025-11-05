# Importamos la librería Streamlit
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.api_client import consultar_pais
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

st.title("Proyecto APP")
st.subheader("Sarita & Rachel")

tab1, tab2, tab3, tab4 = st.tabs(["Datos y limpieza", "API", "Visualización de API", "Visualización de Datos"])
with tab1:
    st.header("Datos y limpieza")
    st.subheader("Datos originales")
    path= r"C:\Users\richa\tu-repo-streamlit\data\pisos_chile_limpio_streamlit.csv"
    df = pd.read_csv(path)
    df = df.drop(columns="id")
    st.dataframe(df.head())
    if st.button("Renombrar columnas"):
        from src.limpieza import snake_columns
        snake_columns(df)
        st.write(f"Los nombres de las columnas se han renombrado como snake_column")
    if st.button("Abrir data"):
        from src.limpieza import open_data
        open_data(df)
    if st.button("Explorar data"):
        from src.limpieza import explore_data
        explore_data(df)
   ##### if st.button("Borrar duplicados"):
   #####     from src.limpieza import borrar_duplicados
   #####     borrar_duplicados(df)
   #####     st.write(f"Los valores duplicados se han borrado, re-eplora la data para comprobar")
   ##### if st.button("Re-Explorar data"):
   #####     from src.limpieza import explore_data
   #####     explore_data(df)
    
with tab2:
    st.header("API")
    
    st.set_page_config(page_title="Consulta de Lugar", layout="centered")

    st.title("🌍 Consulta de información geográfica")

    # Campo de texto
    nombre_pais = st.text_input("Introduce el nombre de un país (por ejemplo, 'España', 'México', 'Argentina'):")

    if st.button("Consultar"):
        if not nombre_pais.strip():
            st.warning("Por favor, escribe un país antes de consultar.")
        else:
            resultado = consultar_pais(nombre_pais)
            if resultado is None:
                st.session_state["resultado"] = None
                st.error("No se encontraron resultados para tu búsqueda.")
            else:
                st.session_state["resultado"] = resultado
                st.success(f"Información del país: {resultado['pais']}")
                st.subheader("📄 Resumen del resultado")
                df3 = pd.DataFrame([resultado])
                st.table(df3)

        
with tab3:
    resultado = st.session_state.get("resultado", None)
    if resultado and resultado.get("lat") and resultado.get("lon"):
        st.subheader(f"🗺️ Capital de {resultado['pais']}: {resultado['capital']}")
        lat = resultado["lat"]
        lon = resultado["lon"]

        # Crear mapa Folium
        m = folium.Map(location=[lat, lon], zoom_start=5)
        folium.Marker(
            [lat, lon],
            popup=f"{resultado['capital']} ({resultado['pais']})",
            tooltip="Capital",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

        # Mostrar mapa en Streamlit
        st_folium(m, width=700, height=500)
    else:
        st.info("No hay coordenadas disponibles para mostrar en el mapa.")
    
with tab4:
    st.title("Santiago de Chile")
    st.subheader("Encuentra la comuna en el mapa")
    from src.visualizacion import show_comuna_map
    from src.visualizacion import show_comuna_statistics
    show_comuna_map()
    
