import os
from playwright.sync_api import sync_playwright

USERNAME = os.getenv("COURT_USERNAME")
PASSWORD = os.getenv("COURT_PASSWORD")
URL = "https://pnwtennis.clubautomation.com/login"

def reserve():
    with sync_playwright() as p:
        # Launch browser with a real-world User Agent
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print("Navigating to PNW Tennis...")
        page.goto(URL, wait_until="networkidle")

        # Try to find the login boxes with multiple possible names
        print("Attempting to log in...")
        try:
            # ClubAutomation usually uses 'login' or 'username'
            page.wait_for_selector('input[name="login"]', timeout=10000)
            page.fill('input[name="login"]', USERNAME)
            page.fill('input[name="password"]', PASSWORD)
            page.click('button[type="submit"]')
            print("Login submitted!")
        except Exception as e:
            print(f"Could not find login boxes. Saving screenshot for debug...")
            page.screenshot(path="error_screenshot.png")
            raise e

        # Wait to see if we reached the dashboard
        page.wait_for_load_state("networkidle")
        print(f"Successfully logged in! Current page: {page.title()}")
        
        # NEXT STEP: Add your navigation to the court calendar here
        
        browser.close()

if __name__ == "__main__":
    reserve()
