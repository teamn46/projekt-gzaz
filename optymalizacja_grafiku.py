import numpy as np
from scipy.optimize import linprog


def optymalizacja_harmonogramu():
    print("--- 4. OPTYMALIZACJA ZASOBÓW LUDZKICH (BADANIA OPERACYJNE) ---")

    # Funkcja celu: Koszt godzinowy 4 pracowników w GZAZ
    # Pracownik 0 i 1 (z orzeczeniem - 28 PLN/h), Pracownik 2 i 3 (standard - 32 PLN/h)
    c = [28, 28, 32, 32]

    # Ograniczenia górne (A_ub * x <= b_ub)
    # Rygorystyczne przepisy prawne: max 7h dla orzeczeń, max 8h dla normy
    A_ub = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    b_ub = [7, 7, 8, 8]

    # Ograniczenia dolne (Zapotrzebowanie: suma godzin >= 25)
    # Mnożymy przez -1, bo linprog standardowo obsługuje tylko '<='
    A_ub_dolne = [[-1, -1, -1, -1]]
    b_ub_dolne = [-25]

    # Scalenie wszystkich ograniczeń nierównościowych
    A_calosc = A_ub + A_ub_dolne
    b_calosc = b_ub + b_ub_dolne

    # Definiowanie dopuszczalnych przedziałów (bounds)
    x_bounds = [(0, 7), (0, 7), (0, 8), (0, 8)]

    # =====================================================================
    # KLUCZOWA ZMIANA: IMPLEMENTACJA PROGRAMOWANIA CAŁKOWITOLICZBOWEGO (MILP)
    # =====================================================================
    # Wartość 1 oznacza, że dana zmienna musi być liczbą całkowitą (brak ułamków godzinowych)
    zmienne_calkowite = [1, 1, 1, 1]

    res = linprog(
        c,
        A_ub=A_calosc,
        b_ub=b_calosc,
        bounds=x_bounds,
        integrality=zmienne_calkowite,  # Wymuszenie liczb całkowitych przez solver HIGHS
        method="highs",
    )

    if res.success:
        print("Optymalizacja zakończona sukcesem!")
        print(f"Minimalny dzienny koszt personelu: {res.fun:.2f} PLN")
        print("\nOptymalny podział godzin pracy (Wartości całkowitoliczbowe):")
        for i, godziny in enumerate(res.x):
            stopen = (
                "7h (orzeczenie)" if i in [0, 1] else "8h (standard)"
            )
            # Wyświetlamy jako .0f, bo solver gwarantuje brak ułamków!
            print(f" - Pracownik {i} ({stopen}): {godziny:.0f} godzin")
    else:
        print("Nie udało się znaleźć optymalnego rozwiązania grafiku.")

    print("-" * 70)


if __name__ == "__main__":
    optymalizacja_harmonogramu()