import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def main():
    options = Options()
    options.add_argument("--headless=new")  # headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # Use undetected_chromedriver to avoid detection
    import undetected_chromedriver.v2 as uc
    driver = uc.Chrome(options=options)

    print("🌐 Visiting DTT Guide main page to pass IUAM...")
    driver.get("https://dttguide.nbtc.go.th/dttguide/")

    print("⏳ Waiting for IUAM challenge to complete...")
    time.sleep(10)  # wait for Cloudflare IUAM to finish

    print("📡 Making API request inside browser...")
    script = """
        return fetch('https://dttguide.nbtc.go.th/BcsEpgDataServices/BcsEpgDataController/getProgramDataWeb', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'accept': '*/*',
                'accept-language': 'en,th;q=0.9,en-US;q=0.8',
                'origin': 'https://dttguide.nbtc.go.th',
                'referer': 'https://dttguide.nbtc.go.th/dttguide/'
            },
            body: JSON.stringify({ channelType: "1" })
        }).then(res => res.json());
    """
    result = driver.execute_script(script)

    driver.quit()

    print("💾 Filtering channels...")
    filtered = [
        item for item in result.get("results", [])
        if int(item.get("channelNo", "0")) in {33, 31, 35, 25}
    ]

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(filtered)} channels to data.json")

if __name__ == "__main__":
    main()
