# České Dráhy Ticket Price Scraper

Tento Python skript automaticky sbírá informace o cenách jízdenek, datu, čase a úrovni obsazenosti vlakových spojení od Českých drah z webu [cd.cz/spojeni-a-jizdenka](https://www.cd.cz/spojeni-a-jizdenka/). Výstup je uložen ve formátu CSV.

## Požadavky

- Python 3.8 nebo novější
- Nainstalovaný [Google Chrome](https://www.google.com/chrome/) a [ChromeDriver](https://chromedriver.chromium.org/downloads)
- Nainstalované Python balíčky:
  - `selenium`
  - `validators`

Instalace závislostí:
```bash
pip install selenium validators
```

## Použití

Skript je spuštěn přes příkazovou řádku s následujícími parametry:

```bash
python cd_scraper4.py <from_station> <to_station> <output_file.csv> <number_of_pages>
```

### Parametry:
- `from_station` – Výchozí stanice (např. "Praha hl.n.").
- `to_station` – Cílová stanice (např. "Brno hl.n.").
- `output_file.csv` – Název výstupního souboru ve formátu `.csv` (např. "results.csv").
- `number_of_pages` – Počet stránek výsledků k procházení (každá stránka obsahuje 5 spojení).

### Příklad:
```bash
python cd_scraper4.py "Praha hl.n." "Brno hl.n." results.csv 10
```

## Hlavní funkce

- **Validace vstupních dat**: Kontroluje, zda výstupní soubor končí na `.csv`.
- **Automatizace pomocí Selenium WebDriver**:
  - Přijímání cookies.
  - Vyplnění vstupních polí pro stanice.
  - Posun času, aby výsledky zahrnovaly budoucí spoje.
  - Omezení výsledků pouze na vlaky Českých drah.
- **Scrapování dat**:
  - Datum a čas spoje.
  - Cena jízdenky.
  - Úroveň obsazenosti.
- **Export do CSV**: Ukládá data do uživatelem definovaného souboru.

## Omezení

- Stránka může změnit strukturu nebo XPath prvků, což může způsobit nefunkčnost skriptu.
- Skript předpokládá, že je ChromeDriver kompatibilní s verzí Google Chrome.

## Debugging

V případě problémů:
- Zkontrolujte kompatibilitu verzí ChromeDriver a Google Chrome.
- Ujistěte se, že jsou nainstalované všechny požadované knihovny.
- Použijte příkaz `--help` pro získání nápovědy:

```bash
python cd_scraper4.py --help
```

## Licenční ujednání

Tento projekt je poskytován pod licencí MIT. Více informací v přiloženém souboru `LICENSE`.
