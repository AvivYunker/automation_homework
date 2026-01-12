"""
Inspect the eBay login page to find the actual button attributes.
"""

from playwright.sync_api import sync_playwright

def inspect_page():
    """Inspect what elements are on the eBay login page."""
    print("\n" + "="*60)
    print("INSPECTING: eBay Login Page Elements")
    print("="*60 + "\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            print("1. Navigating to eBay login page...")
            page.goto("https://signin.ebay.com/", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)
            
            print("\n2. Finding and filling email field...")
            email_field = page.locator("//label[text()=\"Email or username\"]/..//input")
            email_field.wait_for(state="visible", timeout=10000)
            email_field.fill("test@example.com")
            print("   ✓ Email field filled")
            
            page.wait_for_timeout(1000)
            
            print("\n3. Looking for ALL buttons on the page...")
            buttons = page.locator("button").all()
            print(f"   Found {len(buttons)} button(s)")
            
            for i, button in enumerate(buttons, 1):
                print(f"\n   Button #{i}:")
                try:
                    print(f"      Text: {button.inner_text()}")
                except:
                    print(f"      Text: (no text)")
                
                try:
                    btn_id = button.get_attribute("id")
                    print(f"      ID: {btn_id if btn_id else '(no id)'}")
                except:
                    pass
                
                try:
                    btn_type = button.get_attribute("type")
                    print(f"      Type: {btn_type if btn_type else '(no type)'}")
                except:
                    pass
                
                try:
                    btn_class = button.get_attribute("class")
                    print(f"      Class: {btn_class if btn_class else '(no class)'}")
                except:
                    pass
            
            print("\n\n4. Keeping browser open for 15 seconds for you to inspect...")
            print("   Look at the Continue button and note its attributes!")
            page.wait_for_timeout(15000)
        
        finally:
            print("\nClosing browser...")
            browser.close()

if __name__ == "__main__":
    inspect_page()
