import asyncio
from datetime import datetime, timedelta
from patchright.async_api import async_playwright
import random
import sys

TARGET_HOUR = 13
TARGET_MINUTE = 59
TARGET_SECOND = 59

async def wait_until_target():
    while True:
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

        remaining = (target - now).total_seconds()

        if remaining <= 0:
            break

        # hitung jam, menit, detik
        hrs = int(remaining // 3600)
        mins = int((remaining % 3600) // 60)
        secs = int(remaining % 60)

        # print countdown (overwrite line)
        sys.stdout.write(f"\rCountdown: {hrs:02d}:{mins:02d}:{secs:02d}")
        sys.stdout.flush()

        await asyncio.sleep(1)

    print("\nWaktu target tercapai!")


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
        
        await page.goto("https://dyandraglobalstore-02.com/", wait_until="load")

        await wait_until_target()

        print("Mulai hunting tombol...")

        while True:
            await page.goto("https://dyandraglobalstore-02.com/", wait_until="load")

            target = page.locator("button:has-text('10 April 2026')").first
            
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