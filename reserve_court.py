import os
import time
from playwright.sync_api import sync_playwright

# 1. Configuration - Pulls from your GitHub Secrets
USERNAME = os.getenv("COURT_USERNAME")
PASSWORD = os.getenv("COURT_PASSWORD")
LOGIN_URL = "https://pnwtennis.clubautomation.com/login"

def reserve_court():
    with sync_playwright() as p:
        # Launch browser with stealth settings to avoid being flagged as a bot
        # We use a real-world User Agent to look like a standard Windows Chrome user
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            # --- STEP 1: LOGIN ---
            print(f"Navigating to {LOGIN_URL}...")
            page.goto(LOGIN_URL, wait_until="networkidle")

            print("Attempting to fill login credentials...")
            # We target 'login' for email and 'input[type="password"]' to skip the hidden 'login_token'
            page.wait_for_selector('input[name="login"]', timeout=15000)
            page.fill('input[name="login"]', USERNAME)
            
            page.wait_for_selector('input[type="password"]', timeout=10000)
            page.fill('input[type="password"]', PASSWORD)
            
            print("Credentials entered. Clicking sign-in...")
            page.click('button[type="submit"]')

            # Wait for the dashboard to load to verify login success
            page.wait_for_load_state("networkidle")
            print(f"Login Successful. Page Title: {page.title()}")

            # --- STEP 2: NAVIGATE TO RESERVATIONS ---
            # Most ClubAutomation sites have a specific 'Reserve a Court' link or URL
            # Adjust the text below if your club uses different wording (e.g., 'Court Scheduler')
            print("Navigating to the reservation scheduler...")
            page.get_by_role("link", name="Reserve a Court").click()
            page.wait_for_load_state("networkidle")

            # --- STEP 3: SELECT COURT & TIME ---
            # Note: This part varies by club. Usually, you need to select a date.
            # Example: Selecting a court for 7 days from now
            # page.click(".date-picker-selector") 
            
            print("Scheduler loaded. Current URL:", page.url)
            
            # --- STEP 4: THE SNIPE (OPTIONAL PLACEHOLDER) ---
            # If you want to click a specific time (e.g., 8:00 AM), 
            # you would use something like:
            # page.get_by_text("8:00am").first.click()
            
            print("Agent task complete. Closing session.")

        except Exception as e:
            print(f"ERROR ENCOUNTERED: {e}")
            # Take a screenshot so you can see exactly what the bot saw when it failed
            page.screenshot(path="error_screenshot.png")
            print("Screenshot saved as 'error_screenshot.png' in the Action Artifacts.")
            raise e

        finally:
            browser.close()

if __name__ == "__main__":
    if not USERNAME or not PASSWORD:
        print("ERROR: Credentials not found in Environment Variables.")
    else:
        reserve_court()
