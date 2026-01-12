"""
Debug script to see exactly what's happening during login.
"""

from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

def debug_login():
    """Debug the login process step by step."""
    print("\n" + "="*60)
    print("DEBUG: eBay Login - Step by Step")
    print("="*60 + "\n")
    
    load_dotenv()
    username = os.getenv("EBAY_USERNAME")
    password = os.getenv("EBAY_PASSWORD")
    
    if not username or not password:
        print("❌ Error: Username or password not found in .env file")
        print("Please ensure .env file exists with EBAY_USERNAME and EBAY_PASSWORD")
        return
    
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password)}\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        
        try:
            # Step 1: Navigate
            print("1. Navigating to eBay login page...")
            page.goto("https://signin.ebay.com/", wait_until="domcontentloaded", timeout=30000)
            print(f"   Current URL: {page.url}\n")
            
            # Step 2: Try to find the email field
            print("2. Looking for email field...")
            
            # Try the specific locator
            locator = "//label[text()=\"Email or username\"]/..//input"
            print(f"   Trying locator: {locator}")
            
            try:
                email_field = page.locator(locator)
                email_field.wait_for(state="visible", timeout=10000)
                print(f"   ✓ Found email field!")
                
                # Step 3: Fill the email
                print(f"\n3. Filling email field with: {username}")
                email_field.fill(username)
                print(f"   ✓ Email entered")
                
                # Step 4: Look for Continue button
                print(f"\n4. Looking for Continue button...")
                continue_locators = [
                    "button[type='submit']",
                    "//button[@type='submit']",
                    "//button[contains(text(), 'Continue')]",
                ]
                
                for loc in continue_locators:
                    try:
                        print(f"   Trying: {loc}")
                        btn = page.locator(loc)
                        btn.wait_for(state="visible", timeout=3000)
                        print(f"   ✓ Found button!")
                        
                        # Click it
                        print(f"\n5. Clicking Continue button...")
                        btn.click()
                        print(f"   ✓ Clicked!")
                        
                        # Wait for password field
                        print(f"\n6. Waiting for password field...")
                        page.wait_for_timeout(3000)
                        print(f"   Current URL: {page.url}")
                        
                        # Try to find password field
                        pwd_locators = ["#pass", "input[type='password']", "//input[@type='password']"]
                        for pwd_loc in pwd_locators:
                            try:
                                pwd = page.locator(pwd_loc)
                                pwd.wait_for(state="visible", timeout=3000)
                                print(f"   ✓ Found password field with: {pwd_loc}")
                                
                                # Fill password
                                print(f"\n7. Filling password...")
                                pwd.fill(password)
                                print(f"   ✓ Password entered")
                                break
                            except:
                                continue
                        
                        break
                    except Exception as e:
                        print(f"   ✗ Failed: {str(e)[:50]}")
                        continue
                
                print(f"\n8. Keeping browser open for 10 seconds...")
                page.wait_for_timeout(10000)
                
            except Exception as e:
                print(f"   ✗ ERROR: {str(e)}")
                print(f"\n   Let me check what's on the page...")
                print(f"   Page title: {page.title()}")
                print(f"   Page URL: {page.url}")
                
                # Try to find any input field
                inputs = page.locator("input").all()
                print(f"   Found {len(inputs)} input fields on the page")
                
                page.wait_for_timeout(10000)
        
        finally:
            print("\nClosing browser...")
            browser.close()

if __name__ == "__main__":
    debug_login()
