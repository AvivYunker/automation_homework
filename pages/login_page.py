"""
Login Page Object
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for eBay login page"""
    
    # Locators with fallback options
    SIGN_IN_LINK = [
        (By.XPATH, "//a[contains(text(), 'Sign in')]"),
        (By.LINK_TEXT, "Sign in"),
        (By.XPATH, "//span[contains(text(), 'Sign in')]/parent::a")
    ]
    
    USERNAME_INPUT = [
        (By.ID, "userid"),
        (By.XPATH, "//input[@type='text' and contains(@placeholder, 'Email')]"),
        (By.XPATH, "//input[@name='userid']")
    ]
    
    PASSWORD_INPUT = [
        (By.ID, "pass"),
        (By.XPATH, "//input[@type='password']"),
        (By.XPATH, "//input[@name='pass']")
    ]
    
    CONTINUE_BUTTON = [
        (By.ID, "signin-continue-btn"),
        (By.XPATH, "//button[contains(text(), 'Continue')]"),
        (By.XPATH, "//button[@type='submit']")
    ]
    
    LOGIN_BUTTON = [
        (By.ID, "sgnBt"),
        (By.XPATH, "//button[@type='submit' and contains(text(), 'Sign in')]"),
        (By.XPATH, "//button[@name='sgnBt']")
    ]
    
    def login(self, username: str, password: str):
        """
        Perform login
        
        Args:
            username: User email
            password: User password
        """
        import time
        
        self.logger.info(f"Attempting to login with username: {username}")
        
        # Step 1: Click "Sign in" link on homepage
        self.logger.info("Clicking 'Sign in' link to navigate to login page")
        self.click_with_fallback(self.SIGN_IN_LINK, "Sign In Link")
        time.sleep(2)
        
        # Step 2: Enter username
        self.send_keys_with_fallback(self.USERNAME_INPUT, username, "Username Input")
        time.sleep(1)
        
        # Step 3: Click Continue button (eBay has 2-step login)
        try:
            self.logger.info("Clicking 'Continue' button after entering email")
            self.click_with_fallback(self.CONTINUE_BUTTON, "Continue Button")
            time.sleep(3)  # Wait for password page to load
        except Exception as e:
            self.logger.warning(f"Continue button not found or not needed: {str(e)}")
        
        # Step 4: Enter password
        self.send_keys_with_fallback(self.PASSWORD_INPUT, password, "Password Input")
        time.sleep(1)
        
        # Step 5: Click login button
        self.click_with_fallback(self.LOGIN_BUTTON, "Login Button")
        time.sleep(3)  # Wait for login to complete
        
        self.screenshot.take_screenshot("after_login")
