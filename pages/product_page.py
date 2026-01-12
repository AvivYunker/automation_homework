"""
Product Page Object
"""
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class ProductPage(BasePage):
    """Page object for eBay product page"""
    
    # Locators
    ADD_TO_CART_BUTTON = [
        (By.ID, "isCartBtn_btn"),
        (By.XPATH, "//a[contains(@class, 'ux-call-to-action') and contains(text(), 'Add to cart')]"),
        (By.XPATH, "//button[contains(text(), 'Add to cart')]")
    ]
    
    QUANTITY_SELECT = [
        (By.ID, "qtyTextBox"),
        (By.XPATH, "//select[@aria-label='Quantity']")
    ]
    
    SIZE_SELECT = [
        (By.ID, "msku-sel-1"),
        (By.XPATH, "//select[contains(@aria-label, 'Size')]")
    ]
    
    COLOR_SELECT = [
        (By.XPATH, "//select[contains(@aria-label, 'Color')]"),
        (By.ID, "msku-sel-2")
    ]
    
    VARIANT_BUTTONS = [
        (By.XPATH, "//div[contains(@class, 'msku')]//button[not(@disabled)]"),
        (By.XPATH, "//fieldset//button[not(@disabled)]")
    ]
    
    def select_random_variants(self):
        """
        Select random variants (size, color, etc.) if available
        """
        self.logger.info("Checking for product variants...")
        
        # Try to find and select from dropdown variants
        for select_locators, name in [
            (self.SIZE_SELECT, "Size"),
            (self.COLOR_SELECT, "Color")
        ]:
            try:
                select_element = self.find_element_with_fallback(select_locators, f"{name} Select")
                select = Select(select_element)
                options = [opt for opt in select.options if opt.get_attribute("value")]
                if len(options) > 1:  # Skip if only one option
                    selected = random.choice(options[1:])  # Skip first (usually "Select")
                    select.select_by_value(selected.get_attribute("value"))
                    self.logger.info(f"Selected {name}: {selected.text}")
            except Exception as e:
                self.logger.debug(f"No {name} dropdown or error: {str(e)}")
        
        # Try to find and click variant buttons
        try:
            variant_buttons = self.find_elements_with_fallback(self.VARIANT_BUTTONS, "Variant Buttons")
            if variant_buttons:
                button = random.choice(variant_buttons)
                button.click()
                self.logger.info("Clicked random variant button")
                time.sleep(1)
        except Exception as e:
            self.logger.debug(f"No variant buttons or error: {str(e)}")
    
    def add_to_cart(self):
        """
        Add product to cart
        """
        self.logger.info("Adding product to cart...")
        
        # Select variants if available
        self.select_random_variants()
        
        # Click add to cart
        self.click_with_fallback(self.ADD_TO_CART_BUTTON, "Add to Cart Button")
        time.sleep(2)
        
        self.screenshot.take_screenshot("product_added_to_cart")
        self.logger.info("Product added to cart successfully")
