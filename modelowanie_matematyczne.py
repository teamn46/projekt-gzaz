import numpy as np


def analiza_niezawodnosci_mtbf():
    print("--- 1. ANALIZA NIEZAWODNOŚCI INFRASTRUKTURY (MODELE PROBABILISTYCZNE) ---")

    # Dane testowe: czasy pracy maszyn (np. niszczarek dokumentów) między awariami w godzinach
    czasy_pracy_h = [120, 340, 210, 180, 420, 290, 150, 310, 260, 380]

    # Obliczanie MTBF (Mean Time Between Failures) jako średnia arytmetyczna
    mtbf = np.mean(czasy_pracy_h)

    # W modelach probabilistycznych niezawodności często przyjmuje się rozkład wykładniczy
    # Intensywność awarii (lambda) = 1 / MTBF
    lambd = 1 / mtbf

    # Obliczanie prawdopodobieństwa bezawaryjnej pracy przez np. t = 200 godzin: R(t) = e^(-lambda * t)
    t = 200
    prawdopodobienstwo_R = np.exp(-lambd * t)

    print(f"Liczba zaobserwowanych cykli pracy: {len(czasy_pracy_h)}")
    print(f"Średni czas między awariami (MTBF): {mtbf:.2f} godzin")
    print(f"Intensywność awarii (lambda): {lambd:.5f} awarii na godzinę")
    print(
        f"Prawdopodobieństwo bezawaryjnej pracy przez {t} godzin: {prawdopodobienstwo_R * 100:.2f}%"
    )
    print("-" * 70)


def analiza_punktu_rentownosci_bep():
    print("\n--- 2. ANALIZA KOSZTÓW I PUNKTU RENTOWNOŚCI (MODELE LINIOWE) ---")

    # Założenia ekonomiczne dla wybranej usługi GZAZ (np. niszczenie 1 kg dokumentów)
    koszty_stale_miesieczne = 12000  # np. utrzymanie lokalu, stałe pensje (w PLN)
    koszt_zmienny_jednostkowy = 1.50  # np. prąd, worki, utylizacja na 1 kg (w PLN)
    cena_jednostkowa_uslugi = 4.50  # cena dla klienta za 1 kg (w PLN)

    # Wzór na BEP (Break-Even Point) ilościowy: Koszty Stałe / (Cena - Koszt Zmienny)
    marza_skonstruowana = cena_jednostkowa_uslugi - koszt_zmienny_jednostkowy

    if marza_skonstruowana <= 0:
        print(
            "Błąd: Cena jednostkowa musi być wyższa niż koszt zmienny, aby osiągnąć rentowność!"
        )
        return

    bep_ilosciowy = koszty_stale_miesieczne / marza_skonstruowana
    bep_wartosciowy = bep_ilosciowy * cena_jednostkowa_uslugi

    print(f"Koszty stałe zakładu: {koszty_stale_miesieczne:.2f} PLN/miesiąc")
    print(f"Koszt zmienny usługi: {koszt_zmienny_jednostkowy:.2f} PLN/jednostkę")
    print(f"Cena sprzedaży usługi: {cena_jednostkowa_uslugi:.2f} PLN/jednostkę")
    print(f"Marża jednostkowa pokrycia: {marza_skonstruowana:.2f} PLN")
    print(
        f"PUNKT RENTOWNOŚCI (Ilościowy): musisz zrealizować {int(np.ceil(bep_ilosciowy))} jednostek usługi, aby wyjść na zero."
    )
    print(f"PUNKT RENTOWNOŚCI (Wartościowy): Przychód minimalny = {bep_wartosciowy:.2f} PLN")
    print("-" * 70)


if __name__ == "__main__":
    analiza_niezawodnosci_mtbf()
    analiza_punktu_rentownosci_bep()