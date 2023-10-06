from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def extract_data(page_source):
    print("Extracting data from current page...")
    soup = BeautifulSoup(page_source, 'html.parser')
    rows = soup.find_all('mat-row', {'class': 'master-row'})
    
    for row in rows:
        date_time = row.find('mat-cell', {'class': 'cdk-column-timestamp'}).text.strip()
        merchant = row.find('mat-cell', {'class': 'cdk-column-merchant'}).text.strip()
        amount = row.find('mat-cell', {'class': 'cdk-column-amount'}).text.strip()
        print(f"Date & Time: {date_time}, Merchant: {merchant}, Amount: {amount}")
    print("Data extraction complete for current page.")

# Initialize Selenium
print("Initializing Selenium...")
driver = webdriver.Safari()
driver.get("https://wbtc.network/dashboard/order-book")
wait = WebDriverWait(driver, 10)

# Wait for the first page to load
print("Waiting for the first page to load...")
time.sleep(2)

while True:
    # Extract data from the current page
    print("Fetching current page HTML...")
    page_source = driver.page_source
    extract_data(page_source)

    # Go to the next page
    print("Navigating to the next page...")
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mat-paginator-navigation-next")))
        if not next_button.is_enabled():
            print("Reached the last page.")
            break
        next_button.click()
    except:
        print("Unable to find or click the next button.")
        break

    # Wait for the next page to load
    print("Waiting for the next page to load...")
    time.sleep(2)

# Close the browser
print("Closing the browser...")
driver.quit()
print("Process completed.")
