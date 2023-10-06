from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time

def extract_data(page_source, csv_writer):
    soup = BeautifulSoup(page_source, 'html.parser')
    rows = soup.find_all('mat-row', {'class': 'master-row'})
    
    for row in rows:
        date_time = row.find('mat-cell', {'class': 'cdk-column-timestamp'}).text.strip()
        merchant = row.find('mat-cell', {'class': 'cdk-column-merchant'}).text.strip()
        amount = row.find('mat-cell', {'class': 'cdk-column-amount'}).text.strip()
        
        # Write to CSV
        csv_writer.writerow([date_time, merchant, amount])

# Initialize Selenium and CSV writer
driver = webdriver.Safari()
driver.get("https://wbtc.network/dashboard/order-book")
wait = WebDriverWait(driver, 10)

csv_file = open('scraped_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Date & Time', 'Merchant', 'Amount'])  # Header

# Wait for the first page to load
time.sleep(2)

while True:
    # Extract data from the current page
    page_source = driver.page_source
    extract_data(page_source, csv_writer)

    # Go to the next page
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mat-paginator-navigation-next")))
        if not next_button.is_enabled():
            break
        next_button.click()
    except:
        break

    # Wait for the next page to load
    time.sleep(2)

# Close the browser and CSV file
driver.quit()
csv_file.close()
