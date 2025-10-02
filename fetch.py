import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_website_title(url):
    driver = None
    try:
        # Initialize the undetected_chromedriver
        options = uc.ChromeOptions()
        
        # --- CRITICAL FIXES FOR CI/CD ---
        # 1. Enable headless mode (required for servers/CI runners)
        options.add_argument('--headless=new') # Use 'new' for modern Chrome
        
        # 2. Disable sandbox (often required in Linux CI environments)
        options.add_argument('--no-sandbox') 
        
        # 3. Disable shared memory (fixes issues in some environments)
        options.add_argument('--disable-dev-shm-usage')
        
        # 4. Add a dummy window size (often required with headless)
        options.add_argument('--window-size=1920,1080')
        # -------------------------------
        
        driver = uc.Chrome(options=options)
        
        print(f"Attempting to access: {url}")
        driver.get(url)
        
        # ... rest of your code to log title
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

# This code is for educational and ethical purposes only.
