"""
Search Page Object
"""
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
import time


class SearchPage(BasePage):
    """Page object for eBay search functionality"""
    
    # Locators
    SEARCH_INPUT = [
        (By.ID, "gh-ac"),
        (By.XPATH, "//input[@type='text' and @aria-label='Search for anything']")
    ]
    
    SEARCH_BUTTON = [
        (By.ID, "gh-btn"),
        (By.XPATH, "//input[@type='submit' and @value='Search']")
    ]
    
    PRICE_MIN_INPUT = [
        (By.XPATH, "//input[@aria-label='Minimum Value in $']"),
        (By.XPATH, "//input[contains(@class, 'x-textrange__input--from')]")
    ]
    
    PRICE_MAX_INPUT = [
        (By.XPATH, "//input[@aria-label='Maximum Value in $']"),
        (By.XPATH, "//input[contains(@class, 'x-textrange__input--to')]")
    ]
    
    PRICE_SUBMIT = [
        (By.XPATH, "//button[contains(@aria-label, 'Submit price range')]"),
        (By.XPATH, "//button[contains(text(), 'Submit')]")
    ]
    
    PRODUCT_ITEMS = [
        (By.XPATH, "//li[contains(@class, 's-item')]//a[@class='s-item__link']"),
        (By.XPATH, "//div[contains(@class, 'srp-results')]//a[contains(@href, '/itm/')]")
    ]
    
    PRODUCT_PRICES = [
        (By.XPATH, "//li[contains(@class, 's-item')]//span[@class='s-item__price']"),
        (By.XPATH, "//span[contains(@class, 's-item__price')]")
    ]
    
    NEXT_PAGE_BUTTON = [
        (By.XPATH, "//a[@type='next']"),
        (By.XPATH, "//a[contains(@class, 'pagination__next')]")
    ]
    
    def search_items(self, query: str):
        """
        Search for items
        
        Args:
            query: Search term
        """
        self.logger.info(f"Searching for: {query}")
        self.send_keys_with_fallback(self.SEARCH_INPUT, query, "Search Input")
        
        # Try to click search button, if it fails, press Enter key
        try:
            self.click_with_fallback(self.SEARCH_BUTTON, "Search Button")
        except Exception as e:
            self.logger.warning(f"Could not click search button: {str(e)}")
            self.logger.info("Pressing Enter key to search instead")
            from selenium.webdriver.common.keys import Keys
            search_input = self.find_element_with_fallback(self.SEARCH_INPUT, "Search Input")
            search_input.send_keys(Keys.RETURN)
        
        time.sleep(3)  # Wait for results to load
        self.screenshot.take_screenshot(f"search_results_{query}")
    
    def apply_price_filter(self, max_price: float):
        """
        Apply price filter if available
        
        Args:
            max_price: Maximum price to filter
        """
        try:
            self.logger.info(f"Applying price filter: max ${max_price}")
            self.send_keys_with_fallback(self.PRICE_MAX_INPUT, str(max_price), "Max Price Input")
            self.click_with_fallback(self.PRICE_SUBMIT, "Price Submit Button")
            time.sleep(2)
            self.screenshot.take_screenshot("price_filter_applied")
        except Exception as e:
            self.logger.warning(f"Could not apply price filter: {str(e)}")
    
    def get_product_items_under_price(self, max_price: float, limit: int = 5) -> List[str]:
        """
        Get product URLs under specified price
        
        Args:
            max_price: Maximum price
            limit: Number of items to collect
            
        Returns:
            List of product URLs
        """
        self.logger.info(f"Collecting up to {limit} items under ${max_price}")
        collected_urls = []
        page_num = 1
        
        while len(collected_urls) < limit:
            self.logger.info(f"Processing page {page_num}")
            
            # Get all product elements
            product_elements = self.find_elements_with_fallback(self.PRODUCT_ITEMS, "Product Items")
            price_elements = self.find_elements_with_fallback(self.PRODUCT_PRICES, "Product Prices")
            
            if not product_elements:
                self.logger.warning("No products found on this page")
                break
            
            # Process each product
            for i, (product, price_elem) in enumerate(zip(product_elements, price_elements)):
                if len(collected_urls) >= limit:
                    break
                
                try:
                    # Parse price
                    price_text = price_elem.text.replace('$', '').replace(',', '')
                    # Handle price ranges (take the first price)
                    if 'to' in price_text.lower():
                        price_text = price_text.split('to')[0].strip()
                    
                    price = float(price_text)
                    
                    if price <= max_price:
                        url = product.get_attribute('href')
                        collected_urls.append(url)
                        self.logger.info(f"Found item {len(collected_urls)}/{limit}: ${price} - {url}")
                except (ValueError, AttributeError) as e:
                    self.logger.warning(f"Could not parse price for item {i}: {str(e)}")
                    continue
            
            # Check if we need more items and if next page exists
            if len(collected_urls) < limit:
                try:
                    next_button = self.find_element_with_fallback(self.NEXT_PAGE_BUTTON, "Next Page Button")
                    next_button.click()
                    time.sleep(2)
                    page_num += 1
                except Exception:
                    self.logger.info("No more pages available")
                    break
            else:
                break
        
        self.logger.info(f"Collected {len(collected_urls)} items total")
        return collected_urls
