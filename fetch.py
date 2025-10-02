# fetch_dttguide.py
import json
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def main():
    async with async_playwright() as p:
        print("🌐 Launching browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Apply stealth to bypass automation detection
        await stealth_async(page)

        print("🌍 Visiting DTT Guide to pass Cloudflare IUAM...")
        await page.goto(
            "https://dttguide.nbtc.go.th/dttguide/",
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("⏳ Waiting for IUAM challenge to complete...")
        await page.wait_for_timeout(10000)  # wait 10 seconds

        print("📡 Fetching program data...")
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

        # Filter channels we want
        filtered = [
            r for r in result.get("results", [])
            if int(r.get("channelNo", "0")) in {33, 31, 35, 25}
        ]

        print(f"💾 Saving {len(filtered)} channels to data.json")
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(filtered, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
