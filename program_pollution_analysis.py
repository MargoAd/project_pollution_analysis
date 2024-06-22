import statystyki_roczne as sr
import stacje_dolnyslak_mapa as sdm
import Function_analysis_average_pollution_in_voivodeship as afa
import city_pollution_analysis as cpa
import subprocess

# To skrypt łączący działanie wszystkich modułów projektu
# pierwszym etapem działania programu jest poprawne pobranie danych po API do plików json
sr.get_data('https://api.gios.gov.pl/pjp-api/rest/statistics/getStatisticsForPollutants?indicator=PM2,5&size=500&filter[DOLNYŚLĄSKIE]','statistics_PM25_DOLNYSLASK.json')
sr.get_data('https://api.gios.gov.pl/pjp-api/rest/statistics/getStatisticsForPollutants?indicator=SO2&size=500&filter[DOLNOŚLĄSKIE]','statistics_SO2_DOLNYSLASK.json')
sr.get_data('https://api.gios.gov.pl/pjp-api/rest/statistics/getStatisticsForPollutants?indicator=O3&size=500&filter[DOLNOŚLĄSKIE]','statistics_O3_DOLNYSLASK.json')
sr.get_data('https://api.gios.gov.pl/pjp-api/rest/statistics/getStatisticsForPollutants?indicator=CO&size=500&filter[DOLNOŚLĄSKIE]','statistics_CO_DOLNYSLASK.json')
sr.get_data('https://api.gios.gov.pl/pjp-api/rest/statistics/getStatisticsForPollutants?indicator=PM10&size=500&filter[DOLNOŚLĄSKIE]','statistics_NO2_DOLNYSLASK.json')
sr.get_data('https://api.gios.gov.pl/pjp-api/rest/statistics/getStatisticsForPollutants?indicator=PM10&size=500&filter[DOLNOŚLĄSKIE]','statistics_PM10_DOLNYSLASK.json')
# kolejnym etapem jest generowanie i wyświetlenie mapki stacji pomiarowych na Dolnymśląsku
sdm.generate_map()
subprocess.Popen(["start", "mapa_stacji_pomiarowych_dolnoslaskie.html"], shell=True)

# uruchamianie danych modułów zamykam w pętli while,aby moznabyło w sposób ciągły generowac wykresy
while True:

    # uruchomienie modułu do generowania satytstyk dla Województwa - średnie poziomy zanieczyszczeń w podanych latach ('wybrany rok'-2020)
    afa.user_analysis()
    #uruchomienie modułu budowania statystyk dla danej stefy:

    cpa.user_analysis_city()
    action = input("Czy chcesz dalej generować wizualizajce danych w wykresach?\nWybierz:\nY jeżeli tak\nN jeżeli chcesz zakończyć analizę")
    if action=="Y" or action=='y':continue
    if action=="N" or action=='n':break
    


# w dalszym etapie projektu planuję pobrać większą ilość danych i przechowywać się je w własnej bazie danych.
# Będzie to kontunacja tego projektu dla drugiego przedmiotu
print("Dziękuję za uwagę")




