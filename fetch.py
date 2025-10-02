import undetected_chromedriver as uc
import os  # <-- Import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_website_title(url):
    driver = None
    try:
        options = uc.ChromeOptions()
        
        # --- CRITICAL FIXES FOR CI/CD ---
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox') 
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        # --- NEW FIX: Force Chrome Executable Path ---
        # Get the path set in the GitHub Workflow environment variable
        chrome_bin_path = os.environ.get("CHROME_BIN") 
        if chrome_bin_path:
            options.binary_location = chrome_bin_path
            print(f"Using Chrome binary at: {chrome_bin_path}")
        else:
            print("Warning: CHROME_BIN environment variable not found. Relying on default system search.")
        # --------------------------------------------
        
        # uc.Chrome will now look for the browser at options.binary_location
        driver = uc.Chrome(options=options)
        
        # ... rest of your code
        print(f"Attempting to access: {url}")
        driver.get(url)
        
        WebDriverWait(driver, 10).until(EC.title_is(driver.title))
        title = driver.title
        print(f"Successfully accessed. Website Title: '{title}'")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    target_url = "https://dttguide.nbtc.go.th/dttguide/"
    get_website_title(target_url)
