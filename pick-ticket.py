from patchright.async_api import async_playwright
import asyncio

#Sarah

# Duality Package
# CAT 4
# CAT 2
# CAT 3
# CAT 6
# CAT 1

membership_ready = False
SESSION_PATH = './shared-browser-session'
url = ""
seat = ["Duality Package"]
qty = ['2']
membership = "ND475307598" #APABILA TIDAK ADA KOSONGKAN DENGAN ""

def ticket_selector(seat):
    return f'.ticket-item:has(h6:has-text("{seat}"))'

async def execute():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=SESSION_PATH,
            channel="chrome", #kalau tidak ada ganti dengan "msedge"
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
            ]
        )
        
        page = await context.new_page()
        
        await page.goto(url, wait_until="load")
        await asyncio.sleep(999999)
        
        while True:
            await page.reload(wait_until="domcontentloaded")
            await asyncio.sleep(0.2)
            for i in range(len(seat)) :
                await page.wait_for_selector(ticket_selector(seat[i]), timeout=3000)
                seat_ticket = page.locator('.ticket-item').filter(
                has=page.locator('h6', has_text=seat[i])
                )
                text_content = await seat_ticket.inner_text()   
                print(text_content)
                is_sold_out = "Sold Out" in text_content
                is_fullbooked = "Fullbooked" in text_content
                is_habis_terjual = "Habis Terjual" in text_content
                print(f"is_sold_out: {is_sold_out}, is_fullbooked: {is_fullbooked}", is_habis_terjual)
                if is_sold_out or is_fullbooked or is_habis_terjual:
                    print("Seat is SOLD OUT/ FULLBOOKED, skipping...")
                else:
                    print(f"Found seat: {seat[i]}")
                    select_element = seat_ticket.locator('.ticket-types')
                    await select_element.wait_for(state="visible")
                    await select_element.select_option(qty[i])
                    selected_value = await select_element.input_value()
                    print(f"Selected quantity: {selected_value}")
                    if membership_ready:
                        locator = page.get_by_placeholder("example", exact=False)
                        if await locator.is_visible():
                            await locator.fill(membership)
                        else:
                            print("Membership not ready")
                        btn = page.get_by_role("button", name="Submit", exact=False)
                        if await btn.count() > 0:
                            await btn.click()
                        else:
                            print("Submit Button not ready")
                    await page.click('#buy_ticket')
                
            
asyncio.run(execute())

