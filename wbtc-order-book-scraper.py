from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time

def extract_data(page_source, csv_writer):
    global seen_rows
    soup = BeautifulSoup(page_source, 'html.parser')
    rows = soup.find_all('mat-row', {'class': 'master-row'})
    
    for row in rows:
        date_time_str = row.find('mat-cell', {'class': 'cdk-column-timestamp'}).text.strip()
        date_time_obj = datetime.strptime(date_time_str, '%b %d %Y - %H:%M')
        date_str = date_time_obj.strftime('%Y-%m-%d')
        merchant = row.find('mat-cell', {'class': 'cdk-column-merchant'}).text.strip()
        amount = row.find('mat-cell', {'class': 'cdk-column-amount'}).text.strip()

        action_cell = row.find('mat-cell', {'class': 'cdk-column-action'})
        action_img = action_cell.find('img')
        action = 'Mint' if 'mint' in action_img.get('class', []) else 'Burn'
        
        # Check for duplicates before writing to CSV
        row_data = (date_str, merchant, amount)
        if row_data not in seen_rows:
            csv_writer.writerow([date_str, merchant, amount, action])
            seen_rows.add(row_data)

# Initialize Selenium and CSV writer
driver = webdriver.Safari()
driver.get("https://wbtc.network/dashboard/order-book")
wait = WebDriverWait(driver, 10)

csv_file = open('scraped_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Date & Time', 'Merchant', 'Amount', 'Action'])  # Header

extract_data(driver.page_source, csv_writer)  # Scrape the initial page
prev_page_source = driver.page_source

# Initialize seen_rows set
seen_rows = set()

# Testing feature: Set this to True to only grab data from the first two pages for testing
testing_mode = False
page_count = 0

while True:
    # Scrape data from the current page first
    extract_data(prev_page_source, csv_writer)
    page_count += 1
    
    if testing_mode and page_count >= 2:
        break

    # Go to the next page
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mat-paginator-navigation-next")))
        if not next_button.is_enabled():
            break
        next_button.click()

        time.sleep(2)
        curr_page_source = driver.page_source
        if curr_page_source == prev_page_source:  # If pages are identical
            time.sleep(3)  # Add an additional delay
            curr_page_source = driver.page_source  # Fetch page source again

        prev_page_source = curr_page_source  # Update for the next iteration
    except:
        break

# Close the browser and CSV file
driver.quit()
csv_file.close()
