import json
import requests
import pandas as pd
import folium

# Funkcja do zapisywania stacji pomiarowych dla danego miasta
def save_stations_for_city(city_id, stations):
    city_stations = [station for station in stations if station['city']['id'] == city_id]
    return city_stations
    
def generate_map():
# URL do API GIOŚ dla stacji pomiarowych
    url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'

# Wysłanie zapytania GET do API
    response = requests.get(url)

# Sprawdzenie, czy zapytanie zakończyło się sukcesem
    if response.status_code == 200:
        lista_stacji_pomiarowych = response.json()
    else:
        print(f"Błąd podczas pobierania danych: {response.status_code}")
        lista_stacji_pomiarowych = []

    # Pobranie listy wszystkich stacji pomiarowych dla województwa dolnośląskiego
    dolnoslaskie_stations = [station for station in lista_stacji_pomiarowych if station['city']['commune']['provinceName'] == 'DOLNOŚLĄSKIE']

    # Zapis stacji pomiarowych dla całego województwa dolnośląskiego
    for station in dolnoslaskie_stations:
        city_id = station['city']['id']
        city_name = station['city']['name']
        stations_for_city = save_stations_for_city(city_id, lista_stacji_pomiarowych)
        with open(f'stacje_miasta_{city_name}.json', 'w', encoding='utf-8') as f:
            json.dump(stations_for_city, f, ensure_ascii=False, indent=4)

        print(f"Zapisano stacje pomiarowe dla miasta {city_name}.")

    # Przekształcenie listy stacji do DataFrame
    df_dolnoslaskie = pd.DataFrame(dolnoslaskie_stations)
    df_dolnoslaskie['gegrLat'] = df_dolnoslaskie['gegrLat'].astype(float)
    df_dolnoslaskie['gegrLon'] = df_dolnoslaskie['gegrLon'].astype(float)

    # Tworzenie mapy z folium dla województwa dolnośląskiego
    mapa_dolnoslaskie = folium.Map(location=[51.1079, 17.0385], zoom_start=8)  # Środkowa lokalizacja Dolnego Śląska

    # Dodawanie markerów do mapy
    for index, row in df_dolnoslaskie.iterrows():
        folium.Marker(
            location=[row['gegrLat'], row['gegrLon']],
            popup=f"{row['stationName']}, {row['city']['name']}",
            tooltip=row['stationName']
        ).add_to(mapa_dolnoslaskie)

    # Zapis mapy do pliku HTML
    mapa_dolnoslaskie.save('mapa_stacji_pomiarowych_dolnoslaskie.html')

    print("Mapa Dolnego Śląska została zapisana do pliku 'mapa_stacji_pomiarowych_dolnoslaskie.html'.")
#generate_map()