import os
import time
from playwright.sync_api import sync_playwright

USERNAME = os.getenv("COURT_USERNAME")
PASSWORD = os.getenv("COURT_PASSWORD")
URL = "https://pnwtennis.clubautomation.com/login"

def reserve_court():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print(f"Navigating to {URL}...")
            page.goto(URL, wait_until="networkidle", timeout=60000)
            
            # Give the site 5 seconds to load any background frames
            time.sleep(5)

            # --- SEARCHING ALL FRAMES ---
            target_area = None
            
            # 1. Check the main page first
            if page.query_selector("#login"):
                target_area = page
                print("Found login box on the main page.")
            else:
                # 2. If not on main page, search every hidden 'iframe'
                print(f"Not on main page. Searching {len(page.frames)} frames...")
                for frame in page.frames:
                    try:
                        if frame.query_selector("#login"):
                            target_area = frame
                            print(f"SUCCESS: Found login box inside frame: {frame.name or 'unnamed'}")
                            break
                    except:
                        continue

            if not target_area:
                print("STILL CANNOT FIND LOGIN BOX. Saving debug info...")
                page.screenshot(path="not_found_debug.png")
                raise Exception("Could not locate the login input field in any frame.")

            # --- FILLING THE CREDENTIALS ---
            print("Filling credentials...")
            target_area.fill("#login", USERNAME)
            target_area.fill("#password", PASSWORD)
            
            print("Clicking Login button...")
            target_area.click("#loginButton")

            # Wait for the dashboard to load
            page.wait_for_load_state("networkidle")
            time.sleep(5)
            
            print(f"Final URL: {page.url}")
            print(f"Final Page Title: {page.title()}")

            if "login" not in page.url:
                print("LOGIN SUCCESSFUL!")
            else:
                print("LOGIN FAILED: Still on the login page.")
                page.screenshot(path="login_failure_state.png")

        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            page.screenshot(path="error_trace_screenshot.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    reserve_court()
