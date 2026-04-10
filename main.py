import asyncio
import time
from playwright.async_api import async_playwright
async def execute():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        while True:
            await page.goto("http://localhost:3000", wait_until="load")
            print("PAGE LOADED")
            target = page.locator("button:has-text('9 April 2026')").first
            
            try:
                await target.wait_for(timeout=2000)
                is_disabled = await target.is_disabled()
                print("Disabled:", is_disabled)
                if not is_disabled:
                    await target.click(force=True)
                    print("CLICKED!")
                    break
            except:
                print("Button belum ada")
                await asyncio.sleep(0.05)
        await asyncio.sleep(9999999999)
asyncio.run(execute())