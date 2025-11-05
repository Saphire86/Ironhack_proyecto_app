import requests

def consultar_pais(nombre_pais: str):
    """
    Consulta la API de REST Countries para obtener información
    sobre un país: capital, región, población y coordenadas de la capital.
    """
    if not nombre_pais:
        return None

    url = f"https://restcountries.com/v3.1/name/{nombre_pais}"

    try:
        response = requests.get(url, headers={"User-Agent": "streamlit-app"})
        response.raise_for_status()
        data = response.json()

        if not data or not isinstance(data, list):
            return None

        pais = data[0]

        capital = pais.get("capital", ["Desconocida"])[0]
        region = pais.get("region", "Desconocida")
        poblacion = pais.get("population", "Desconocida")

        # Coordenadas de la capital
        latlng = pais.get("capitalInfo", {}).get("latlng", None)
        if latlng and len(latlng) == 2:
            lat, lon = latlng
        else:
            lat, lon = None, None

        return {
            "pais": pais.get("name", {}).get("common", nombre_pais),
            "capital": capital,
            "region": region,
            "poblacion": poblacion,
            "lat": lat,
            "lon": lon
        }

    except requests.RequestException as e:
        print(f"Error al consultar la API: {e}")
        return None
