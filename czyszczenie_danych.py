import os
import pandas as pd

def wyczysc_dane_produkcyjne(sciezka_wejsciowa, sciezka_wyjsciowa):
    # 1. Sprawdzenie, czy plik źródłowy istnieje
    if not os.path.exists(sciezka_wejsciowa):
        print(f"Błąd: Plik '{sciezka_wejsciowa}' nie istnieje! Wygeneruj go najpierw.")
        return

    # 2. Wczytanie surowych danych
    df = pd.read_csv(sciezka_wejsciowa)
    print(f"--- ROZPOCZĘCIE PROCESU CZYSZCZENIA DANYCH ---")
    print(f"Liczba rekordów w surowym pliku: {len(df)}")

    # 3. Eliminacja identycznych duplikatów wierszy
    df_cleaned = df.drop_duplicates()
    print(f"Liczba rekordów po usunięciu duplikatów: {len(df_cleaned)}")

    # 4. Usunięcie wierszy bez identyfikatora pracownika
    df_cleaned = df_cleaned.dropna(subset=["id_pracownika"])

    # 5. Korekta błędów ludzkich (wartości ujemne zmieniamy na ich wartość bezwzględną)
    if "wyprodukowane_sztuki" in df_cleaned.columns:
        df_cleaned["wyprodukowane_sztuki"] = df_cleaned["wyprodukowane_sztuki"].abs()

    # 6. Imputacja brakujących danych (NaN)
    # Dla wyprodukowanych sztuk wstawiamy medianę (odporną na skrajne anomalie)
    if "wyprodukowane_sztuki" in df_cleaned.columns:
        mediana_sztuk = df_cleaned["wyprodukowane_sztuki"].median()
        df_cleaned["wyprodukowane_sztuki"] = df_cleaned["wyprodukowane_sztuki"].fillna(mediana_sztuk)

    # Dla czasu przerw wstawiamy średnią arytmetyczną
    if "czas_przerw_min" in df_cleaned.columns:
        srednia_przerw = df_cleaned["czas_przerw_min"].mean()
        df_cleaned["czas_przerw_min"] = df_cleaned["czas_przerw_min"].fillna(srednia_przerw)

    print(f"Proces czyszczenia zakończony. Liczba końcowych wierszy: {len(df_cleaned)}")

    # 7. Wyznaczenie i wyświetlenie statystyki opisowej (efektywność)
    print("\n--- GENEROWANIE STATYSTYKI OPISOWEJ DLA KIEROWNICTWA ---")
    statystyki = df_cleaned["wyprodukowane_sztuki"].describe()
    print(statystyki)

    # 8. Zapisanie oczyszczonego zbioru do nowego pliku CSV
    df_cleaned.to_csv(sciezka_wyjsciowa, index=False)
    print(f"\nOczyszczone dane zostały pomyślnie zapisane do pliku: '{sciezka_wyjsciowa}'")

if __name__ == "__main__":
    # Uruchomienie funkcji czyszczącej
    wyczysc_dane_produkcyjne("surowe_dane_produkcja.csv", "oczyszczone_dane_produkcja.csv")