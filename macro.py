import asyncio
import random
from patchright.async_api import async_playwright

async def human_delay(min_ms=200, max_ms=800):
    await asyncio.sleep(random.uniform(min_ms/1000, max_ms/1000))

async def execute():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            channel="chrome",
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
            ]
        )

        context = await browser.new_context()
        page = await context.new_page()

        print("OPEN PAGE...")
        await page.goto("https://dyandraglobalstore-02.com/")

        while True:
            try:
                print("Reload page")
                
                await human_delay(100, 300)
                await page.reload(wait_until="domcontentloaded")

                await human_delay(100, 300)

                print("Mencari tombol...")
                target = page.locator("button:has-text('9 April 2026')").first

                await target.wait_for(timeout=3000)

                await target.scroll_into_view_if_needed()
                await human_delay(100, 300)

                is_disabled = await target.is_disabled()
                print("Disabled:", is_disabled)

                if not is_disabled:
                    # hover dulu
                    await target.hover()
                    await human_delay(100, 300)

                    await target.click()
                    print("CLICKED!")
                    break
                else:
                    print("Tombol masih disabled... lanjut retry")

            except Exception as e:
                print("Belum siap:", str(e))

            await human_delay(100, 300)

        print("SELESAI, menunggu...")
        await asyncio.sleep(999999999)

asyncio.run(execute())