import asyncio
from datetime import datetime, timedelta
from patchright.async_api import async_playwright
import random

TARGET_HOUR = 1
TARGET_MINUTE = 13
TARGET_SECOND = 45

async def wait_until_target():
    now = datetime.now()
    target = now.replace(
        hour=TARGET_HOUR,
        minute=TARGET_MINUTE,
        second=TARGET_SECOND,
        microsecond=0
    )

    # kalau waktu sudah lewat, target besok
    if now >= target:
        target += timedelta(days=1)

    wait_seconds = (target - now).total_seconds()
    print(f"Menunggu {wait_seconds:.2f} detik sampai target time...")
    
    await asyncio.sleep(wait_seconds)


async def execute():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            channel="msedge",
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
            ]
        )
        
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto("http://localhost:3000", wait_until="load")

        # ⏳ Tunggu sampai jam tertentu
        await wait_until_target()

        print("Mulai hunting tombol...")

        while True:
            await page.goto("http://localhost:3000", wait_until="load")

            target = page.locator("button:has-text('9 April 2026')").first
            
            try:
                await target.wait_for(timeout=3000)
                is_disabled = await target.is_disabled()
                print("Disabled:", is_disabled)

                if not is_disabled:
                    await asyncio.sleep(0.3)

                    await target.hover()
                    await asyncio.sleep(0.2)

                    await target.click()
                    print("CLICKED!")
                    break

            except:
                print("Button belum ada")

            await asyncio.sleep(random.uniform(0.5, 1))

        await asyncio.sleep(999999)


asyncio.run(execute())