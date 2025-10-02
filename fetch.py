import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_website_title(url):
    """
    Launches undetected_chromedriver, navigates to a URL, and prints the title.
    Note: This code does NOT include functionality to bypass security measures.
    """
    driver = None
    try:
        # Initialize the undetected_chromedriver
        options = uc.ChromeOptions()
        # You can add options here, e.g., options.add_argument('--headless')
        
        # uc.Chrome() will automatically download and manage the appropriate ChromeDriver
        driver = uc.Chrome(options=options)
        
        print(f"Attempting to access: {url}")
        driver.get(url)
        
        # Wait for the title to be present (basic example wait)
        WebDriverWait(driver, 10).until(EC.title_is(driver.title))
        
        # Log the title
        title = driver.title
        print(f"Successfully accessed. Website Title: '{title}'")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            # Always close the browser when done
            driver.quit()

if __name__ == '__main__':
    target_url = "https://dttguide.nbtc.go.th/dttguide/"
    get_website_title(target_url)

# This code is for educational and ethical purposes only.
