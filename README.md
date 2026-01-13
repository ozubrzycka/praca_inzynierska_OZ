# praca_inzynierska_OZ
Repozytorium zawiera programy w języku Python do analizy danych GNSS i wyznaczania wskaźników ROT/ROTI, z wizualizacją czasową i mapową. Wszystkie materiały udostępnione na licencji CC BY 4.0.

---

## Zawartość repozytorium 

### 1. **mapy.py**
Skrypt konwertuje współrzędne **ECEF (XYZ)** na współrzędne geodezyjne **(szerokość, długośc, wysokość)** oraz rysuje mapy rozmieszczenia stacji GNSS dla wybranych obszarów Europy (Polsce, Europie i Szwecji).

**Funkcjonalność:***
- Funkcja 'xyz2latlonh(X, Y, Z)' - konwersja XYZ --> lat/lon/h metodą Hirvonena,
- Funkcja 'draw_map(region_name, stations_subset, extent, country_labels, legend_loc)` --> rysowanie map z oznaczonymi stacjami (wizualizacja stacji GNSS na mapach),

Dane przykładowych stacji GNSS są wbudowane w skrypt: Polska, Hiszpania, Szwecja, Europa.

---

### 2. **xyz2enu.py**
Skrypt służy do wyznaczania współrzędnych **topocentrycznych ENU (Earth, North, Up)** na podstawie danych GNSS w układzie ECEF.

Obliczenia w skrypcie są wykonane na przykładzie:
- stacji referencyjnej **NODW00POL**,
- wektora pomiędzy stacją referencyjną **NODW00POL** a **MIMA00POL**,
- danych eksportowanych z programu **Trimble Busieness Center (TBC)** w formacie csv.

**Funkcjonalność:**
- Funkcja 'xyz2latlonh(X, Y, Z)' – konwersja współrzędnych XYZ → geodezyjne lat/lon/h,
- Funkcja 'plh2xyz(lat, lon, h)' – konwersja współrzędnych geodezyjnych lat/lon/h →  wspólrzedne XYZ (ECEF),
- Funkcja 'topocentrENU(X, Y, Z, lat_ref, lon_ref, h_ref)' – transformacja współrzędnych XYZ (ECEF) → na współrzędne topocentryczne ENU względem stacji referencyjnej,
- zapis wyników ENU do plików CSV.

---

### 3. **wykresy_sigmaENU.py **
Skrypt przedstawia analizę odchyleń współrzędnych topocentrycznych **ENU** względem pozycji referencyjnej stacji bazowej wraz z generowaniem wykresu. W przykładzie znajduje się algorytm dla odchyleń **składowej pólnocnej N**, na przykładzie stacji w Szwecji: **HOA000SWE, TJU000SWE, ONSA00SWE**.

### Zakresy analizy do wykresu:
- okres obserwacyjny: 3 dni (w przykładzie DOY: 284, 285, 286),
- interwał czasowy danych: 30 sekund,
- dane wejściowe: pliki CSV ze współrzednymi ENU wygenerowane na podstawie danych GNSS,
- wyniki przedstawiono w formie wykresu jako ciąg czasowy połączony z trzech kolejnych dni.

### Metodyka:
- dla każdej stacji wyznaczono różnice pomiędzy składową N a jej wartością referencyjną,
- dane z trzech dni połaczono w jeden ciąg czasowy,
- wyniki zwizualizowano w funkcji czasu, z zaznaczonym podziałem na poszczególne dni obserwacyjne.

### Uwagi:
- Analogiczne oblicznenia i wizualizacje wykonano dla pozostałych składowych układu ENU (E oraz U).
- Analizę przeprowadzono również dla drugiego okresu pomiarowego: DOY 131, 132, 133.
- Analogiczną procedurę obliczeniową zastoowano dla pozostałych zestawów stacji GNSS:
  1. **Hiszpania**: CEBR00ESP, VILL00ESP, TOR100ESP,
  2. **Polska**: BOGO00POL, JOZ200POL, MIMA00POL,
  3. **Szwecja**: HOA000SWE, TJU000SWE, ONSA00SWE.

Ze względu na powtarzalność procedury obliczeniowej, w repozytorium przedstawiono wybrany przykład. 

---

### 4. ** **
