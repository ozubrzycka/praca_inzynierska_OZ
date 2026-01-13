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

### 4. **wykresy_EN.py**
Skrypt realizuje analizę rozrzutu odchyleń współrzędnych topocentrycznych **E (East)** i **N (North)** względem wartości referencyjnej dla stacji GNSS.
Odchylenia współrzędnych zostały wyznczone w lokalnym układzie ENU względem stacji referencyjnej, a następnie przedstawione w postaci wykresów punktowych **E-N**.

### Zakres analizy do wykresu:
- analizowane skłądowe: **E oraz N**,
- okresy obserwacyjne:
  - **DOY 131–133**,
  - **DOY 284–286**,  
- krok czasowy danych: **30 sekund**,  
- dane wejściowe: pliki CSV zawierające współrzędne ENU.

  ### Metodyka:
- dla każdej stacji obliczono różnice składowych E i N względem ich wartości referencyjnych,
- dla każdego dnia oraz każdej stacji wygenerowano wykres rozrzutu **σE–σN** (razem 18 wykresów),
- wszystkie wykresy przedstawiono z identycznym zakresem osi, co umożliwia bezpośrednie porównanie rozwiązań GNSS.

### Uwagi
- Identyczną procedurę obliczeniową zastosowano dla **wszystkich analizowanych zestawów stacji GNSS**:
  1. **Hiszpania**: CEBR00ESP, VILL00ESP, TOR100ESP,
  2. **Polska**: BOGO00POL, JOZ200POL, MIMA00POL,
  3. **Szwecja**: HOA000SWE, TJU000SWE, ONSA00SWE.

Ze względu na powtarzalnosć procedury, w repozytorium przedstawiono wybrane przykłądy wykresów.

---

### 5. **RMS_h_v.py**
Skrypt służy do obliczania błędów RMS – Root Mean Square składowych **E (East)**, **N (North)** oraz **U (Up)** współrzędnych topocentrycznych stacji GNSS względem ich pozycji referencyjnych.

### Zakres analizy
- analizowane składowe: **E, N, U**,
- wyznaczane wskaźniki:
  - **RMS_H** – błąd poziomy,
  - **RMS_V** – błąd pionowy,
- okresy obserwacyjne:
  - **DOY 131-133**,
  - **DOY 284–286**,
- dane wejściowe: pliki CSV zawierające współrzędne ENU w interwale 30 s.

### Metodyka obliczeń
Dla każdej stacji i każdego dnia:
1. Wczytano współrzędne topocentryczne E, N, U.
2. Obliczono odchylenia względem wartości referencyjnych.
3. Wyznaczono błędy RMS składowych E, N oraz U.
4. Obliczono błędy RMS poziomy (**RMS_H**) i pionowy (**RMS_V**).

### Uwagi
- Identyczną procedurę obliczeniową zastosowano dla **obu analizowanych okresów pomiarowych (DOY 131–133 oraz DOY 284–286)**.
- Metodykę wykorzystano analogicznie dla **wszystkich zestawów stacji GNSS**:
  1. **Hiszpania**: CEBR00ESP, VILL00ESP, TOR100ESP,
  2. **Polska**: BOGO00POL, JOZ200POL, MIMA00POL,
  3. **Szwecja**: HOA000SWE, TJU000SWE, ONSA00SWE.

Ze względu na powtarzalność obliczeń w repozytorium przedstawiono przykładowy skrypt dla jednego zestawu stacji w jednym analizowanym okresie.

---

### 6. **wykresy_RMS.py**
Skrypt służy do graficznej prezentacji błędów RMS pozycji GNSS w postaci wykresów słupkowych:
- **RMS_H** – błąd pozycji poziomej,
- **RMS_V** – błąd pozycji wysokościowej.

Dla każdej stacji GNSS przedstawiono wartości RMS wyznaczone oddzielnie dla trzech kolejnych dni obserwacyjnych.

### Dane wejściowe
- wartości **RMS_H** oraz **RMS_V** obliczone na podstawie skryptu 'RMS_h_v.py',
- dane zestawione w postaci macierzy.

### Zakres analizy
- okres obserwacyjny:
  - **DOY 131–133**,
  - **DOY 284–286**,
- analizowane stacje GNSS:
  - **CEBR00ESP, VILL00ESP, TOR100ESP**,
  - **BOGO00POL, JOZ200POL, MIMA00POL**,
  - **HOA000SWE, TJU000SWE, ONSA00SWE**.

### Opis wykresów
- wykresy słupkowe przedstawiają wartości RMS dla poszczególnych dni,
- kolory słupków odpowiadają kolejnym dniom obserwacyjnym,
- osobno zaprezentowano:
  - błędy pozycji poziomej (**RMS_H**),
  - błędy pozycji pionowej (**RMS_V**).

### Uwagi
- Identyczną procedurę wizualizacji zastosowano **analogicznie dla drugiego okresu obserwacyjnego (DOY 284–286)**.

Ze względu na powtarzalność metodyki w repozytorium zaprezentowano przykładową realizację dla jednego okresu obserwacji.
