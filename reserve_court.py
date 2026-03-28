import os
import time
from playwright.sync_api import sync_playwright

USERNAME = os.getenv("COURT_USERNAME")
PASSWORD = os.getenv("COURT_PASSWORD")
URL = "https://pnwtennis.clubautomation.com/login"

def reserve_court():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # We add a larger viewport to ensure the login box isn't 'off-screen'
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        try:
            print(f"Navigating to {URL}...")
            page.goto(URL, wait_until="networkidle")
            
            # Hard wait for 5 seconds to let the 'Shadow' elements render
            time.sleep(5)

            print("Attempting to pierce Shadow DOM for login fields...")
            
            # Use 'control' selectors that ignore frame boundaries
            # The '>>' tells Playwright to look deep into every layer
            user_input = page.locator('id=login')
            pass_input = page.locator('id=password')
            login_btn = page.locator('id=loginButton')

            # Check if they are actually there before filling
            user_input.wait_for(state="visible", timeout=15000)
            
            print("Fields found! Filling credentials...")
            user_input.fill(USERNAME)
            pass_input.fill(PASSWORD)
            
            print("Clicking Login...")
            login_btn.click()

            # Verify if we moved to the dashboard
            page.wait_for_load_state("networkidle")
            time.sleep(3)
            
            print(f"Current URL: {page.url}")
            if "login" not in page.url:
                print("SUCCESS: Login achieved!")
            else:
                print("STILL ON LOGIN: Check credentials or error messages.")
                page.screenshot(path="login_fail_visible.png")

        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            page.screenshot(path="shadow_error_screenshot.png")
            # This captures the HTML so we can see the 'Shadow' structure if it fails
            with open("page_source.html", "w") as f:
                f.write(page.content())
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    reserve_court()
