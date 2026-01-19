import pandas as pd

days_info = [131, 132, 133]
stations = ["HOA", "TJU", "ONSA"]

results = {}

for doy in days_info:
    results[doy] = {}

    # suma dla wszystkich stacji tego dnia
    total_fixed_day = 0
    total_float_day = 0

    for st in stations:
        df_status = pd.read_csv(f"SPT_{st}_{doy}.csv")
        status = df_status["GNSS Vector Observation.Solution Type"]

        fixed = (status == "Fixed").sum()
        float_ = (status != "Fixed").sum()
        total = fixed + float_

        total_fixed_day += fixed
        total_float_day += float_

        results[doy][st] = {
            "Fixed": fixed,
            "Float": float_,
            "Fixed (%)": fixed / total * 100,
            "Float (%)": float_ / total * 100
        }

   
    total_all_day = total_fixed_day + total_float_day
    results[doy]["ALL"] = {
        "Fixed": total_fixed_day,
        "Float": total_float_day,
        "Fixed (%)": total_fixed_day / total_all_day * 100,
        "Float (%)": total_float_day / total_all_day * 100
    }

# Wyniki: 
for doy, data in results.items():
    print(f"\nDOY {doy}")
    for st, res in data.items():
        print(f"  {st}: Fixed {res['Fixed (%)']:.2f}% , Float {res['Float (%)']:.2f}%")
