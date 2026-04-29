import asyncio
from datetime import datetime, timedelta
from patchright.async_api import async_playwright
import random
import sys

TARGET_HOUR = 8
TARGET_MINUTE =16
TARGET_SECOND = 30

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
        browser = await p.chromium.launch(
            channel="chrome",
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
            ]
        )
        
        context = await browser.new_context()
        
        async def block_resources(route):
            if route.request.resource_type in ["image", "font", "media"]:
                await route.abort()
            else:
                await route.continue_()

        await context.route("**/*", block_resources)
        
        page = await context.new_page()
        
        await page.goto("https://dyandraglobalstore-05.com/", wait_until="load")

        await wait_until_target()

        print("Mulai hunting tombol...")

        while True:
            await page.reload(wait_until="domcontentloaded")

            target = page.locator("button:has-text('29 April 2026')").first
            
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