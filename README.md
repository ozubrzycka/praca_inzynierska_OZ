# Wykorzystane programy
Repozytorium zawiera programy w języku Python do analizy danych GNSS i wyznaczania wskaźników ROT/ROTI, z wizualizacją czasową i mapową. Wszystkie materiały udostępnione na licencji CC BY 4.0.

---

## Zawartość repozytorium 

### 1. **mapy.py**
Skrypt konwertuje współrzędne **ECEF (XYZ)** na współrzędne geodezyjne **(szerokość, długość, wysokość)** oraz rysuje mapy rozmieszczenia stacji GNSS dla wybranych obszarów Europy (Polsce, Europie i Szwecji).

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

### 3. **wykresy_sigmaENU.py** oraz **wykresyENU_pol_284_6.py**
Skrypt przedstawiają analizę odchyleń współrzędnych topocentrycznych **ENU (East, North, Up)** względem pozycji referencyjnej stacji bazowych GNSS wraz z generowaniem wykresów czasowych. Wyniki przedstawiono w formie wykresó czasowych obejmujących trzy kolejne dni obserwacyjne, z zachowaniem podziału na granice dobowe.

### Zakres analizy
Skrypty zostały wykorzystane do analizy stacji:
- 'wykresy_sigmaENU.py' - stacje Europy południowej: CEBR00ESP, VILL00ESP, TOR100ESP, stacje Europy północnej: HOA000SWE, TJU00SWE, ONSA00SWE w dwóch okresach obserwacyjnych: **DOY 131-133** i **DOY 284-286** oraz w pierwszym okresie obserwacyjnym **DOY 131-133** dla stacji Europy centralnej: BOGO00POL, JOZ200POL, MIMA00POL,
- 'wykresyENU_pol_284_6.py' - drugi okres obserwacyjny **DOY 284-286** dla stacji Europy centralnej: BOGO00POL, JOZ200POL, MIMA00POL, ze względu na brak danych obserwacyjnych w godzinach 13:29:30 - 19:00:00 w dniu o DOY 285.

### Dane wejściowe
- pliki CSV ze współrzednymi, wygenerowane na podstawie skryptu 'xyz2enyu.py'.

### Metodyka:
1. Obliczono różnice pomiędzy składowymi ENU a ich wartościami referencyjnymi.
2. Połączono dane z trzech kolejnych dni w jeden ciąg czasowy.
3. Oś czasu wyznaczono w godzinach (oznaczonych co trzecia), z zachowaniem ciągłości pomiędzy kolejnymi dobami.
4. Wyniki zwizualizowano w formie 3 wykresów, dla każdej skłądowej, a stacje rozróżniono kolorami zgodnie z legendą.

### Uwagi:
Ze względu na powtarzalność procedury, w przypadku skryptu 'wykresy_sigmaENU.py' zaprezentowano jeden przykłąd dotyczący stacji Europy północnej w okresie **DOY 131-133**, ponieważ analogiczą procedurę wykonano dla pozostałych stacji i okresów. Dla stacji Europy centralnej w okresie **DOY 284-286** (skrypt 'fixed_float_pol_284_6.py'), zaprezentowano konkretny przykład, ponieważ wyróżniał się on "luką" w danych. 

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

### 6. **wykresyRMS_131_3.py** oraz **wykresyRMS_284_6.py**
Skrypty służą do graficznej prezentacji błędów RMS pozycji GNSS w postaci wykresów słupkowych:
- **RMS_H** – błąd pozycji poziomej,
- **RMS_V** – błąd pozycji wysokościowej.

Dla każdej stacji GNSS przedstawiono wartości RMS wyznaczone oddzielnie dla trzech kolejnych dni obserwacyjnych.

### Dane wejściowe
- wartości **RMS_H** oraz **RMS_V** obliczone na podstawie skryptu 'RMS_h_v.py',
- dane zestawione w postaci macierzy.

### Zakres analizy
- okres obserwacyjny:
  - **DOY 131–133** - skrypt 'wykresyRMS_131_3.py',
  - **DOY 284–286** - skrypt 'wykresyRMS_284_6.py',
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

---

### 7. **wykresy_ROT_ROTI.py** i **wykresy_rot_roti_NODW_284_6.py***
Skrypty służą do wyznaczania wskaźników:
- **ROT (Rate of TEC)**,
- **ROTI (Rate Of TEC Index)**,
na podstawie danych TEC pozyskanych z plików obserwacyjnych GNSS.

### Dane wejściowe
- pliki '.Cmn' wygenerowane w aplikacji **GPS-TEC analysis program (ver. 3.5)**.

### Metodyka obliczeń
1. Z plików '.Cmn' wczytywane są wartości **VTEC** dla kolejnych epok pomiarowych.
2. Wskaźnik **ROT** obliczany jest jako różnica kolejnych wartości VTEC przy kroku czasowym 30 s.
3. Wskaźnik **ROTI** obliczany jest jako odchylenie standardowe wartości ROT oknie 5-minutowym (10 epok).
4. Dane z trzech kolejnych dni obserwacyjnych są łączone w jeden ciąg czasowy oraz jest generowany wykres.

### Zakres analizy - okresy czasowe i stacje referencyjne
Skrypt 'wykresy_ROT_ROTI.py'
  - **DOY 131–133**: **MADR00ESP**, **NODW00POL**, **SPT700SWE**,
  - **DOY 284–286**: **MADR00ESP**, **SPT700SWE**

Skrypt 'wykresy_rot_roti_NODW_284_6.py'
- **DOY 284-286**: NODW00POL - skrypt generuje wykres z pominięciem obszaru na wykresie, ze względu na 'lukę' w danych obserwacyjnych pomiędzy 13:29:30 a 19:00:00.

### Wizualizacja wyników
Wykresy punktowe przedstawiają przebieg **ROT** oraz przebieg **ROTI**:
- pionowe linie przerywane wyznaczają granice kolejnych dni obserwacyjnych,
- osie czasu przedstawione są w godzinach (0–72 h).

### Uwagi
- Zaprezentowany skrypt stanowi przykład realizacji procedury
  dla stacji **SPT700SWE** w okresie **DOY 131–133** oraz dla stacji **NODW00POL** w okresie **DOY 284-286**. 
- **Analogiczna procedura obliczeniowa i wizualizacyjna została wykonana**
  dla pozostałych stacji referencyjnych (**MADR00ESP**, **NODW00POL**)
  oraz dla drugiego okresu obserwacyjnego (**DOY 284–286**).

W repozytorium zaprezentowano dwa przykłady, ponieważ, metodyka obliczeń ROT i ROTI była identyczna we wszystkich analizowanych przypadkach.

---
### 8. **fixed_float.py** oraz **fixed_float_pol_284_6.py**
Skrypty przedstawiają analizę odchyleń współrzędnych topocentrycznych **ENU (East, North, Up)** względem pozycji referencyjnej stacji bazowych GNSS oraz ich wizualizację w postaci wykresów czasowych z rozróżnieniem rozwiązań typu **FIXED** i **FLOAT**. Wyniki przedstawiono w formie wykresó czasowych z trzech dni, z zachowaniem podziąłu na granice czasowe dni. 

### Zakres analizy
Skrypty zostały wykorzystane do analizy stacji:
- 'fixed_float.py' - stacje Europy południowej: CEBR00ESP, VILL00ESP, TOR100ESP, stacje Europy północnej: HOA000SWE, TJU00SWE, ONSA00SWE w dwóch okresach obserwacyjnych: **DOY 131-133** i **DOY 284-286** oraz w pierwszym okresie obserwacyjnym **DOY 131-133** dla stacji Europy centralnej: BOGO00POL, JOZ200POL, MIMA00POL,
- 'fixed_float_pol_284_6.py' - drugi okres obserwacyjny **DOY 284-286** dla stacji Europy centralnej: BOGO00POL, JOZ200POL, MIMA00POL, ze względu na brak danych obserwacyjnych w godzinach 13:29:30 - 19:00:00 w dniu o DOY 285.

### Dane wejściowe
- pliki CSV ze współrzędnymi ENU wygenerowane na podstawie kodu 'xyz2enu.py',
- pliki CSV zawierające informację o typie rozwiązania FIXED/FLOAT z programu **Trimble Busieness Center**.

### Metodyka obliczeń 
1. Dla każdej stacji obliczono różnice pomiędzy skłądowymi ENU, a ich wartościami referencyjnymi.
2. Dane z trzech kolejnych dni zostały połączone w jeden ciąg czasowy.
3. Punkty na wykresach oznaczono kolorami w zależności od rozwiązania FIXED/FLOAT:
   - kolor zielony: rozwiązanie typu FIXED (różne odcienie dotyczą stacji opidanych w legendzie wykresu),
   - kolor czarny: rozwiązanie FLOAT.

### Uwagi
- W przypadku skryptu 'fixed_float.py' zaprezentowano jeden przykłąd dotyczący stacji Europy północnej w okresie **DOY 131-133**, ponieważ analogiczą procedurę wykonano dla pozostałych stacji i okresów, oprócz stacji Europy centralnej w okresie **DOY 284-286** (skrypt 'fixed_float_pol_284_6.py').

---
