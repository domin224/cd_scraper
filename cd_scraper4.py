import argparse
import validators
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def is_url_valid(url):
    """Check if the provided URL is in a valid format."""
    return validators.url(url)

def get_arguments():
    """Parse and validate command-line arguments for the scraper."""
    parser = argparse.ArgumentParser(description="Ceske drahy ticket price scraper")

    parser.add_argument("from_station_input", type=str, help="Enter your desired from station")
    parser.add_argument("to_station_input", type=str, help="Enter your desired to station")
    parser.add_argument("output_file", type=str, help="Enter the output CSV file name (e.g., results.csv)")
    parser.add_argument("pages", type=int, help="Enter the number of pages to scrape (1 page contains 5 train connections)")

    args = parser.parse_args()

    if not args.output_file.endswith(".csv"):
        raise ValueError("Error: Output file must end with .csv")

    return args

def start_driver():
    """Initialize the Selenium WebDriver and open the target URL."""
    driver = webdriver.Chrome()
    driver.get('https://www.cd.cz/spojeni-a-jizdenka/')
    return driver

def accept_cookies(driver):
    """Handle the cookie consent popup if it appears."""
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'consentBtnall'))).click()
    except Exception:
        print("Warning: Accept cookies button not found.")

def enter_station(driver, args):
    """Fill in the departure and arrival stations in the form."""
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fromto"]/div/div[1]/div/div/input[2]')))
    driver.find_element(By.XPATH, '//*[@id="fromto"]/div/div[1]/div/div/input[2]').send_keys(args.from_station_input)
    driver.find_element(By.XPATH, '//*[@id="fromto"]/div/div[2]/div/div/input[2]').send_keys(args.to_station_input)

def clicking_to_add_day(driver):
    """Advance the date by one day if scraping late at night."""
    if time.localtime().tm_hour >= 22:
        try:
            driver.find_element(By.XPATH, '//*[@id="nextday"]').click()
        except Exception:
            print("Warning: Next day button not found.")

def click_to_add_one_hour(driver):
    """Adjust the time to ensure scraping future connections."""
    try:
        time_button = driver.find_element(By.XPATH, '//*[@id="timepicker-input"]/button[2]')
        for _ in range(2):
            time_button.click()
    except Exception:
        print("Warning: Time adjustment button not found.")

def click_only_cd(driver):
    """Select trains connections operated by České dráhy"""
    driver.find_element(By. XPATH, '//*[@id="main"]/div/div/div[1]/form/div/div[7]/button[2]').click()
    driver.find_element(By. XPATH, '//*[@id="parameters-carrier-label"]').click()
    driver.find_element(By. XPATH, '//*[@id="parameters-carrier"]/ul/li[2]').click()

def click_search_button(driver):
    """Click the search button to begin finding connections."""
    try:
        driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div[1]/form/div/div[7]/button[3]').click()
    except Exception:
        print("Error: Search button not found.")

def extract_content(driver, xpath_code, content_type):
    """Extract specific content (e.g., price, date) from the webpage using XPath."""
    try:
        WebDriverWait(driver, 10).until(lambda d: len(d.find_elements(By.XPATH, xpath_code)) >= 5)
        buttons = driver.find_elements(By.XPATH, xpath_code)
        content = []

        for button in buttons:
            text = button.text
            if content_type == "price":
                match = re.search(r'\d+', text)
                if match:
                    content.append(int(match.group()))
            elif content_type == "date":
                match = re.search(r'\d{1,2}\.\d{1,2}\.\d{4}', text)
                if match:
                    content.append(match.group())
            elif content_type == "time":
                content.append(text)
            elif content_type == "occupancy":
                src_value = button.get_attribute("src")
                occupancy = src_value.split("-")[1].split(".")[0]
                content.append(occupancy)

        return content
    except Exception as e:
        print(f"Warning: Unable to extract {content_type} data. Error: {e}")
        return []

def click_next_button(driver):
    """Click the button to navigate to the next page of results."""
    try:
        next_button = driver.find_element(By.XPATH, '//*[@id="connectionlistanchor"]/div/div/a[3]')
        if next_button.is_displayed():
            next_button.click()
            time.sleep(3)
        else:
            print("Info: Next button is not available.")
    except Exception as e:
        print(f"Error: Failed to click next button. {e}")

def enter_again(driver, last_date, last_time):
    """Reset the search parameters and re-submit the form."""
    url = 'https://www.cd.cz/spojeni-a-jizdenka/'
    driver.get(url)

    try:
        enter_station(driver, args)
        driver.find_element(By.XPATH, '//*[@id="depDate"]').clear()
        driver.find_element(By.XPATH, '//*[@id="depDate"]').send_keys(last_date)
        driver.find_element(By.XPATH, '//*[@id="timepicker-input"]/input').clear()
        driver.find_element(By.XPATH, '//*[@id="timepicker-input"]/input').send_keys(last_time)

        click_only_cd(driver)
        click_search_button(driver)
    except Exception as e:
        print(f"Error: Failed to reset search. {e}")

def scrape_content(driver):
    """Extract data from the current page of search results."""
    return (
        extract_content(driver, "//button[@class='btn btn--green' and @type='button']", "price"),
        extract_content(driver, '//span[contains(@data-bind, "text: journeyDateTextFrom()")]', "date"),
        extract_content(driver, ".//div[1]/ul[2]/li/ul/li[1]/div/div/p[2]", "time"),
        extract_content(driver, '//img[@class="meter-icon"]', "occupancy")
    )

def iterate_pages(driver, args):
    """Iterate through the specified number of pages and collect data."""
    all_prices, all_dates, all_times, all_occupancy = ["price"], ["date"], ["time"], ["occupancy"]

    for page_counter in range(args.pages):
        time.sleep(5)
        prices, dates, times, occupancy = scrape_content(driver)

        all_prices.extend(prices)
        all_dates.extend(dates)
        all_times.extend(times)
        all_occupancy.extend(occupancy)

        if page_counter < args.pages - 1:
            if page_counter % 34 == 0 and page_counter > 0:
                print(f"Reached page {page_counter}, resetting search...")
                enter_again(driver, all_dates[-1], all_times[-1])
                time.sleep(2)
            else:
                click_next_button(driver)

        print(f"Page {page_counter + 1}/{args.pages} scraped.")

    return all_dates, all_times, all_prices, all_occupancy

def import_to_csv_file(args, dates, times, prices, occupancy):
    """Save the scraped data into a CSV file."""
    with open(args.output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "Price", "Occupancy Level"])
        writer.writerows(zip(dates, times, prices, occupancy))

if __name__ == "__main__":
    try:
        args = get_arguments()
        driver = start_driver()

        accept_cookies(driver)
        enter_station(driver, args)
        clicking_to_add_day(driver)
        click_to_add_one_hour(driver)
        click_only_cd(driver)
        click_search_button(driver)

        dates, times, prices, occupancy = iterate_pages(driver, args)
        import_to_csv_file(args, dates, times, prices, occupancy)

    except Exception as e:
        print(f"Critical Error: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
