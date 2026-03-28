import os
import time
from playwright.sync_api import sync_playwright

USERNAME = os.getenv("COURT_USERNAME")
PASSWORD = os.getenv("COURT_PASSWORD")
URL = "https://pnwtennis.clubautomation.com/login"

def reserve_court():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        try:
            print(f"Navigating to {URL}...")
            # We wait for 'commit' so we can manually handle the wait time
            page.goto(URL, wait_until="commit")
            
            print("Waiting for page to fully stabilize (Hydration)...")
            # This waits until the network has been quiet for 500ms
            page.wait_for_load_state("networkidle")
            time.sleep(5) 

            # NEW STRATEGY: Find by Placeholder or Text (Pierces most JS wrappers)
            print("Searching for inputs by visible text...")
            
            # This looks for the box that has 'Username' near it in the DOM
            user_input = page.get_by_label("Username")
            # If that fails, look for the input box that has the word 'login' in its ID or name
            if not user_input.is_visible():
                user_input = page.locator('input[name="login"], input#login').first

            user_input.wait_for(state="visible", timeout=20000)
            print("Login field detected!")
            
            user_input.fill(USERNAME)
            
            # Target password by type to avoid ID issues
            page.locator('input[type="password"]').fill(PASSWORD)
            
            print("Credentials entered. Clicking Login...")
            # Target the button by the text 'Login' rather than ID
            page.get_by_role("button", name="Login").click()

            # Verify redirect
            page.wait_for_load_state("networkidle")
            time.sleep(5)
            
            print(f"Final URL: {page.url}")
            if "login" not in page.url:
                print("SUCCESS: Login achieved!")
            else:
                # If we are still here, the site might have rejected the login
                print("FAILED: Still on login page. Screenshot saved.")
                page.screenshot(path="login_failed_check_creds.png")

        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            page.screenshot(path="final_debug.png")
            # Save the raw HTML to the log so we can read it
            print("DEBUG: Current Page Content follows:")
            print(page.content()[:2000]) # Print first 2000 chars
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    reserve_court()
