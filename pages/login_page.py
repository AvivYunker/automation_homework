"""
Login Page Object
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for eBay login page"""
    
    # Locators with fallback options
    USERNAME_INPUT = [
        (By.ID, "userid"),
        (By.XPATH, "//input[@type='text' and contains(@placeholder, 'Email')]")
    ]
    
    PASSWORD_INPUT = [
        (By.ID, "pass"),
        (By.XPATH, "//input[@type='password']")
    ]
    
    LOGIN_BUTTON = [
        (By.ID, "sgnBt"),
        (By.XPATH, "//button[@type='submit' and contains(text(), 'Sign in')]")
    ]
    
    def login(self, username: str, password: str):
        """
        Perform login
        
        Args:
            username: User email
            password: User password
        """
        self.logger.info(f"Attempting to login with username: {username}")
        self.send_keys_with_fallback(self.USERNAME_INPUT, username, "Username Input")
        self.send_keys_with_fallback(self.PASSWORD_INPUT, password, "Password Input")
        self.click_with_fallback(self.LOGIN_BUTTON, "Login Button")
        self.screenshot.take_screenshot("after_login")
