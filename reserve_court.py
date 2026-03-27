import os
import time
from playwright.sync_api import sync_playwright

USERNAME = os.getenv("COURT_USERNAME")
PASSWORD = os.getenv("COURT_PASSWORD")
URL = "https://pnwtennis.clubautomation.com/login"

def reserve_court():
    with sync_playwright() as p:
        # We add 'slow_mo' to give the site's Javascript time to breathe
        browser = p.chromium.launch(headless=True, slow_mo=500) 
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()

        try:
            print(f"Navigating to {URL}...")
            # 'commit' means we wait for the server to acknowledge the request
            page.goto(URL, wait_until="commit", timeout=60000)
            
            # CRITICAL: We wait 5 seconds for the Javascript to build the form
            print("Waiting for Javascript to build the login form...")
            time.sleep(5) 

            # Attempt 1: Using the Label (Most reliable for dynamic forms)
            print("Looking for Username field...")
            try:
                # This looks for the text "Username" on the screen and finds the box next to it
                user_box = page.get_by_label("Username")
                user_box.wait_for(state="visible", timeout=10000)
                user_box.fill(USERNAME)
                
                pass_box = page.get_by_label("Password")
                pass_box.fill(PASSWORD)
                print("Filled credentials via Label.")
            except:
                print("Label failed, falling back to ID selectors...")
                page.fill("#login", USERNAME)
                page.fill("#password", PASSWORD)

            # Click the login button using the data-testid from your HTML
            print("Clicking Login...")
            page.locator('button[data-testid="loginFormSubmitButton"]').click()

            # Wait to see if we move off the login page
            page.wait_for_load_state("networkidle")
            time.sleep(5)
            
            print(f"Final URL: {page.url}")
            if "login" not in page.url:
                print("SUCCESS: We are in.")
            else:
                print("FAILED: Still on login page. Saving debug image.")
                page.screenshot(path="failed_login_state.png")

        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            page.screenshot(path="error_trace_screenshot.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    reserve_court()
