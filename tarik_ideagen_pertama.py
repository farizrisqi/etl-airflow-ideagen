import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://lionairgroup.gaelenlighten.com")

         # 2. Isi username & password
    page.fill("#username", "risqi")
    page.fill("#password", "Sylvia123")
    page.wait_for_timeout(1000)
    # 3. Klik tombol login
    page.get_by_role("button", name="Login").click()
    page.wait_for_timeout(10000)
    # Navigasi awal
    page.locator("div").nth(5).click()
    page.get_by_role("link", name="This week").click()
    
    # 1. Klik Export
    page.get_by_role("button", name="Export As CSV").click()
    page.wait_for_timeout(10000)

    # Cleanup
    page.close()
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
