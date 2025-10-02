import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import sys

def main():
    """
    Launches an undetected Chrome browser, passes the IUAM challenge, 
    makes an internal fetch request, and saves the filtered data to a JSON file.
    """
    
    options = uc.ChromeOptions()
    # Setting to False runs in 'headful' mode, which is better for anti-bot pages
    options.headless = False  
    
    # Standard anti-detection arguments
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Use a try/except block to handle the Chrome version mismatch gracefully
    try:
        # NOTE: Keeping version_main=140 to solve the previous error. 
        # If your Chrome updates, you MUST change this number or remove the argument.
        driver = uc.Chrome(options=options, version_main=140)
    except Exception as e:
        print("❌ FAILED to launch Chrome driver.")
        print(f"Error: {e}")
        print("Please check your installed Chrome version matches 'version_main=140' or update the argument.")
        sys.exit(1)


    print("🌐 Visiting DTT Guide main page to pass IUAM...")
    driver.get("https://dttguide.nbtc.go.th/dttguide/")

    # --- RELIABLE WAIT FOR IUAM COMPLETION ---
    # Find a reliable selector on the successfully loaded page.
    # In this case, we'll try to wait for the main table container to appear.
    SUCCESS_PAGE_SELECTOR = (By.ID, "epg_list_container")
    
    print("⏳ Waiting up to 30 seconds for IUAM challenge to complete...")

    try:
        # Wait until the main content element is present
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(SUCCESS_PAGE_SELECTOR)
        )
        print("✅ IUAM Challenge successfully passed. Page is loaded.")

    except Exception:
        print("❌ Failed to load the final page within the timeout (30 seconds).")
        print("This usually means the anti-bot protection was not passed.")
        driver.quit()
        return

    # --- API CALL INSIDE BROWSER ---
    print("📡 Making API request inside browser...")
    script = """
    return fetch("https://dttguide.nbtc.go.th/BcsEpgDataServices/BcsEpgDataController/getProgramDataWeb", {
        method: "POST",
        headers: {
            "Accept": "*/*",
            "Content-Type": "application/json; charset=UTF-8"
        },
        // The fetch request automatically includes the cookies gained from passing the IUAM
        body: JSON.stringify({"channelType":"1"})
    }).then(res => res.text());
    """
    
    # Execute the JavaScript fetch request
    result = driver.execute_script(script)

    # --- DATA PROCESSING ---
    try:
        data = json.loads(result)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON: {e}")
        print("Raw response (check for error message):", result[:500] + "...")
        driver.quit()
        return

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
    driver.quit()

if __name__ == "__main__":
    main()
