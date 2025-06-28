import time
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from PIL import Image
from tqdm import tqdm

# Set scraping duration (in seconds)
scrape_duration = 2 * 60  # Adjusted to 2 minutes as in your code
interval = 5  # Delay between refreshes/scrapes
iterations = scrape_duration // interval

# Setup Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
try:
    driver = webdriver.Chrome(options=options)
except WebDriverException:
    print("Can't open Chrome browser. Make sure ChromeDriver is installed and configured.")
    exit()

# Open target website
url = "http://manishsas.t1cloudwaf.com/"
try:
    driver.get(url)
except WebDriverException:
    print("Can't scrape any more. Website not reachable.")
    driver.quit()
    exit()

# Screenshot flag
screenshot_taken = False
print("Starting scraping for 2 minutes with page refresh...\n")

try:
    for _ in tqdm(range(iterations), desc="Scraping Progress", unit="check"):
        try:
            # Refresh the page to get updated content
            driver.refresh() #calls the method to refresh chrome over and over again
            time.sleep(2)  # Give it a second or two to fully reload

            # Finds "Medium" size button through inspect element via dev tools
            size_m_button = driver.find_element(By.CSS_SELECTOR, 'button[data-size="m"]')

            # Check availability based on class and 'disabled' attribute
            button_class = size_m_button.get_attribute('class')
            is_disabled = size_m_button.get_attribute('disabled') is not None

            if 'out-of-stock' not in button_class and not is_disabled:
                print("\n✅ Size M is AVAILABLE!")

                if not screenshot_taken:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_path = os.path.join(os.getcwd(), f"screenshot_{timestamp}.png")
                    driver.save_screenshot(screenshot_path)
                    print(f"📸 Screenshot saved to: {screenshot_path}")
                    screenshot_taken = True
            else:
                print("⛔ Size M is NOT available. Data cant be found")

        except NoSuchElementException:
            print("❓ Size M button not found.")

        time.sleep(interval)

except Exception as e:
    print(f"\nCan't scrape any more. Error: {e}")

finally:
    driver.quit()
    print("🔚 Scraping finished.")
