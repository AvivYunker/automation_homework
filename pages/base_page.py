"""
Base Page Module - Provides core functionality for all Page Objects.

Implements smart locator strategy with automatic fallback mechanism,
retry logic, comprehensive logging, and screenshot capture on failures.
"""

import logging
from typing import Sequence, Tuple, Optional, Union
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page, Locator, Error as PlaywrightError


class BasePage:
    """
    Base class for all Page Objects implementing smart locator strategy.
    
    Features:
    - Multiple locator support with automatic fallback
    - Configurable retry mechanism
    - Comprehensive logging of locator attempts
    - Screenshot capture on final failure
    - Common page operations (click, fill, wait, etc.)
    """
    
    def __init__(self, page: Page):
        """
        Initialize the base page.
        
        Args:
            page: Playwright Page object
        """
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)
        self.screenshots_dir = Path("screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)
        
    def find_element(
        self,
        locators: Sequence[Union[str, Tuple[str, str]]],
        element_name: str = "Element",
        timeout: int = 10000
    ) -> Locator:
        """
        Find element using multiple locator strategies with automatic fallback.
        
        Args:
            locators: List of locator strings or tuples (strategy, value)
                     e.g., ["#id", "//xpath", ("css", ".class"), ("xpath", "//div")]
            element_name: Name of the element for logging purposes
            timeout: Timeout in milliseconds for each locator attempt
            
        Returns:
            Playwright Locator object if found
            
        Raises:
            Exception: If all locator strategies fail
        """
        self.logger.info(f"Searching for '{element_name}' with {len(locators)} locator(s)")
        
        for attempt, locator in enumerate(locators, 1):
            try:
                self.logger.debug(f"Attempt {attempt}/{len(locators)}: Trying locator '{locator}'")
                
                # Normalize locator to string format
                if isinstance(locator, tuple):
                    strategy, value = locator
                    if strategy == "xpath":
                        locator_str = value if value.startswith("//") or value.startswith("(//") else f"//{value}"
                    elif strategy == "css":
                        locator_str = value
                    elif strategy == "text":
                        locator_str = f"text={value}"
                    elif strategy == "id":
                        locator_str = f"#{value}"
                    else:
                        locator_str = value
                else:
                    locator_str = locator
                
                # Try to find the element
                element = self.page.locator(locator_str)
                element.wait_for(state="visible", timeout=timeout)
                
                self.logger.info(f"✓ SUCCESS: Found '{element_name}' using locator {attempt}: '{locator}'")
                return element
                
            except (PlaywrightError, TimeoutError):
                self.logger.warning(f"✗ FAILED: Locator {attempt}/{len(locators)} timed out for '{element_name}': '{locator}'")
                continue
            except Exception as e:
                self.logger.warning(f"✗ FAILED: Locator {attempt}/{len(locators)} error for '{element_name}': {str(e)}")
                continue
        
        # All locators failed - take screenshot and raise exception
        self.logger.error(f"✗ FINAL FAILURE: All {len(locators)} locators failed for '{element_name}'")
        screenshot_path = self._take_screenshot(f"failed_{element_name}")
        self.logger.error(f"Screenshot saved to: {screenshot_path}")
        
        raise Exception(
            f"Failed to find '{element_name}' after trying {len(locators)} locator strategies. "
            f"Screenshot: {screenshot_path}"
        )
    
    def click_element(
        self,
        locators: Sequence[Union[str, Tuple[str, str]]],
        element_name: str = "Element",
        timeout: int = 10000
    ) -> None:
        """
        Click an element using smart locator strategy.
        
        Args:
            locators: List of locator strategies
            element_name: Name of the element for logging
            timeout: Timeout in milliseconds
        """
        element = self.find_element(locators, element_name, timeout)
        self.logger.info(f"Clicking on '{element_name}'")
        element.click()
        
    def fill_element(
        self,
        locators: Sequence[Union[str, Tuple[str, str]]],
        text: str,
        element_name: str = "Input Field",
        timeout: int = 10000,
        clear_first: bool = True
    ) -> None:
        """
        Fill an input element using smart locator strategy.
        
        Args:
            locators: List of locator strategies
            text: Text to fill
            element_name: Name of the element for logging
            timeout: Timeout in milliseconds
            clear_first: Whether to clear the field before filling
        """
        element = self.find_element(locators, element_name, timeout)
        self.logger.info(f"Filling '{element_name}' with: '{text}'")
        
        if clear_first:
            element.fill("")  # Clear by filling with empty string
        element.fill(text)
        
    def get_text(
        self,
        locators: Sequence[Union[str, Tuple[str, str]]],
        element_name: str = "Element",
        timeout: int = 10000
    ) -> str:
        """
        Get text content from an element using smart locator strategy.
        
        Args:
            locators: List of locator strategies
            element_name: Name of the element for logging
            timeout: Timeout in milliseconds
            
        Returns:
            Text content of the element
        """
        element = self.find_element(locators, element_name, timeout)
        text = element.inner_text()
        self.logger.debug(f"Retrieved text from '{element_name}': '{text}'")
        return text
    
    def get_attribute(
        self,
        locators: Sequence[Union[str, Tuple[str, str]]],
        attribute: str,
        element_name: str = "Element",
        timeout: int = 10000
    ) -> Optional[str]:
        """
        Get attribute value from an element using smart locator strategy.
        
        Args:
            locators: List of locator strategies
            attribute: Attribute name to retrieve
            element_name: Name of the element for logging
            timeout: Timeout in milliseconds
            
        Returns:
            Attribute value or None if not found
        """
        element = self.find_element(locators, element_name, timeout)
        value = element.get_attribute(attribute)
        self.logger.debug(f"Retrieved attribute '{attribute}' from '{element_name}': '{value}'")
        return value
    
    def is_element_visible(
        self,
        locators: Sequence[Union[str, Tuple[str, str]]],
        element_name: str = "Element",
        timeout: int = 5000
    ) -> bool:
        """
        Check if an element is visible using smart locator strategy.
        
        Args:
            locators: List of locator strategies
            element_name: Name of the element for logging
            timeout: Timeout in milliseconds
            
        Returns:
            True if element is visible, False otherwise
        """
        try:
            element = self.find_element(locators, element_name, timeout)
            visible = element.is_visible()
            self.logger.debug(f"Element '{element_name}' visibility: {visible}")
            return visible
        except Exception:
            self.logger.debug(f"Element '{element_name}' not found or not visible")
            return False
    
    def wait_for_element(
        self,
        locators: Sequence[Union[str, Tuple[str, str]]],
        element_name: str = "Element",
        timeout: int = 30000,
        state: str = "visible"
    ) -> Locator:
        """
        Wait for an element to reach a specific state.
        
        Args:
            locators: List of locator strategies
            element_name: Name of the element for logging
            timeout: Timeout in milliseconds
            state: Element state to wait for (visible, hidden, attached, detached)
            
        Returns:
            Playwright Locator object
        """
        self.logger.info(f"Waiting for '{element_name}' to be '{state}'")
        return self.find_element(locators, element_name, timeout)
    
    def wait_for_page_load(self, timeout: int = 30000) -> None:
        """
        Wait for the page to finish loading.
        
        Args:
            timeout: Timeout in milliseconds
        """
        self.logger.info("Waiting for page to load")
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        
    def navigate_to(self, url: str) -> None:
        """
        Navigate to a specific URL.
        
        Args:
            url: URL to navigate to
        """
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_timeout(1000)
        
    def get_current_url(self) -> str:
        """
        Get the current page URL.
        
        Returns:
            Current URL
        """
        url = self.page.url
        self.logger.debug(f"Current URL: {url}")
        return url
    
    def _take_screenshot(self, name: str) -> str:
        """
        Take a screenshot and save it to the screenshots directory.
        
        Args:
            name: Name for the screenshot file
            
        Returns:
            Path to the saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = self.screenshots_dir / filename
        
        self.page.screenshot(path=str(filepath), full_page=True)
        return str(filepath)
    
    def take_screenshot(self, name: str = "screenshot") -> str:
        """
        Public method to take a screenshot.
        
        Args:
            name: Name for the screenshot file
            
        Returns:
            Path to the saved screenshot
        """
        screenshot_path = self._take_screenshot(name)
        self.logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
