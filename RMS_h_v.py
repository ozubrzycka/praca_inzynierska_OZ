import pandas as pd
import numpy as np

# --- wartości referencyjne ---
E_ref = {"HOA": -11717.483475578178, "TJU": -46126.442650128265, "ONSA": -58076.34517919862}
N_ref = {"HOA": 28170.439823906483, "TJU": 28082.640680199976, "ONSA": -35180.94558484411}
U_ref = {"HOA": -95.15530320150538, "TJU": -391.8129662269639, "ONSA": -536.3832816155409}

# --- stacje i dni ---
stations_info = {
    "HOA": {"file_prefix": "ENU_SPT_HOA", "trim": 1},
    "TJU": {"file_prefix": "ENU_SPT_TJU", "trim": 1},
    "ONSA": {"file_prefix": "ENU_SPT_ONSA", "trim": 1},
}

days = [131, 132, 133]


RMS_results = {station: {"RMS_E": [], "RMS_N": [], "RMS_U": [], "RMS_H": [], "RMS_V": []} 
               for station in stations_info.keys()}


for doy in days:
    for station, info in stations_info.items():
        # wczytanie danych
        df = pd.read_csv(f"{info['file_prefix']}_{doy}.csv", header=None, names=["E","N","U"])
        
        # przycięcie końcowych punktów
        if info["trim"] > 0:
            df = df.iloc[:-info["trim"]]
        
        # odchylenia od pozycji referencyjnej
        diff_E = df["E"] - E_ref[station]
        diff_N = df["N"] - N_ref[station]
        diff_U = df["U"] - U_ref[station]
        
        
        # RMS względem referencji
        rms_E = np.sqrt(np.mean(diff_E**2))
        rms_N = np.sqrt(np.mean(diff_N**2))
        rms_U = np.sqrt(np.mean(diff_U**2))
        
        # RMS poziome i pionowe
        rms_H = np.sqrt(rms_E**2 + rms_N**2)
        rms_V = rms_U
        
        # zapis wyników
        RMS_results[station]["RMS_E"].append(rms_E)
        RMS_results[station]["RMS_N"].append(rms_N)
        RMS_results[station]["RMS_U"].append(rms_U)
        RMS_results[station]["RMS_H"].append(rms_H)
        RMS_results[station]["RMS_V"].append(rms_V)

# Wyniki:
print("RMS dla wszystkich stacji i dni:")
for station, values in RMS_results.items():
    print(f"\nStacja {station}:")
    for i, doy in enumerate(days):
        print(f" DOY {doy} -> RMS_H: {values['RMS_H'][i]:.4f} m, RMS_V: {values['RMS_V'][i]:.4f} m")
