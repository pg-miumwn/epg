import asyncio
import json
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Apply stealth techniques
        await stealth_async(page)

        print("🌐 Visiting DTT Guide main page to pass IUAM...")
        await page.goto("https://dttguide.nbtc.go.th/dttguide/", wait_until="networkidle")

        print("📡 Making API request...")
        response = await page.evaluate("""
            async () => {
                const res = await fetch('https://dttguide.nbtc.go.th/BcsEpgDataServices/BcsEpgDataController/getProgramDataWeb', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ "channelType": "1" })
                });
                return await res.json();
            }
        """)

        # Filter and save the data
        filtered_data = [
            item for item in response['results']
            if item['channelNo'] in ['33', '31', '35', '25']
        ]
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=4)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
