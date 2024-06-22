import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Funkcja do wczytywania i przetwarzania danych
def read_json_file(json_file, year, pollution):
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
                if statystyka['Rok'] == year:
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

            print(f"Średnia dla roku {year} dla {pollution}: {srednia_dla_roku}")
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

# Funkcja do rysowania wykresu z linią trendu
def plot_data(list_of_years, list_of_aver, pollution, start_year, color):
    df = pd.DataFrame({'Rok': list_of_years, 'Średnia wartość': list_of_aver})
    
    if not df.empty and df['Średnia wartość'].notna().any():
        # Interpolacja danych liniową metodą
        df_interpolated = df.interpolate(method='linear', limit_direction='both')

        plt.figure(figsize=(10, 6))
        bars = plt.bar(df_interpolated['Rok'], df_interpolated['Średnia wartość'], color=color)
        plt.title(f"Średnia wartość zanieczyszczenia {pollution}\n dla Województwa Dolnośląskiego w latach {start_year} - {df['Rok'].max()}", fontsize=14)
        plt.xlabel('Rok')
        plt.ylabel('Średnia [µg/m3]', fontsize=12)
        plt.xticks(df_interpolated['Rok'])
        plt.grid(True)
        
        # Dodanie linii trendu
        z = np.polyfit(df_interpolated['Rok'], df_interpolated['Średnia wartość'], 1)
        p = np.poly1d(z)
        plt.plot(df_interpolated['Rok'], p(df_interpolated['Rok']), "r--", linewidth=2)

        # Dodanie wartości nad słupkami
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval:.2f}', ha='center', va='bottom', fontsize=10)

        plt.tight_layout()
        plt.savefig(f"Zmiana wartości {pollution} w powietrzu.pdf")
        plt.show()
    else:
        print("Brak danych do wygenerowania wykresu.")

# Wczytanie danych dla podanego roku i zanieczyszczenia
def user_analysis():
    while True:
        try:
            global year, year_max
            year = input("Wprowadź rok, od którego chcesz rozpocząć analizę zanieczyszczenia w województwie lub wprowadż x aby przerwać: ")
            if year=='x' or year=='X':break
            year = int(year)
            year_max = input("Do którego roku mają się wyświetlać statystyki?")
            year_max=int(year_max)
            pollution = input("Wybierz zanieczyszczenie do analizy lub x aby przerwać: 'NO2', 'PM10', 'PM25', 'O3', 'SO2', 'CO': ")
            color = input("Podaj kolor dla wykresu :green,blue,yellow etc.")
            json_file = f'D:\\Workspace\\statistics_{pollution}_DOLNYSLASK.json'
            list_of_years = []
            list_of_aver = []
            if pollution=='x' or pollution=='X':break
            if color =='b' or color=='B':color=='light green'
            if year_max=='x':break
            if year == 'x':break

        except:"Podano nie prawidłową wartość"

        # Iteracja przez kolejne lata do wybranego roku
        for yr in range(year, year_max+1):
            years, averages = read_json_file(json_file, yr, pollution)
            list_of_years.extend(years)
            list_of_aver.extend(averages)

        plot_data(list_of_years, list_of_aver, pollution, year, color)
        break

#user_analysis()
