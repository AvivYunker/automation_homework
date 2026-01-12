"""
Smoke test to verify the project setup and basic page object functionality.
"""

import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.base_page import BasePage
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_import_pages():
    """Test that all page objects can be imported without errors."""
    assert BasePage is not None
    assert LoginPage is not None
    print("✓ All page objects imported successfully")

def test_base_page_initialization():
    """Test that BasePage can be initialized with a Playwright page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Test BasePage initialization
        base_page = BasePage(page)
        assert base_page.page is not None
        assert base_page.logger is not None
        assert base_page.screenshots_dir.exists()
        
        browser.close()
    print("✓ BasePage initialized successfully")

def test_login_page_initialization():
    """Test that LoginPage can be initialized."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Test LoginPage initialization
        login_page = LoginPage(page)
        assert login_page.page is not None
        assert login_page.logger is not None
        assert login_page.LOGIN_URL == "https://signin.ebay.com/"
        
        # Verify locators are defined
        assert len(login_page.USERNAME_LOCATORS) >= 2
        assert len(login_page.PASSWORD_LOCATORS) >= 2
        assert len(login_page.SIGNIN_BUTTON_LOCATORS) >= 2
        
        browser.close()
    print("✓ LoginPage initialized successfully")

def test_login_page_navigation():
    """Test that LoginPage can navigate to eBay login page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        login_page = LoginPage(page)
        login_page.navigate()
        
        # Verify we're on the login page
        assert "signin" in page.url.lower() or "ebay" in page.url.lower()
        
        browser.close()
    print("✓ LoginPage navigation successful")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Running Smoke Tests for Automation Project")
    print("="*60 + "\n")
    
    # Run tests
    pytest.main([__file__, "-v", "-s"])
