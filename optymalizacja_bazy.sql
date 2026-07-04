-- =====================================================================
-- ETAP 2: RESTRUKTURYZACJA BAZY DANYCH DO TRZECIEJ POSTACI NORMALNEJ (3NF)
-- =====================================================================

-- Czyszczenie starych tabel (kolejność usuwania wynika z zależności kluczy obcych)
DROP TABLE IF EXISTS efektywnosc_produkcji CASCADE;
DROP TABLE IF EXISTS pracownicy_slownik CASCADE;

-- 1. Tabela słownikowa pracowników (eliminacja redundancji danych zgodnie z 3NF)
CREATE TABLE pracownicy_slownik (
    id_pracownika VARCHAR(20) PRIMARY KEY,
    imie_nazwisko VARCHAR(100) NOT NULL,
    stopien_niepelnosprawnosci VARCHAR(50) NOT NULL -- Rygorystyczne ograniczenie prawne (Compliance)
);

-- 2. Tabela operacji produkcyjnych (powiązana kluczem obcym - FOREIGN KEY)
CREATE TABLE efektywnosc_produkcji (
    id_wpisu SERIAL PRIMARY KEY,
    id_pracownika VARCHAR(20) REFERENCES pracownicy_slownik(id_pracownika),
    data_wpisu DATE NOT NULL,
    wyprodukowane_sztuki NUMERIC NOT NULL, -- Format zmiennoprzecinkowy (np. 141.0)
    czas_przerw_min NUMERIC NOT NULL       -- Wartości po imputacji statystycznej
);

-- =====================================================================
-- WTRYSK DANYCH (ZASILENIE SŁOWNIKA I IMPORT CSV Z POWER QUERY / PYTHON)
-- =====================================================================

-- 3. Populacja tabeli słownikowej (Wymóg spójności referencjalnej przed importem faktów)
INSERT INTO pracownicy_slownik (id_pracownika, imie_nazwisko, stopien_niepelnosprawnosci) VALUES
('PRAC_01', 'Jan Kowalski', 'Stopień umiarkowany'),
('PRAC_02', 'Anna Nowak', 'Stopień umiarkowany'),
('PRAC_03', 'Piotr Wiśniewski', 'Brak / Personel standardowy'),
('PRAC_04', 'Maria Wójcik', 'Brak / Personel standardowy'),
('PRAC_05', 'Krzysztof Kamiński', 'Stopień znaczny'),
('PRAC_06', 'Elena Zielińska', 'Stopień umiarkowany'),
('PRAC_07', 'Tomasz Szymański', 'Stopień umiarkowany'),
('PRAC_08', 'Agnieszka Woźniak', 'Stopień znaczny'),
('PRAC_09', 'Marcin Kozłowski', 'Brak / Personel standardowy'),
('PRAC_10', 'Barbara Jankowska', 'Stopień umiarkowany'),
('PRAC_11', 'Michał Wojciechowski', 'Stopień umiarkowany'),
('PRAC_12', 'Katarzyna Kwiatkowska', 'Stopień znaczny'),
('PRAC_13', 'Andrzej Mazur', 'Brak / Personel standardowy'),
('PRAC_14', 'Magdalena Krawczyk', 'Stopień umiarkowany')
ON CONFLICT (id_pracownika) DO NOTHING;

-- 4. Automatyczny import oczyszczonych danych produkcyjnych z pliku CSV
-- (W środowisku lokalnym upewnij się, że ścieżka do pliku w folderze C:\praktyki\ jest poprawna)
COPY efektywnosc_produkcji(id_pracownika, data_wpisu, wyprodukowane_sztuki, czas_przerw_min)
FROM 'C:\praktyki\oczyszczone_dane_produkcja.csv'
DELIMITER ',' 
CSV HEADER;

-- =====================================================================
-- ANALIZA PLANÓW WYKONANIA (EXPLAIN ANALYZE) ORAZ OPTYMALIZACJA WYDAJNOŚCI
-- =====================================================================

-- 5. Test wydajności PRZED optymalizacją (Weryfikacja planu wykonania — Sekwencyjny skan)
-- Służy do analizy kosztów generowania okresowych raportów dla kierownictwa GZAZ
EXPLAIN ANALYZE
SELECT p.id_pracownika,
       p.imie_nazwisko,
       p.stopien_niepelnosprawnosci,
       SUM(e.wyprodukowane_sztuki) AS laczna_produkcja,
       AVG(e.czas_przerw_min) AS sredni_czas_przerw
FROM efektywnosc_produkcji e
JOIN pracownicy_slownik p ON e.id_pracownika = p.id_pracownika
WHERE e.data_wpisu >= '2026-06-01' AND e.data_wpisu <= '2026-06-30'
GROUP BY p.id_pracownika, p.imie_nazwisko, p.stopien_niepelnosprawnosci
ORDER BY laczna_produkcja DESC;

-- 6. Implementacja indeksowania struktur relacyjnych — utworzenie indeksu B-Drzewa (B-Tree)
-- Indeks przyspiesza filtrowanie danych po zakresie dat (częste zapytania o raporty miesięczne)
CREATE INDEX idx_efektywnosc_data ON efektywnosc_produkcji(data_wpisu);

-- 7. Test wydajności PO optymalizacji (Weryfikacja skrócenia czasu za pomocą indeksu)
EXPLAIN ANALYZE
SELECT p.id_pracownika,
       p.imie_nazwisko,
       p.stopien_niepelnosprawnosci,
       SUM(e.wyprodukowane_sztuki) AS laczna_produkcja,
       AVG(e.czas_przerw_min) AS sredni_czas_przerw
FROM efektywnosc_produkcji e
JOIN pracownicy_slownik p ON e.id_pracownika = p.id_pracownika
WHERE e.data_wpisu >= '2026-06-01' AND e.data_wpisu <= '2026-06-30'
GROUP BY p.id_pracownika, p.imie_nazwisko, p.stopien_niepelnosprawnosci
ORDER BY laczna_produkcja DESC;