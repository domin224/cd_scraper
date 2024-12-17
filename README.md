# České Dráhy Ticket Price Scraper

This Python script automatically collects information about ticket prices, dates, times, and occupancy levels for train connections operated by České dráhy from the website [cd.cz/spojeni-a-jizdenka](https://www.cd.cz/spojeni-a-jizdenka/). The output is saved in CSV format.

## Requirements

- Python 3.8 or later
- Installed [Google Chrome](https://www.google.com/chrome/) and [ChromeDriver](https://chromedriver.chromium.org/downloads)
- Dependencies listed in the `requirements.txt` file

Install dependencies using:
```bash
pip install -r requirements.txt
```

## Usage

The script is executed via the command line with the following parameters:

```bash
python cd_scraper4.py <from_station> <to_station> <output_file.csv> <number_of_pages>
```

### Parameters:
- `from_station` – Departure station (e.g., "Praha hl.n.").
- `to_station` – Destination station (e.g., "Brno hl.n.").
- `output_file.csv` – The name of the output file in `.csv` format (e.g., "results.csv").
- `number_of_pages` – The number of pages of results to scrape (each page contains 5 connections).

### Example:
```bash
python cd_scraper4.py "Praha hl.n." "Brno hl.n." results.csv 10
```

## Key Features

- **Input Validation**: Ensures the output file ends with `.csv`.
- **Automation with Selenium WebDriver**:
  - Accepting cookies.
  - Filling in departure and destination stations.
  - Adjusting the time to ensure future connections are included.
  - Filtering results to show only trains operated by České dráhy.
- **Data Scraping**:
  - Train departure dates and times.
  - Ticket prices.
  - Occupancy levels.
- **CSV Export**: Saves the collected data to the user-specified file.

## Limitations

- The website may change its structure or XPath elements, which can break the script.
- The script assumes ChromeDriver is compatible with the installed version of Google Chrome.

## Debugging

In case of issues:
- Check compatibility between ChromeDriver and Google Chrome versions.
- Ensure all required libraries are installed.
- Use the `--help` command for guidance:

```bash
python cd_scraper4.py --help
```
