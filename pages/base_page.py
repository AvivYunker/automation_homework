"""
Base Page class with smart locator fallback mechanism
"""
from typing import List, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.logger import Logger
from utils.screenshot_helper import ScreenshotHelper


class BasePage:
    """Base class for all page objects with smart locator handling"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = Logger.get_logger()
        self.screenshot = ScreenshotHelper(driver)
    
    def find_element_with_fallback(self, locators: List[Tuple[str, str]], element_name: str = "Element") -> WebElement:
        """
        Attempts to find an element using multiple fallback locators
        
        Args:
            locators: List of tuples (By.TYPE, "locator_value")
            element_name: Name of the element for logging
            
        Returns:
            WebElement if found
            
        Raises:
            NoSuchElementException if all locators fail
        """
        for i, (by, value) in enumerate(locators, 1):
            try:
                self.logger.info(f"Attempting to find '{element_name}' using locator {i}/{len(locators)}: {by}='{value}'")
                element = self.wait.until(EC.presence_of_element_located((by, value)))
                self.logger.info(f"Successfully found '{element_name}' using locator {i}")
                return element
            except TimeoutException:
                self.logger.warning(f"Locator {i}/{len(locators)} failed for '{element_name}': {by}='{value}'")
                if i == len(locators):
                    self.logger.error(f"All {len(locators)} locators failed for '{element_name}'")
                    self.screenshot.take_screenshot(f"locator_failure_{element_name}")
                    raise NoSuchElementException(f"Could not find '{element_name}' with any of the {len(locators)} locators")
    
    def find_elements_with_fallback(self, locators: List[Tuple[str, str]], element_name: str = "Elements") -> List[WebElement]:
        """Find multiple elements with fallback mechanism"""
        for i, (by, value) in enumerate(locators, 1):
            try:
                self.logger.info(f"Attempting to find '{element_name}' using locator {i}/{len(locators)}")
                elements = self.driver.find_elements(by, value)
                if elements:
                    self.logger.info(f"Successfully found {len(elements)} '{element_name}' using locator {i}")
                    return elements
                else:
                    self.logger.warning(f"Locator {i} returned 0 elements")
            except Exception as e:
                self.logger.warning(f"Locator {i}/{len(locators)} failed: {str(e)}")
        
        self.logger.error(f"All locators failed for '{element_name}'")
        return []
    
    def click_with_fallback(self, locators: List[Tuple[str, str]], element_name: str = "Element"):
        """Click an element with fallback locators"""
        element = self.find_element_with_fallback(locators, element_name)
        element.click()
        self.logger.info(f"Clicked on '{element_name}'")
    
    def send_keys_with_fallback(self, locators: List[Tuple[str, str]], text: str, element_name: str = "Input"):
        """Send keys to an element with fallback locators"""
        element = self.find_element_with_fallback(locators, element_name)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"Sent keys to '{element_name}': {text}")
    
    def get_text_with_fallback(self, locators: List[Tuple[str, str]], element_name: str = "Element") -> str:
        """Get text from an element with fallback locators"""
        element = self.find_element_with_fallback(locators, element_name)
        text = element.text
        self.logger.info(f"Got text from '{element_name}': {text}")
        return text