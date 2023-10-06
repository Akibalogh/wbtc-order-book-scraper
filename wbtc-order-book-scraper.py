
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
        # Convert 'Date & Time' to just 'Date' in the 'YYYY-MM-DD' format
from datetime import datetime
date_time_str = row.find('mat-cell', {'class': 'cdk-column-timestamp'}).text.strip()
date_time_obj = datetime.strptime(date_time_str, '%b %d %Y - %H:%M')
date_str = date_time_obj.strftime('%Y-%m-%d')

        merchant = row.find('mat-cell', {'class': 'cdk-column-merchant'}).text.strip()
        amount = row.find('mat-cell', {'class': 'cdk-column-amount'}).text.strip()
        
        
        # Identify whether it's a Mint or Burn based on the class attribute of img tag in 'mat-cell cdk-column-action'
        action_cell = row.find('mat-cell', {'class': 'cdk-column-action'})
        action_img = action_cell.find('img')
        action = 'Mint' if 'mint' in action_img.get('class', []) else 'Burn'
        
        # Write to CSV (once, including the action)
        csv_writer.writerow([date_str, merchant, amount, action])

# Initialize Selenium and CSV writer
driver = webdriver.Safari()
driver.get("https://wbtc.network/dashboard/order-book")
wait = WebDriverWait(driver, 10)

csv_file = open('scraped_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Date & Time', 'Merchant', 'Amount', 'Action'])  # Header

# Wait for the first page to load
time.sleep(2)


# Testing feature: Set this to True to only grab data from the first two pages for testing
testing_mode = True

# Counter for pages processed
page_count = 0

while True:
    # Extract data from the current page
    page_source = driver.page_source
    extract_data(page_source, csv_writer)
    
    page_count += 1  # Increment the page counter
    
    if testing_mode and page_count >= 2:
        break  # Exit loop if in testing mode and two pages have been processed

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
