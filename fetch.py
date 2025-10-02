import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import sys
import os

def main():
    """
    Launches an undetected Chrome browser, passes the IUAM challenge, 
    makes an internal fetch request, and saves the filtered data to a JSON file.
    """
    
    options = uc.ChromeOptions()
    
    # Check if running in CI environment
    is_ci = os.getenv('CI') == 'true' or os.getenv('GITHUB_ACTIONS') == 'true'
    
    if is_ci:
        # CI environment - use headless mode
        options.headless = True
        options.add_argument("--headless=new")
        print("🤖 Running in CI mode (headless)")
    else:
        # Local environment - use headful mode
        options.headless = False
        print("💻 Running in local mode (headful)")
    
    # Standard anti-detection arguments
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    try:
        # Auto-detect Chrome version - no version_main parameter
        driver = uc.Chrome(options=options)
        print("✅ Chrome driver launched successfully")
    except Exception as e:
        print("❌ FAILED to launch Chrome driver.")
        print(f"Error: {e}")
        sys.exit(1)
    
    try:
        print("🌐 Visiting DTT Guide main page to pass IUAM...")
        driver.get("https://dttguide.nbtc.go.th/dttguide/")
        
        # --- RELIABLE WAIT FOR IUAM COMPLETION ---
        SUCCESS_PAGE_SELECTOR = (By.ID, "epg_list_container")
        
        print("⏳ Waiting up to 30 seconds for IUAM challenge to complete...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(SUCCESS_PAGE_SELECTOR)
        )
        print("✅ IUAM Challenge successfully passed. Page is loaded.")
        
        # --- API CALL INSIDE BROWSER ---
        print("📡 Making API request inside browser...")
        script = """
        return fetch("https://dttguide.nbtc.go.th/BcsEpgDataServices/BcsEpgDataController/getProgramDataWeb", {
            method: "POST",
            headers: {
                "Accept": "*/*",
                "Content-Type": "application/json; charset=UTF-8"
            },
            body: JSON.stringify({"channelType":"1"})
        }).then(res => res.text());
        """
        
        result = driver.execute_script(script)
        
        # --- DATA PROCESSING ---
        try:
            data = json.loads(result)
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON: {e}")
            print("Raw response:", result[:500] + "...")
            driver.quit()
            sys.exit(1)
        
        # Filter data for the specified channel numbers
        channel_targets = [33, 31, 35, 25]
        filtered = [
            x for x in data.get("results", []) 
            if int(x.get("channelNo", 0)) in channel_targets
        ]
        
        # --- SAVE DATA ---
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(filtered, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Data for channels {channel_targets} saved to data.json")
        print(f"📊 Retrieved {len(filtered)} channel records")
        
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        sys.exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
