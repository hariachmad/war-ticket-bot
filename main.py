import asyncio
from datetime import datetime, timedelta
from patchright.async_api import async_playwright
import random
import sys

TARGET_HOUR = 11
TARGET_MINUTE =59
TARGET_SECOND = 58
SESSION_PATH = './shared-browser-session'

async def wait_until_target():
    now = datetime.now()
    target = now.replace(
        hour=TARGET_HOUR,
        minute=TARGET_MINUTE,
        second=TARGET_SECOND,
        microsecond=0
    )

    if now >= target:
        target += timedelta(days=1)

    while True:
        now = datetime.now()
        remaining = (target - now).total_seconds()

        if remaining <= 0:
            break

        hrs = int(remaining // 3600)
        mins = int((remaining % 3600) // 60)
        secs = int(remaining % 60)

        sys.stdout.write(f"\rCountdown: {hrs:02d}:{mins:02d}:{secs:02d}")
        sys.stdout.flush()

    print("\nWaktu target tercapai!")


async def execute():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=SESSION_PATH,
            channel="chrome",
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
            ]
        )
        
        # context = await browser.new_context()

        
        page = await context.new_page()
        
        await page.goto("https://dyandraglobalstore-04.com/", wait_until="load")

        await wait_until_target()

        print("Mulai hunting tombol...")

        while True:
            await page.reload(wait_until="domcontentloaded")

            target = page.locator("button:has-text('14 Mei 2026')").first
            
            try:
                await target.wait_for(timeout=3000)
                is_disabled = await target.is_disabled()
                print("Disabled:", is_disabled)

                if not is_disabled:
                    await target.click()
                    print("CLICKED!")
                    break

            except:
                print("Button belum ada")

        await asyncio.sleep(999999)


asyncio.run(execute())