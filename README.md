# praca_inzynierska_OZ
Repozytorium zawiera programy w języku Python do analizy danych GNSS i wyznaczania wskaźników ROT/ROTI, z wizualizacją czasową i mapową. Wszystkie materiały udostępnione na licencji CC BY 4.0.

---

## Zawartość repozytorium 

1. **mapy.py**
Skrypt konwertuje współrzędne XYZ na geograficzne lat, lon, h (szerokość, długośc, wysokość) i rysuje mapy z oznaczonymi stacjami GNSS wybranych krajach (Polsce, Europie i Szwecji).
- Funkcja 'xyz2latlonh(X, Y, Z)' - konwersja XYZ --> lat/lon/h
- Funkcja 'draw_map(region_name, stations_subset, extent, country_labels, legend_loc)` --> rysowanie map z oznaczonymi stacjami
- Dane przykładowych stacji GNSS są wbudowane w skrypt: Polska, Hiszpania, Szwecja.

