import os


def wygeneruj_zalozenia_infografiki():
    """Automatyczne generowanie pliku tekstowego z danymi na plakat dla GZAZ."""
    tresc = """==================================================================
WNIOSKI Z MODELOWANIA MATEMATYCZNEGO I STATYSTYCZNEGO - RAZEM BUDUJEMY GZAZ!
==================================================================

1. NIEZAWODNOŚĆ (DBAJMY O NASZE MASZYNY):
   * Średni czas między awariami niszczarek (MTBF) wynosi dokładnie 266.00 GODZIN.
   * Pamiętaj! Prawidłowe smarowanie noży i nieprzeładowywanie podajnika 
     zmniejsza ryzyko przestojów i ułatwia codzienną pracę.

2. EKONOMIA (NASZ WSPÓLNY CEL RENTOWNOŚCI):
   * Koszty stałe utrzymania naszego zakładu to 12 000,00 PLN miesięcznie.
   * Marża na każdym zniszczonym kilogramie dokumentów to 3,00 PLN.
   * PUNKT RENTOWNOŚCI (BEP) = MINIMUM 4000 KG (4 TONY) DOKUMENTÓW MIESIĘCZNIE.
   * Każdy kilogram zutylizowany powyżej tej granicy to czysty zysk, który 
     pozwala na stabilne funkcjonowanie i rozwój naszego zespołu!

==================================================================
Opracowano w ramach praktyk studenckich - Gliwice 2026.
"""
    sciezka_pliku = "zalozenia_infografiki.txt"
    with open(sciezka_pliku, "w", encoding="utf-8") as f:
        f.write(tresc)
    print(
        f"[INFO] Wygenerowano dane do infografiki w pliku: {os.path.abspath(sciezka_pliku)}"
    )


def kalkulator_zespolowy():
    """Interaktywny kalkulator efektywności dla zespołu co najmniej 5 pracowników."""
    print("\n" + "=" * 60)
    print("      ZBIORCZY KALKULATOR EFEKTYWNOŚCI ZESPOŁU GZAZ      ")
    print("=" * 60)

    NORMA_GODZINOWA = 15.0  # 15 kg/h
    pracownicy_dane = []

    # Pętla wymuszająca wprowadzenie danych dla minimum 5 osób
    LICZBA_PRACOWNIKOW = 5

    for i in range(1, LICZBA_PRACOWNIKOW + 1):
        print(f"\n[Pracownik {i}/{LICZBA_PRACOWNIKOW}]")
        imie = input(" Podaj imię i nazwisko: ")

        while True:
            try:
                godziny = float(
                    input(
                        " Wpisz liczbę przepracowanych godzin (np. 7): "
                    )
                )
                if godziny > 0:
                    break
                print("   [BŁĄD] Liczba godzin musi być większa od zera!")
            except ValueError:
                print("   [BŁĄD] Wprowadź poprawną liczbę.")

        while True:
            try:
                kilogramy = float(
                    input(
                        " Wpisz masę zniszczonych dokumentów w kg: "
                    )
                )
                if kilogramy >= 0:
                    break
                print("   [BŁĄD] Masa nie może być ujemna!")
            except ValueError:
                print("   [BŁĄD] Wprowadź poprawną liczbę.")

        # Obliczenia indywidualne
        plan = godziny * NORMA_GODZINOWA
        efektywnosc = (kilogramy / plan) * 100
        status = (
            "Cel osiągnięty" if efektywnosc >= 100.0 else "Do poprawy"
        )

        pracownicy_dane.append(
            {
                "imie": imie,
                "godziny": godziny,
                "kilogramy": kilogramy,
                "efektywnosc": efektywnosc,
                "status": status,
            }
        )

    # =====================================================================
    # RAPORT KOŃCOWY DLA KIEROWNICTWA
    # =====================================================================
    print("\n\n" + "═" * 70)
    print("             ZBIORCZY RAPORT WYDAJNOŚCIOWY ZESPOŁU             ")
    print("═" * 70)
    print(
        f"{'Pracownik':<25} | {'Godziny':<8} | {'Wynik (kg)':<10} | {'Efektywność':<12} | {'Status':<15}"
    )
    print("─" * 70)

    suma_kg = 0.0
    suma_godz = 0.0
    efektywnosci_lista = []

    for p in pracownicy_dane:
        print(
            f"{p['imie']:<25} | {p['godziny']:<8.1f} | {p['kilogramy']:<10.1f} | {p['efektywnosc']:<11.1f}% | {p['status']:<15}"
        )
        suma_kg += p["kilogramy"]
        suma_godz += p["godziny"]
        efektywnosci_lista.append(p["efektywnosc"])

    srednia_efektywnosc = sum(efektywnosci_lista) / len(
        efektywnosci_lista
    )

    print("─" * 70)
    print(f"ŁĄCZNA MASA ZNISZCZONYCH DOKUMENTÓW: {suma_kg:.2f} kg")
    print(f"ŁĄCZNA LICZBA ROBOCZOGODZIN:         {suma_godz:.2f} h")
    print(f"ŚREDNIA EFEKTYWNOŚĆ ZESPOŁU:         {srednia_efektywnosc:.2f}%")
    print("═" * 70)


if __name__ == "__main__":
    print("--- 6. POPULARYZACJA I ZAKOŃCZENIE PRAKTYK ---")
    wygeneruj_zalozenia_infografiki()
    kalkulator_zespolowy()