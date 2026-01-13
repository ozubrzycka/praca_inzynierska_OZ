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
- zapis wyników ENU do plików csv.

---

### 3. ** **

