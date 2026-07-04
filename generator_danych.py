import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Ustawienie ziarna losowości dla powtarzalności wyników
np.random.seed(42)
liczba_wierszy = 120
data_poczatkowa = datetime(2026, 6, 1)

# Generowanie podstawowych, poprawnych danych bazowych
id_pracowników = [f"PRAC_{np.random.randint(1, 15):02d}" for _ in range(liczba_wierszy)]
daty = [(data_poczatkowa + timedelta(days=int(np.random.randint(0, 30)))).strftime("%Y-%m-%d") for _ in range(liczba_wierszy)]
produkcja = np.random.normal(loc=150, scale=25, size=liczba_wierszy).astype(int)
przerwy = np.random.normal(loc=30, scale=7, size=liczba_wierszy).astype(int)

# Tworzenie tabeli (DataFrame)
df_surowy = pd.DataFrame({
    "id_pracownika": id_pracowników,
    "data_wpisu": daty,
    "wyprodukowane_sztuki": produkcja,
    "czas_przerw_min": przerwy
})

# --- WPROWADZANIE SZTUCZNYCH BŁĘDÓW DO PLIKU ---

# 1. Wstawianie pustych wartości (NaN) w losowych miejscach
for _ in range(7):
    df_surowy.loc[np.random.randint(0, liczba_wierszy), "wyprodukowane_sztuki"] = np.nan
for _ in range(5):
    df_surowy.loc[np.random.randint(0, liczba_wierszy), "czas_przerw_min"] = np.nan

# 2. Dodawanie identycznych duplikatów (wielokrotne kliknięcie zapisu)
duplikaty = df_surowy.sample(n=6, random_state=10)
df_surowy = pd.concat([df_surowy, duplikaty], ignore_index=True)

# 3. Wprowadzenie anomalii (błąd ludzki - wartość ujemna)
df_surowy.loc[12, "wyprodukowane_sztuki"] = -45

# Zapis do pliku CSV na dysku
df_surowy.to_csv("surowe_dane_produkcja.csv", index=False)
print("Pomyślnie utworzono plik 'surowe_dane_produkcja.csv' zawierający dane z błędami.")