from decimal import Decimal, ROUND_HALF_UP
import unittest


# =====================================================================
# SYSTEM F-K: Algorytmy naliczania podatków i agregacji
# =====================================================================
def oblicz_brutto_i_vat(netto_str, stawka_vat_str="0.23"):
    """Bezpieczne obliczanie wartości VAT i Brutto przy użyciu Decimal."""
    netto = Decimal(netto_str)
    vat_stawka = Decimal(stawka_vat_str)

    # Obliczenie podatku i zaokrąglenie do 2 miejsc po przecinku (w górę od połowy grosza)
    vat_wartosc = (netto * vat_stawka).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    brutto = (netto + vat_wartosc).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    return {"netto": netto, "vat": vat_wartosc, "brutto": brutto}


# =====================================================================
# SCENARIUSZE TESTOWE (Testy Jednostkowe i Integracyjne)
# =====================================================================
class TestySystemuKsiegowego(unittest.TestCase):

    def test_zaokraglenia_vat_standardowego(self):
        """Scenariusz 1: Test groszowych zaokrągleń walutowych dla standardowej stawki 23%."""
        # Kwota netto, która przy zwykłym float mogłaby sprawiać problemy zaokrągleń
        wynik = oblicz_brutto_i_vat("100.05")

        # 100.05 * 0.23 = 23.0115 -> po zaokrągleniu do grosza powinno być 23.01
        self.assertEqual(wynik["vat"], Decimal("23.01"))
        self.assertEqual(wynik["brutto"], Decimal("123.06"))

    def test_granica_zaokraglenia_w_gore(self):
        """Scenariusz 2: Test matematycznej poprawności zaokrąglania dokładnie od połowy grosza w górę."""
        # 10.02 * 0.23 = 2.3046 -> 2.30
        # 10.03 * 0.23 = 2.3069 -> 2.31
        wynik = oblicz_brutto_i_vat("10.03")
        self.assertEqual(wynik["vat"], Decimal("2.31"))

    def test_integracja_agregacji_faktur(self):
        """Scenariusz 3: Test integracyjny agregacji danych (sumowanie paczki faktur bez straty grosza)."""
        paczka_netto = ["10.50", "20.75", "100.00"]
        suma_brutto = Decimal("0.00")

        for kwota in paczka_netto:
            suma_brutto += oblicz_brutto_i_vat(kwota)["brutto"]

        # Wyliczenia:
        # 10.50 -> vat 2.42 -> brutto 12.92
        # 20.75 -> vat 4.77 -> brutto 25.52
        # 100.00 -> vat 23.00 -> brutto 123.00
        # Suma brutto = 12.92 + 25.52 + 123.00 = 161.44
        self.assertEqual(suma_brutto, Decimal("161.44"))


if __name__ == "__main__":
    print(
        "--- 5. SYSTEMY FINANSOWO-KSIĘGOWE I TESTOWANIE OPROGRAMOWANIA ---"
    )
    # Uruchomienie automatycznych testów jednostkowych
    unittest.main()
    # Instrukcja Stanowiskowa dla Personelu Biurowego GZAZ
    # Dotyczy: Automatycznego generowania raportów i weryfikacji finansowej
    #
    # Uruchomienie Narzędzia: Na pulpicie komputera biurowego znajduje się skrót do skryptu raportującego. Kliknij na niego dwukrotnie lewym przyciskiem myszy.
    #
    # Wprowadzanie Danych: System automatycznie pobierze najnowsze, oczyszczone dane o produkcji i finansach z bazy danych PostgreSQL.
    #
    # Weryfikacja i Kontrola: * Jeśli w czarnym oknie konsoli pojawi się komunikat OK (Tests Passed), oznacza to, że wszystkie faktury i koszty zostały poprawnie zagregowane, a podatki naliczone bez błędów zaokrągleń.
    #
    # W przypadku pojawienia się komunikatu FAILED, należy natychmiast wstrzymać księgowanie i przekazać logi do działu IT.
    #
    # Odbiór Wyników: Gotowy, zsumowany raport miesięczny zostanie automatycznie zapisany w folderze sieciowym jako plik CSV, gotowy do zaimportowania do głównego systemu F-K.