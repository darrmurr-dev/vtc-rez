import os
import time
from playwright.sync_api import sync_playwright

# Credentials from GitHub Secrets
USERNAME = os.getenv("COURT_USERNAME")
PASSWORD = os.getenv("COURT_PASSWORD")
URL = "https://pnwtennis.clubautomation.com/login"

def reserve():
    with sync_playwright() as p:
        # Open browser in 'stealth' mode to avoid bot detection
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36")
        page = context.new_page()

        # 1. Login
        page.goto(URL)
        page.fill('input[name="login"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        page.click('button[type="submit"]')
        
        # 2. Navigate to Reserve a Court
        # ClubAutomation usually has a specific sidebar link or URL for court booking
        page.wait_for_selector('text=Reserve a Court')
        page.click('text=Reserve a Court')

        # 3. Select Date and Time
        # You will need to inspect the page to find the specific ID for the court/time
        # Example: select the date for 7 days from now
        # page.click('#date-picker-id') 

        # 4. The "Hammer" Loop
        # This clicks the reserve button as soon as it appears
        while True:
            if page.is_visible('button.reserve-btn-class'): # Replace with actual class
                page.click('button.reserve-btn-class')
                print("Court reserved!")
                break
            time.sleep(0.5) # Wait half a second and try again

        browser.close()

if __name__ == "__main__":
    reserve()
