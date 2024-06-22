PROJEKT WYKONAŁA : Małgorzata Adamska 49428
nazwa projektu:
Analiza zmian jakości powietrza na podstawie danych z sensorów środowiskowych na przestrzeni  lat na Dolnym Śląsku. 
Sprawozdanie w formacie pdf.

Uruchomienie poszczególnych modułów odbywa się w skrypcie program_pollution_analysis.py
Może to zabrać chwilę, bo w pierwszym punkcie trwa pobranie danych po API.


po uruchomieniu skryptu, najpierw wykonają się wywołanie funckji ściągającej dane po API i zapisującej je do pliku
.json
następnie:
wykona się funcja z modułu stacje_dolnyslask_mapa.py,
następnie uruchomi się funkcja do generowania wykresów dla wybranego zanieczyszczenia dla Województwa Dolnośląskieg w wybranych latach. Można wprowadzić parametry, bądź 'x' przerwać program. 
Kolejnym elementem jest wywołanie funckji ze skryptu city_pollution_analysis.py. Program poprosi o wporwadzenie danych
do generowania wykresów dla podanych Stref w województwie Dolnośląskim, program zapisuje wykresy w formacie pdf.




