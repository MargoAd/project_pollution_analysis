import json
import requests
import pandas as pd

# URL do API GIOŚ - Stworzyłam funkcje przyjmującą jako argument adres URL z którego pobieram API oraz nazwę pliku do któego zapiszemy dane
def get_data(url,json_file):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Błąd podczas pobierania danych: {response.status_code}")
    with open(json_file, 'w',encoding ='utf-8') as f:
        json.dump(data, f, indent=4,ensure_ascii=False)
        
    print(json.dumps(data, indent=2, ensure_ascii=False))
   

   


    print(f"Dane zostały zapisane do pliku'{json_file}'")
# Zapisuje dane historyczne na temat wybranych zanieczyszczeń powietrza dla dolnegośląska 
"""get_data('https://api.gios.gov.pl/pjp-api/rest/statistics/getStatisticsForPollutants?indicator=NO2&size=500&filter[DOLNYŚLĄSK]','statistics_NO2_DOLNYSLASK.json')

get_data('https://api.gios.gov.pl/pjp-api/rest/statistics/getStatisticsForPollutants?indicator=PM10&size=500&filter[DOLNOŚLĄSKIE]','statistics_PM10_DOLNYSLASK.json')
get_data('https://api.gios.gov.pl/pjp-api/rest/statistics/getStatisticsForPollutants?indicator=PM2,5&size=500&filter[DOLNYŚLĄSKIE]','statistics_PM25_DOLNYSLASK.json')
get_data('https://api.gios.gov.pl/pjp-api/rest/statistics/getStatisticsForPollutants?indicator=SO2&size=500&filter[DOLNOŚLĄSKIE]','statistics_SO2_DOLNYSLASK.json')
get_data('https://api.gios.gov.pl/pjp-api/rest/statistics/getStatisticsForPollutants?indicator=O3&size=500&filter[DOLNOŚLĄSKIE]','statistics_O3_DOLNYSLASK.json')
get_data('https://api.gios.gov.pl/pjp-api/rest/statistics/getStatisticsForPollutants?indicator=CO&size=500&filter[DOLNOŚLĄSKIE]','statistics_CO_DOLNYSLASK.json')
get_data('https://api.gios.gov.pl/pjp-api/rest/statistics/getStatisticsForPollutants?indicator=PM10&size=500&filter[DOLNOŚLĄSKIE]','statistics_NO2_DOLNYSLASK.json')

get_data('https://api.gios.gov.pl/pjp-api/v1/rest/archivalData/getDataForAllStationsByYearAndVoivodeship?year=2020&voivodeship=DOLNOŚLĄSKIE&pollution=PM10','statistics_123tri_DOLNYSLASK.json')

"""