"""
Screenshot helper utility
"""
import os
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from utils.logger import Logger


class ScreenshotHelper:
    """Helper class for taking screenshots"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = Logger.get_logger()
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def take_screenshot(self, name: str):
        """
        Take a screenshot with a given name
        
        Args:
            name: Screenshot name (without extension)
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        try:
            self.driver.save_screenshot(filepath)
            self.logger.info(f"Screenshot saved: {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to save screenshot: {str(e)}")
