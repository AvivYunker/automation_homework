"""
E2E Shopping Test - Based on automation_homework.pdf requirements
"""
import pytest
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


class TestE2EShopping:
    """
    End-to-end shopping test scenario implementing the 4 main functions:
    1. Authentication
    2. searchItemsByNameUnderPrice
    3. addItemsToCart
    4. assertCartTotalNotExceeds
    """
    
    def test_ebay_shopping_flow(self, driver, test_data):
        """
        Complete e2e test: Search items under price, add to cart, validate total
        
        Test Flow:
        1. Navigate to eBay
        2. Search for items under specified price
        3. Add items to cart
        4. Validate cart total doesn't exceed budget
        """
        # Get test data
        search_query = test_data.get("search_query", "shoes")
        max_price = test_data.get("max_price", 220)
        item_limit = test_data.get("item_limit", 5)
        base_url = test_data.get("base_url", "https://www.ebay.com")
        
        # Navigate to eBay
        driver.get(base_url)
        
        # Initialize page objects
        login_page = LoginPage(driver)
        search_page = SearchPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)
        
        # Step 1: Authentication (optional - set login_enabled=true in test_data.json)
        if test_data.get("login_enabled", False):
            username = test_data.get("username")
            password = test_data.get("password")
            if username and password:
                login_page.login(username, password)
            else:
                print("Login enabled but credentials not provided in test_data.json")
        
        # Step 2: searchItemsByNameUnderPrice
        product_urls = self.search_items_by_name_under_price(
            search_page, 
            search_query, 
            max_price, 
            item_limit
        )
        
        # Verify we found items
        assert len(product_urls) > 0, f"No items found under ${max_price}"
        print(f"Found {len(product_urls)} items to add to cart")
        
        # Step 3: addItemsToCart
        self.add_items_to_cart(driver, product_page, product_urls)
        
        # Step 4: assertCartTotalNotExceeds
        self.assert_cart_total_not_exceeds(
            cart_page, 
            max_price, 
            len(product_urls)
        )
    
    def search_items_by_name_under_price(self, search_page: SearchPage, query: str, 
                                         max_price: float, limit: int = 5) -> list:
        """
        Function 2: Search for items by name under specified price
        
        Implements the searchItemsByNameUnderPrice function from the PDF:
        - Searches by query
        - Applies price filter if available
        - Collects up to 'limit' items where price <= maxPrice
        - Handles pagination if needed
        - Returns list of product URLs
        
        Args:
            search_page: SearchPage object
            query: Search term
            max_price: Maximum price
            limit: Number of items to collect (default 5)
            
        Returns:
            List of product URLs (up to limit items)
        """
        # Perform search
        search_page.search_items(query)
        
        # Apply price filter if possible
        search_page.apply_price_filter(max_price)
        
        # Get product URLs under the price limit
        product_urls = search_page.get_product_items_under_price(max_price, limit)
        
        return product_urls
    
    def add_items_to_cart(self, driver, product_page: ProductPage, urls: list):
        """
        Function 3: Add items to cart
        
        Implements the addItemsToCart function from the PDF:
        - Loops through each URL
        - Opens product page
        - Selects random variants if needed (size, color, quantity)
        - Clicks "Add to cart"
        - Returns to search/previous page
        - Takes screenshot/log for each item
        
        Args:
            driver: WebDriver instance
            product_page: ProductPage object
            urls: List of product URLs to add
        """
        for i, url in enumerate(urls, 1):
            try:
                product_page.logger.info(f"Adding item {i}/{len(urls)} to cart: {url}")
                
                # Open product page
                driver.get(url)
                
                # Add to cart (handles variant selection internally)
                product_page.add_to_cart()
                
                # Go back or keep the current state (eBay might redirect to cart)
                # driver.back()  # Optional: uncomment if you want to go back
                
            except Exception as e:
                product_page.logger.error(f"Failed to add item {i} to cart: {str(e)}")
                product_page.screenshot.take_screenshot(f"add_to_cart_failure_item_{i}")
                # Continue with next item instead of failing the test
                continue
    
    def assert_cart_total_not_exceeds(self, cart_page: CartPage, 
                                      budget_per_item: float, items_count: int):
        """
        Function 4: Assert cart total doesn't exceed budget
        
        Implements the assertCartTotalNotExceeds function from the PDF:
        - Opens shopping cart
        - Reads subtotal/total
        - Calculates threshold: budgetPerItem * itemsCount
        - Asserts total <= threshold
        - Takes screenshot of cart page
        
        Args:
            cart_page: CartPage object
            budget_per_item: Budget per item
            items_count: Number of items added
        """
        # Open cart
        cart_page.open_cart()
        
        # Get cart total
        cart_total = cart_page.get_cart_total()
        
        # Calculate threshold
        threshold = budget_per_item * items_count
        
        # Log the comparison
        cart_page.logger.info(f"Cart total: ${cart_total}")
        cart_page.logger.info(f"Threshold: ${threshold} (${budget_per_item} x {items_count} items)")
        
        # Take screenshot before assertion
        cart_page.screenshot.take_screenshot("cart_total_validation")
        
        # Assert
        assert cart_total <= threshold, \
            f"Cart total ${cart_total} exceeds threshold ${threshold} (${budget_per_item} x {items_count})"
        
        cart_page.logger.info(f"✓ Cart total validation passed: ${cart_total} <= ${threshold}")


class TestCartValidation:
    """Additional cart validation tests"""
    
    def test_empty_cart(self, driver, test_data):
        """Test cart behavior when empty"""
        base_url = test_data.get("base_url", "https://www.ebay.com")
        driver.get(base_url)
        
        cart_page = CartPage(driver)
        cart_page.open_cart()
        
        # Verify cart can be opened
        cart_page.screenshot.take_screenshot("empty_cart")
