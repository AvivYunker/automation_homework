"""
Cart Page Object
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page object for eBay cart page"""
    
    # Locators
    CART_ICON = [
        (By.ID, "gh-cart"),
        (By.XPATH, "//a[@title='Your shopping cart']"),
        (By.XPATH, "//a[contains(@href, '/sh/sc')]")
    ]
    
    SUBTOTAL = [
        (By.XPATH, "//span[@class='total-price']"),
        (By.XPATH, "//div[contains(@class, 'subtotal')]//span[contains(@class, 'price')]"),
        (By.XPATH, "//div[@data-test-id='SUBTOTAL']//span[contains(text(), '$')]")
    ]
    
    CART_ITEMS = [
        (By.XPATH, "//div[@data-test-id='cart-item']"),
        (By.XPATH, "//div[contains(@class, 'cart-item')]")
    ]
    
    def open_cart(self):
        """
        Navigate to cart page
        """
        self.logger.info("Opening cart...")
        self.click_with_fallback(self.CART_ICON, "Cart Icon")
        self.screenshot.take_screenshot("cart_opened")
    
    def get_cart_total(self) -> float:
        """
        Get the cart subtotal
        
        Returns:
            Cart total as float
        """
        self.logger.info("Getting cart total...")
        total_text = self.get_text_with_fallback(self.SUBTOTAL, "Cart Subtotal")
        
        # Parse the price
        total_text = total_text.replace('$', '').replace(',', '').replace('US', '').strip()
        # Handle cases like "Total: $123.45"
        if ':' in total_text:
            total_text = total_text.split(':')[-1].strip()
        
        try:
            total = float(total_text)
            self.logger.info(f"Cart total: ${total}")
            return total
        except ValueError as e:
            self.logger.error(f"Could not parse cart total from: {total_text}")
            raise ValueError(f"Invalid cart total format: {total_text}")
    
    def get_cart_items_count(self) -> int:
        """
        Get number of items in cart
        
        Returns:
            Number of items
        """
        items = self.find_elements_with_fallback(self.CART_ITEMS, "Cart Items")
        count = len(items)
        self.logger.info(f"Cart contains {count} items")
        return count
