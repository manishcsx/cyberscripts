import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from plyer import notification
from bs4 import BeautifulSoup

URL = "https://manishsas.t1cloudwaf.com/"

options = uc.ChromeOptions()
#options.add_argument("--headless")
driver = uc.Chrome(options=options)

def is_medium_in_stock(html):
    soup = BeautifulSoup(html, 'html.parser')
    buttons = soup.find_all(['button', 'div', 'span'])
    for btn in buttons:
        text = btn.get_text(strip=True)
        if text.startswith("Medium") and "Out of Stock" not in text:
            return True
    return False

def notify(title, message):
    notification.notify(title=title, message=message, timeout=15)

def main():
    print("Monitoring 'Medium' stock status with browser simulation...")
    while True:
        try:
            driver.get(URL)
            time.sleep(5)  
            html = driver.page_source
            if is_medium_in_stock(html):
                notify("Product Alert", "'Medium' size is now in stock.")
                print("Medium is in stock.")
                break
            else:
                print("Medium still out of stock. Retrying...")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
