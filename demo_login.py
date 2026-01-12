"""
Demo script to test eBay login with credentials from .env file.
"""

from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from dotenv import load_dotenv
import os
import time

def demo_login():
    """Demonstrate eBay login with visible browser."""
    print("\n" + "="*60)
    print("eBay Login Demo - Visible Mode")
    print("="*60 + "\n")
    
    # Load credentials from .env file
    load_dotenv()
    username = os.getenv("EBAY_USERNAME")
    password = os.getenv("EBAY_PASSWORD")
    
    if not username or not password:
        print("❌ Error: Username or password not found in .env file")
        print("Please ensure .env file exists with EBAY_USERNAME and EBAY_PASSWORD")
        return
    
    print(f"📧 Username loaded: {username}")
    print(f"🔑 Password loaded: {'*' * len(password)}")
    print()
    
    with sync_playwright() as p:
        # Launch browser in visible mode
        print("1. Launching Chrome browser...")
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500  # Slow down actions by 500ms to see them
        )
        
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720}
        )
        page = context.new_page()
        
        # Maximize the browser window
        page.set_viewport_size({'width': 1920, 'height': 1080})
        
        try:
            print("2. Initializing LoginPage...")
            login_page = LoginPage(page)
            
            print("3. Starting login process...")
            print(f"   Navigating to: {login_page.LOGIN_URL}")
            
            # Perform login
            success = login_page.login(username, password)
            
            if success:
                print("\n✅ LOGIN SUCCESSFUL!")
                print(f"   Current URL: {page.url}")
                
                # Perform search for chair
                print("\n4. Performing search for 'chair'...")
                if login_page.search_for_item("chair"):
                    print("   ✓ Search completed successfully!")
                    
                    # Display search results summary
                    login_page.get_search_results_summary()
                    
                    # Click on a random item
                    print("5. Selecting first random item from search results...")
                    if login_page.click_random_search_result():
                        print("   ✓ First item selected successfully!")
                        
                        # Add first item to cart
                        print("\n6. Adding first item to cart...")
                        if login_page.add_to_cart():
                            print("   ✓ First item added to cart!")
                            
                            # Go back to search results
                            print("\n7. Going back to search results...")
                            login_page.go_back()
                            print("   ✓ Back to search results")
                            
                            # Add 4 more items
                            print("\n8. Adding 4 additional items to cart...")
                            added = login_page.add_multiple_items_to_cart(4)
                            print(f"   ✓ Added {added}/4 additional items")
                            
                            # Open shopping cart
                            print("\n9. Opening shopping cart...")
                            if login_page.open_shopping_cart():
                                print("   ✓ Shopping cart opened!")
                                print("\n10. Keeping browser open for 30 seconds to view cart...")
                                time.sleep(30)
                            else:
                                print("   ✗ Failed to open cart")
                                time.sleep(10)
                        else:
                            print("   ✗ Failed to add to cart")
                            time.sleep(10)
                    else:
                        print("   ✗ Failed to select random item")
                        print("\n6. Keeping browser open for 10 seconds...")
                        time.sleep(10)
                else:
                    print("   ✗ Search failed")
                    print("\n5. Keeping browser open for 10 seconds...")
                    time.sleep(10)
            else:
                print("\n❌ LOGIN FAILED!")
                print(f"   Current URL: {page.url}")
                print("   Check screenshots folder for error details")
                print("\n4. Keeping browser open for 10 seconds to review the error...")
                time.sleep(10)
                
        except Exception as e:
            print(f"\n❌ ERROR during login: {type(e).__name__}")
            print(f"   Message: {str(e)}")
            print(f"   Current URL: {page.url}")
            print("\n4. Keeping browser open for 10 seconds to review...")
            time.sleep(10)
        
        finally:
            print("11. Closing browser...")
            browser.close()
            print("\n✓ Demo completed!")

if __name__ == "__main__":
    demo_login()
