import json
import pandas as pd
import requests
import matplotlib.pyplot as plt
import csv


#Badam jakie nazwy stref są zawarte w danych, aby przedstawić osobne statystyki dla poszczególnych stref
with open('statistics_PM10_DOLNYSLASK.json', mode='r', encoding='utf-8') as file:
            data = json.load(file)
            list_of_zone=[]
            statistics_list = data.get('Lista statystyk', [])
            for statistic in statistics_list:
                 list_of_zone.append(statistic['Nazwa strefy'])
# tutaj usuwam duplikaty z listy stref
            print(list(set(list_of_zone)))
#list_of_zone:['miasto Legnica', 'strefa dolnośląska', 'miasto Wałbrzych', 'strefa dolnośląska_2', 'Aglomeracja Wrocławska']


# Funkcja do wczytywania i przetwarzania danych
def zones_pollution(json_file, year, pollution,zone_name):
    list_of_years = []
    list_of_aver = []

    try:
        with open(json_file, mode='r', encoding='utf-8') as file:
            data = json.load(file)
            print("Dane JSON wczytane poprawnie")

        if 'Lista statystyk' in data:
            statistics_list = data['Lista statystyk']
            suma_srednich = 0
            liczba_pomiarow = 0

            # Iteracja przez listę statystyk
            for statystyka in statistics_list:
                if statystyka['Rok'] == year and statystyka['Nazwa strefy']== zone_name:
                    # Sprawdzanie obecności kluczy i przeliczanie jednostek
                    if 'Średnia [mg/m3]' in statystyka:
                        srednia = statystyka['Średnia [mg/m3]'] * 1000  # Przeliczanie na µg/m³
                    elif 'Średnia [µg/m3]' in statystyka:
                        srednia = statystyka['Średnia [µg/m3]']
                    else:
                        print(f"Brak klucza 'Średnia [mg/m3]' ani 'Średnia [µg/m3]' w danych dla roku {year}.")
                        continue

                    suma_srednich += srednia
                    liczba_pomiarow += 1

            if liczba_pomiarow > 0:
                srednia_dla_roku = suma_srednich / liczba_pomiarow
            else:
                srednia_dla_roku = None

            print(f"Średnia dla roku {year} dla {pollution} dla Województwa Dolnośląskiego: {srednia_dla_roku}")
            list_of_years.append(year)
            list_of_aver.append(srednia_dla_roku)
        else:
            print("Klucz 'Lista statystyk' nie istnieje w danych.")
    
    except json.JSONDecodeError as e:
        print(f"Błąd dekodowania JSON: {e}")
    except FileNotFoundError:
        print(f"Plik {json_file} nie został znaleziony.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

    return list_of_years, list_of_aver

# Funkcja do rysowania wykresu
import pandas as pd
import matplotlib.pyplot as plt

def plot_data(list_of_years, list_of_aver, pollution, start_year, color,year_max,zone_name):
    df = pd.DataFrame({'Rok': list_of_years, 'Średnia wartość': list_of_aver})

    if not df.empty and df['Średnia wartość'].notna().any():
        plt.figure(figsize=(10, 6))
        plt.bar(df['Rok'], df['Średnia wartość'], color=color)
        plt.title(f"Średnia wartość zanieczyszczenia {pollution}\n dla strefy {zone_name} w latach {start_year} - {year_max}", fontsize=14)
        plt.xlabel('Rok')
        plt.ylabel('Średnia [µg/m³]', fontsize=12)
        plt.xticks(df['Rok'])
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        
        # Dodanie wartości do etykiet na osi y
        for i, value in enumerate(df['Średnia wartość']):
            plt.text(df['Rok'][i], value + 0.5, f'{value:.2f}', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(f"Zmiana wartości {pollution} w powietrzu w strefie {zone_name}.pdf")
        plt.show()

    else:
        print("Brak danych do wygenerowania wykresu.")

# Wczytanie danych dla podanego roku i zanieczyszczenia
def user_analysis_city():
    while True:
        try:
            global pollution,year,zone_name,color,year_max
            year = input("Wprowadź rok, od którego chcesz rozpocząć analizę(od 2010roku) zanieczyszczenia w Strefie: lub naciśnij x aby wyjść")
            if year =='x':break
            year = int(year)
            year_max=input("Do którego roku mają wyświetlić się satystyki?")
            year_max=int(year_max)
            zone_name=input("Wprowadz nazwę strefy [['Aglomeracja Wrocławska','miasto Legnica', 'miasto Wałbrzych']]") 
            pollution = input("Wybierz zanieczyszczenie do analizy: 'NO2', 'PM10', 'PM25', 'O3', 'SO2', 'CO': ")
            color = input("Podaj kolor dla wykresu :green,blue,yellow etc. jak nie chcesz dokonywać wyboru naciśnij 'b', jak chcesz przerwać: 'x'")
            if color=='b'or color=='B':
                color ='lightblue'
            if zone_name=='x'or'X':break
            if pollution=='x'or'X':break
        except:
            print("Zła wartość")
    
        
        

    try:
        json_file = f'D:\\Workspace\\statistics_{pollution}_DOLNYSLASK.json'
        list_of_years = []
        list_of_aver = []

        # Iteracja przez kolejne lata do 2024 roku
        for yr in range(year, year_max +1):
            years, averages = zones_pollution(json_file, yr, pollution,zone_name)
            list_of_years.extend(years)
            list_of_aver.extend(averages)
        if [year_max in list_of_years]==False:
            print(f"Nie mamy danych dla roku{year_max}")
            year_max-=1
        
        if [year in list_of_years]==False:
            year+=1




        print("Moje listy:", list_of_years, list_of_aver)
        plot_data(list_of_years, list_of_aver, pollution, year,color,year_max,zone_name)
    except: 
        print("Nie wybrano odpowiedniej wartości")
#user_analysis_city()
