import os
import time
from playwright.sync_api import sync_playwright

# Configuration from GitHub Secrets
USERNAME = os.getenv("COURT_USERNAME")
PASSWORD = os.getenv("COURT_PASSWORD")
URL = "https://pnwtennis.clubautomation.com/login"

def reserve_court():
    with sync_playwright() as p:
        # Launching with stealth arguments to bypass the 'Daxko/ClubAutomation' bot detection
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print(f"Navigating to {URL}...")
            # We wait for 'networkidle' to ensure the 'login_token' has loaded
            page.goto(URL, wait_until="networkidle", timeout=60000)

            print("Locating login fields...")
            
            # 1. Fill Username (using the ID 'login' from your HTML)
            page.wait_for_selector("#login", timeout=15000)
            page.fill("#login", USERNAME)
            print("Username entered.")

            # 2. Fill Password (using the ID 'password' from your HTML)
            page.wait_for_selector("#password", timeout=10000)
            page.fill("#password", PASSWORD)
            print("Password entered.")

            # 3. Click the Login Button (using the specific ID 'loginButton')
            # We use click() then wait for the URL to change
            print("Clicking login button...")
            page.click("#loginButton")

            # 4. Wait for the page to transition after login
            # If the login is successful, the URL will no longer contain '/login'
            page.wait_for_load_state("networkidle")
            time.sleep(3) # Give it a moment to redirect
            
            print(f"Final URL after login: {page.url}")
            print(f"Final Page Title: {page.title()}")

            if "login" in page.url:
                print("STILL ON LOGIN PAGE: Check for error messages.")
                page.screenshot(path="login_failed.png")
            else:
                print("SUCCESS: Login achieved.")
                # You can add your court navigation here next!

        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            page.screenshot(path="error_screenshot.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    reserve_court()
