import pytest
from unittest.mock import MagicMock
from decimal import Decimal

# Funkcja symulująca pobieranie danych z PostgreSQL i agregację finansową
def oblicz_calkowity_przychod_z_bazy(db_connection, id_pracownika):
    """Funkcja, która normalnie łączy się z PostgreSQL, ale przetestujemy ją za pomocą Mocka."""
    cursor = db_connection.cursor()
    # Symulacja zapytania SQL
    cursor.execute(f"SELECT wyprodukowane_sztuki FROM efektywnosc_produkcji WHERE id_pracownika = '{id_pracownika}'")
    rekordy = cursor.fetchall()
    
    # Agregacja finansowa (stawka 3.00 PLN za kg / sztukę)
    suma = Decimal("0.00")
    for r in rekordy:
        suma += Decimal(str(r[0])) * Decimal("3.00")
    return suma

# =====================================================================
# TESTY AUTOMATYCZNE PYTEST Z MOCKOWANIEM I PARAMETRYZACJĄ
# =====================================================================

def test_oblicz_przychod_z_bazy_mocking():
    """Test wykorzystujący Mockowanie do izolacji od bazy PostgreSQL."""
    # Tworzymy sztuczne połączenie i kursor (Mock), aby nie łączyć się z realnym PostgreSQL
    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor.return_value
    
    # Definiujemy, co sztucznie ma zwrócić baza danych (np. 3 wpisy produkcyjne)
    mock_cursor.fetchall.return_value = [(100,), (150,), (50,)]
    
    # Wywołujemy funkcję podając zaimitowane połączenie
    wynik = oblicz_calkowity_przychod_z_bazy(mock_conn, "PRAC_01")
    
    # Asercja: (100 + 150 + 50) * 3.00 = 300 * 3.00 = 900.00
    assert wynik == Decimal("900.00")
    print(f"\\n[MOCK TEST] Pomyślnie zweryfikowano izolację od bazy danych. Wynik: {wynik} PLN")

@pytest.mark.parametrize("dane_wejsciowe, oczekiwany_wynik", [
    ([(10,), (20,)], Decimal("90.00")),   # (10+20)*3 = 90
    ([(0,), (5,)], Decimal("15.00")),     # Skrajne dane: zero
    ([], Decimal("0.00"))                 # Brak rekordów w bazie
])
def test_parametryzacji_skrajnych_danych(dane_wejsciowe, oczekiwany_wynik):
    """Parametryzacja przypadków testowych dla skrajnych danych wejściowych."""
    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.return_value = dane_wejsciowe
    
    wynik = oblicz_calkowity_przychod_z_bazy(mock_conn, "PRAC_TEST")
    assert wynik == oczekiwany_wynik