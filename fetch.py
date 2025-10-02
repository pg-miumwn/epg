# fetch_dttguide.py
import json
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        # Use Chromium with stealth settings
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        page = await context.new_page()

        print("🌐 Visiting DTT Guide main page to pass IUAM...")
        await page.goto("https://dttguide.nbtc.go.th/dttguide/", wait_until="networkidle")

        print("📡 Making API request...")
        result = await page.evaluate("""
            async () => {
                const res = await fetch(
                    "https://dttguide.nbtc.go.th/BcsEpgDataServices/BcsEpgDataController/getProgramDataWeb",
                    {
                        method: "POST",
                        headers: {
                            "accept": "*/*",
                            "accept-language": "en,th;q=0.9,en-US;q=0.8",
                            "content-type": "application/json; charset=UTF-8",
                            "origin": "https://dttguide.nbtc.go.th",
                            "referer": "https://dttguide.nbtc.go.th/dttguide/"
                        },
                        body: JSON.stringify({ channelType: "1" })
                    }
                );
                return await res.json();
            }
        """)

        await browser.close()

        # Filter results for channels we want
        filtered = [
            r for r in result.get("results", [])
            if int(r.get("channelNo", "0")) in {33, 31, 35, 25}
        ]

        print(f"📁 Saving {len(filtered)} channels to data.json")
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(filtered, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    asyncio.run(main())
