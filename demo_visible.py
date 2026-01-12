"""
Demo script to show browser navigation with visible browser window.
"""

from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
import time

def demo_navigation():
    """Demonstrate browser navigation with visible browser."""
    print("\n" + "="*60)
    print("Starting Browser Demo - Visible Mode")
    print("="*60 + "\n")
    
    with sync_playwright() as p:
        # Launch browser in visible mode (headless=False)
        print("1. Launching Chrome browser...")
        browser = p.chromium.launch(
            headless=False,
            slow_mo=1000  # Slow down actions by 1000ms to see them better
        )
        
        print("2. Opening new page...")
        page = browser.new_page()
        
        print("3. Initializing LoginPage...")
        login_page = LoginPage(page)
        
        print(f"4. Navigating to: {login_page.LOGIN_URL}")
        print("   (Note: eBay may show CAPTCHA for bot detection)")
        
        try:
            # Navigate to the login page
            login_page.navigate()
            
            print(f"✓ Successfully navigated to: {page.url}")
            print("\n5. Keeping browser open for 5 seconds so you can see it...")
            time.sleep(5)
            
        except Exception as e:
            print(f"⚠ Navigation encountered: {type(e).__name__}")
            print(f"  Current URL: {page.url}")
            print("  (This is expected if eBay shows CAPTCHA)")
            print("\n5. Keeping browser open for 5 seconds so you can see the page...")
            time.sleep(5)
        
        finally:
            print("6. Closing browser...")
            browser.close()
            print("\n✓ Demo completed!")

if __name__ == "__main__":
    demo_navigation()
