import asyncio
from datetime import datetime, timedelta
from patchright.async_api import async_playwright
import random
import sys

TARGET_HOUR = 11
TARGET_MINUTE =59
TARGET_SECOND = 58
SESSION_PATH = './shared-browser-session'

seat = ["CAT 1"]
qty = ['2']


def ticket_selector(seat):
    return f'.ticket-item:has(h6:has-text("{seat}"))'

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
        
        found = False
        
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
        
        while True:
            try : 
                locator = page.locator(
                    "li",
                    has_text="Ticket Includes Government fee 10% and Platform fee 5%"
                )
                
                if await locator.first.is_visible(timeout=500):
                    should_reload = False
                    for i in range(len(seat)) :
                        await page.wait_for_selector(ticket_selector(seat[i]), timeout=1000)
                        seat_ticket = page.locator('.ticket-item').filter(
                        has=page.locator('h6', has_text=seat[i])
                        )
                        text_content = await seat_ticket.inner_text()   
                        print(text_content)
                        is_sold_out = "Sold Out" in text_content
                        is_fullbooked = "Fullbooked" in text_content
                        is_habis_terjual = "Habis Terjual" in text_content
                        is_habis_dipesan = "Habis Dipesan" in text_content
                        print(f"is_sold_out: {is_sold_out}, is_fullbooked: {is_fullbooked}, is_habis_terjual: {is_habis_terjual}, is_habis_dipesan: {is_habis_dipesan}")
                        if is_sold_out or is_fullbooked or is_habis_terjual or is_habis_dipesan:
                            print("Seat is SOLD OUT/ FULLBOOKED, skipping...")
                            should_reload = True
                            break                         
                        else:
                            print(f"Found seat: {seat[i]}")
                            select_element = seat_ticket.locator('.ticket-types')
                            await select_element.wait_for(state="visible")
                            await select_element.select_option(qty[i])
                            selected_value = await select_element.input_value()
                            print(f"Selected quantity: {selected_value}")
                            await page.click('#buy_ticket')
                            found = True
                            break
                    if found:
                        break
                    
                    if should_reload:
                        print("Reloaded...")
                        await page.reload(wait_until="domcontentloaded")
                        await asyncio.sleep(0.2)
            except Exception as e:
                 print("Page Ticket Picking not Ready:", e)

        await asyncio.sleep(999999)


asyncio.run(execute())