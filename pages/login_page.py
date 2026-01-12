"""
Login Page Module - Handles eBay authentication.

Provides login functionality with smart locator strategy for all elements.
"""

from pages.base_page import BasePage
from typing import Optional
import logging


class LoginPage(BasePage):
    """
    Page Object for eBay Login Page.
    
    Implements login functionality with multiple locator strategies
    for each element to ensure robustness.
    """
    
    # eBay Login URL
    LOGIN_URL = "https://signin.ebay.com/"
    
    # eBay Profile URL for validation
    PROFILE_URL = "https://accountsettings.ebay.com/profile"
    
    # Main eBay homepage
    MAIN_EBAY_URL = "https://www.ebay.com/"
    
    # Edit button locator (second Edit button on profile page)
    EDIT_BUTTON_LOCATOR = "(//button[text()=\"Edit\"])[2]"
    
    # Username/Email input field locators (multiple strategies)
    USERNAME_LOCATORS = [
        "//label[text()=\"Email or username\"]/..//input",  # XPath by label text
        "#userid",  # CSS ID selector
        "input[type='text']",  # CSS type selector (first text input)
        "input[name='userid']",  # CSS attribute selector
        "input[type='email']",  # CSS email type
        "input[autocomplete='username']",  # CSS autocomplete
        "//input[@id='userid']",  # XPath by ID
        "//input[@name='userid']",  # XPath by name
        "//input[@type='text' or @type='email']",  # XPath by type
        ("css", "input#userid"),  # Tuple format CSS
        ("css", "input[type='text']"),  # Tuple format CSS
    ]
    
    # Password input field locators
    PASSWORD_LOCATORS = [
        "//label[text()=\"Password\"]/..//input",  # XPath by label text
        "#pass",  # CSS ID selector
        "input[type='password']",  # CSS type selector
        "input[name='pass']",  # CSS attribute selector
        "//input[@id='pass']",  # XPath by ID
        "//input[@type='password']",  # XPath by type
        "//input[@name='pass' and @type='password']",  # XPath by name and type
        ("css", "input[type='password']"),  # Tuple format CSS
    ]
    
    # Sign in button locators
    SIGNIN_BUTTON_LOCATORS = [
        "#sgnBt",  # CSS ID selector
        "button[name='sgnBt']",  # CSS attribute selector
        "//button[@id='sgnBt']",  # XPath by ID
        "//button[@name='sgnBt']",  # XPath by name
        "//button[contains(text(), 'Sign in')]",  # XPath by text content
        ("css", "button#sgnBt"),  # Tuple format CSS
    ]
    
    # Continue button (for two-step login if applicable)
    CONTINUE_BUTTON_LOCATORS = [
        "//button[text()=\"Continue\"]",  # XPath by exact text match
        "button[type='submit']",  # Submit button type
        "#signin-continue-btn",  # CSS ID selector
        "button[data-testid='signin-continue-btn']",  # CSS data attribute
        "//button[@id='signin-continue-btn']",  # XPath by ID
        "//button[@type='submit']",  # XPath by type
        "//button[contains(text(), 'Continue')]",  # XPath by text
        "//button[contains(@class, 'signin-continue')]",  # XPath by class
        "button[id*='continue']",  # CSS ID contains continue
        ("css", "button[type='submit']"),  # Tuple format CSS
    ]
    
    # Error message locators
    ERROR_MESSAGE_LOCATORS = [
        "#errMsg",  # CSS ID selector
        ".errMsg",  # CSS class selector
        "//div[@id='errMsg']",  # XPath by ID
        "//div[contains(@class, 'errMsg')]",  # XPath by class
        "//span[contains(@class, 'error')]",  # XPath by error class
    ]
    
    # CAPTCHA detection locators
    CAPTCHA_LOCATORS = [
        "iframe[title*='captcha']",  # CSS iframe with captcha in title
        "iframe[src*='captcha']",  # CSS iframe with captcha in src
        "//iframe[contains(@title, 'captcha')]",  # XPath iframe title
        "//iframe[contains(@src, 'captcha')]",  # XPath iframe src
        "#captcha",  # CSS ID
        ".captcha",  # CSS class
        "//div[contains(@class, 'captcha')]",  # XPath by class
        "[id*='captcha']",  # CSS partial ID match
    ]
    
    # Skip for now link locators (appears after login)
    SKIP_FOR_NOW_LOCATORS = [
        "//a[text()='Skip for now']",  # XPath by exact text
        "a[href*='skip']",  # CSS href contains skip
        "//a[contains(text(), 'Skip for now')]",  # XPath contains text
        "//a[contains(text(), 'skip')]",  # XPath contains skip (case insensitive)
        "button:has-text('Skip for now')",  # Playwright text selector for button
        "a:has-text('Skip for now')",  # Playwright text selector for link
    ]
    
    # Cancel button locators (on profile edit)
    CANCEL_BUTTON_LOCATORS = [
        "//button[text()='Cancel']",  # XPath by exact text
        "button:has-text('Cancel')",  # Playwright text selector
        "//button[contains(text(), 'Cancel')]",  # XPath contains text
        "button[type='button']:has-text('Cancel')",  # Button type with text
    ]
    
    # Search box locators (on main eBay page)
    SEARCH_BOX_LOCATORS = [
        "input[type='text'][placeholder*='Search']",  # CSS input with Search in placeholder
        "#gh-ac",  # CSS ID for eBay search box
        "input[name='_nkw']",  # CSS input by name
        "//input[@id='gh-ac']",  # XPath by ID
        "//input[@type='text' and contains(@placeholder, 'Search')]",  # XPath by type and placeholder
        "//input[@name='_nkw']",  # XPath by name
    ]
    
    # Search button locators
    SEARCH_BUTTON_LOCATORS = [
        "#gh-btn",  # CSS ID for eBay search button
        "input[type='submit'][value*='Search']",  # CSS submit input
        "//input[@id='gh-btn']",  # XPath by ID
        "//button[@type='submit']",  # XPath submit button
        "//input[@type='submit']",  # XPath submit input
    ]
    
    # Add to Cart button locators
    ADD_TO_CART_LOCATORS = [
        "//span[text()='Add to cart']/../..",  # XPath by span text with parent
        "//a[contains(text(), 'Add to cart')]",  # XPath by text
        "a:has-text('Add to cart')",  # Playwright text selector
        "//span[text()='Add to cart']/ancestor::a",  # XPath span with ancestor
        "[data-testid*='cart']",  # CSS data-testid
    ]
    
    # Shopping Cart icon locators
    CART_ICON_LOCATORS = [
        "#gh-cart",  # CSS ID for cart icon
        "a[href*='cart']",  # CSS href contains cart
        "//a[@id='gh-cart']",  # XPath by ID
        "//a[contains(@href, 'cart')]",  # XPath href contains cart
        "a:has-text('cart')",  # Playwright text selector
    ]
    
    # Account switcher / Switch account button locators (if already logged in)
    SWITCH_ACCOUNT_LOCATORS = [
        "a[data-testid='switch-account-link']",
        "//a[contains(text(), 'switch account')]",
        "//a[contains(@href, 'signin')]",
    ]
    
    def __init__(self, page):
        """
        Initialize the Login Page.
        
        Args:
            page: Playwright Page object
        """
        super().__init__(page)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def navigate(self) -> None:
        """Navigate to the eBay login page."""
        self.logger.info("Navigating to eBay login page")
        self.navigate_to(self.LOGIN_URL)
    
    def enter_username(self, username: str) -> None:
        """
        Enter username/email in the login form.
        
        Args:
            username: Username or email address
        """
        self.logger.info(f"Entering username: {username}")
        self.page.wait_for_timeout(200)
        self.fill_element(
            locators=self.USERNAME_LOCATORS,
            text=username,
            element_name="Username Input Field",
            timeout=10000
        )
        self.logger.info(f"✓ Username entered successfully")
    
    def enter_password(self, password: str) -> None:
        """
        Enter password in the login form.
        
        Args:
            password: User password
        """
        self.logger.info("Entering password")
        self.fill_element(
            locators=self.PASSWORD_LOCATORS,
            text=password,
            element_name="Password Input Field",
            timeout=10000
        )
    
    def click_signin_button(self) -> None:
        """Click the Sign In button."""
        self.logger.info("Clicking Sign In button")
        self.click_element(
            locators=self.SIGNIN_BUTTON_LOCATORS,
            element_name="Sign In Button",
            timeout=10000
        )
    
    def click_continue_button(self) -> None:
        """
        Click the Continue button (for two-step login process).
        This is required after entering the username/email.
        """
        self.logger.info("Looking for Continue button...")
        self.page.wait_for_timeout(300)
        
        self.click_element(
            locators=self.CONTINUE_BUTTON_LOCATORS,
            element_name="Continue Button",
            timeout=10000
        )
        
        self.logger.info("Clicked Continue - waiting for password field...")
        self.page.wait_for_timeout(500)
    
    def is_captcha_present(self) -> bool:
        """
        Check if CAPTCHA challenge is present on the page.
        
        Returns:
            True if CAPTCHA detected, False otherwise
        """
        try:
            for locator in self.CAPTCHA_LOCATORS:
                try:
                    element = self.page.locator(locator)
                    if element.count() > 0:
                        self.logger.warning("⚠ CAPTCHA detected on page!")
                        return True
                except:
                    continue
            return False
        except Exception as e:
            self.logger.debug(f"Error checking for CAPTCHA: {str(e)}")
            return False
    
    def wait_for_captcha_solution(self, timeout: int = 60000) -> None:
        """
        Wait for user to manually solve CAPTCHA.
        
        Args:
            timeout: Maximum time to wait in milliseconds (default 60 seconds)
        """
        self.logger.warning("⏳ CAPTCHA DETECTED - Please solve it manually!")
        self.logger.warning(f"⏳ Waiting up to {timeout//1000} seconds for you to solve the CAPTCHA...")
        print("\n" + "="*60)
        print("🤖 CAPTCHA CHALLENGE DETECTED!")
        print("👤 Please solve the CAPTCHA in the browser window")
        print(f"⏳ You have {timeout//1000} seconds")
        print("="*60 + "\n")
        
        # Wait for the specified time
        self.page.wait_for_timeout(timeout)
        self.logger.info("✓ Continuing after CAPTCHA wait period")
    
    def click_skip_for_now_if_present(self) -> bool:
        """
        Check if 'Skip for now' link is present and click it.
        This often appears after login asking for additional verification.
        
        Returns:
            True if link was found and clicked, False otherwise
        """
        try:
            self.logger.info("Checking for 'Skip for now' link...")
            self.page.wait_for_timeout(1000)  # Wait for any popups to appear
            
            for locator in self.SKIP_FOR_NOW_LOCATORS:
                try:
                    element = self.page.locator(locator)
                    if element.count() > 0 and element.first.is_visible():
                        self.logger.info("✓ Found 'Skip for now' link - clicking it")
                        element.first.click()
                        self.page.wait_for_timeout(300)
                        print("\n✓ Clicked 'Skip for now' link\n")
                        return True
                except:
                    continue
            
            self.logger.info("'Skip for now' link not found - continuing")
            return False
        except Exception as e:
            self.logger.debug(f"Error checking for 'Skip for now': {str(e)}")
            return False
    
    def get_error_message(self) -> Optional[str]:
        """
        Get error message if login fails.
        
        Returns:
            Error message text or None if no error present
        """
        try:
            if self.is_element_visible(self.ERROR_MESSAGE_LOCATORS, "Error Message", timeout=3000):
                error_text = self.get_text(
                    locators=self.ERROR_MESSAGE_LOCATORS,
                    element_name="Error Message",
                    timeout=3000
                )
                self.logger.warning(f"Login error detected: {error_text}")
                return error_text
        except Exception:
            self.logger.debug("No error message found")
        return None
    
    def is_login_successful(self) -> bool:
        """
        Check if login was successful by verifying page navigation.
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            # Wait a bit for navigation to complete
            self.page.wait_for_load_state("networkidle", timeout=10000)
            current_url = self.get_current_url()
            
            # If we're no longer on the signin page, login was likely successful
            is_success = "signin" not in current_url.lower()
            
            if is_success:
                self.logger.info("Login successful - redirected away from signin page")
            else:
                self.logger.warning("Login may have failed - still on signin page")
                
            return is_success
        except Exception as e:
            self.logger.error(f"Error checking login status: {str(e)}")
            return False
    
    def navigate_to_profile(self) -> None:
        """
        Navigate to the eBay profile page.
        """
        self.logger.info(f"Navigating to profile page: {self.PROFILE_URL}")
        self.page.goto(self.PROFILE_URL, wait_until="domcontentloaded")
        self.page.wait_for_timeout(500)
    
    def click_edit_button(self) -> None:
        """
        Click the Edit button on the profile page to reveal the full email.
        """
        self.logger.info("Clicking Edit button to reveal email...")
        self.click_element(
            locators=[self.EDIT_BUTTON_LOCATOR],
            element_name="Edit Button",
            timeout=10000
        )
        self.page.wait_for_timeout(300)
    
    def click_cancel_button(self) -> None:
        """
        Click the Cancel button on the profile edit page.
        """
        self.logger.info("Clicking Cancel button to exit edit mode...")
        self.click_element(
            locators=self.CANCEL_BUTTON_LOCATORS,
            element_name="Cancel Button",
            timeout=10000
        )
        self.page.wait_for_timeout(300)
    
    def navigate_to_main_ebay(self) -> None:
        """
        Navigate to the main eBay homepage.
        """
        self.logger.info(f"Navigating to main eBay page: {self.MAIN_EBAY_URL}")
        self.page.goto(self.MAIN_EBAY_URL, wait_until="domcontentloaded")
        self.page.wait_for_timeout(300)
        print("\n✓ Returned to main eBay page\n")
    
    def search_for_item(self, search_term: str) -> bool:
        """
        Search for an item on eBay.
        
        Args:
            search_term: The item to search for (e.g., "laptop")
            
        Returns:
            True if search was successful, False otherwise
        """
        try:
            self.logger.info(f"Searching for: {search_term}")
            print(f"\n🔍 Searching for: {search_term}\n")
            
            # Find and fill the search box
            self.fill_element(
                locators=self.SEARCH_BOX_LOCATORS,
                text=search_term,
                element_name="Search Box",
                timeout=10000
            )
            
            # Small wait before clicking search button
            self.page.wait_for_timeout(200)
            
            self.logger.info("Search term entered, clicking search button...")
            
            # Click the search button
            self.click_element(
                locators=self.SEARCH_BUTTON_LOCATORS,
                element_name="Search Button",
                timeout=10000
            )
            
            # Wait for search results to load using load state
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(500)
            self.logger.info("✓ Search executed successfully")
            
            return True
        except Exception as e:
            self.logger.error(f"✗ Search failed: {str(e)}")
            return False
    
    def get_search_results_summary(self) -> None:
        """
        Display a summary of search results.
        """
        try:
            current_url = self.get_current_url()
            page_title = self.page.title()
            
            self.logger.info(f"Search results page loaded: {page_title}")
            
            print("\n" + "="*60)
            print("🔍 SEARCH RESULTS")
            print("="*60)
            print(f"Page Title: {page_title}")
            print(f"Current URL: {current_url}")
            
            # Try to get the number of results
            try:
                results_locators = [
                    ".srp-controls__count-heading",  # CSS class for results count
                    "//h1[contains(@class, 'srp-controls__count-heading')]",  # XPath
                    "h1.srp-controls__count-heading",
                ]
                
                for locator in results_locators:
                    try:
                        results_element = self.page.locator(locator)
                        if results_element.count() > 0:
                            results_text = results_element.first.inner_text()
                            print(f"Results: {results_text}")
                            break
                    except:
                        continue
            except:
                pass
            
            # Try to count visible items
            try:
                item_locators = [
                    ".s-item",  # CSS class for search items
                    "//div[contains(@class, 's-item')]",
                ]
                
                for locator in item_locators:
                    try:
                        items = self.page.locator(locator).all()
                        if len(items) > 0:
                            print(f"Items visible on page: {len(items)}")
                            break
                    except:
                        continue
            except:
                pass
            
            print("="*60 + "\n")
            
        except Exception as e:
            self.logger.error(f"Error getting search results summary: {str(e)}")
    
    def click_random_search_result(self) -> bool:
        """
        Click on a random item from the search results.
        Uses the locator: //img[@fetchpriority="high"]/..
        
        Returns:
            True if item was clicked successfully, False otherwise
        """
        try:
            import random
            
            # Base locator for items
            base_locator = '//img[@fetchpriority="high"]/..'
            
            self.logger.info("Counting search result items...")
            
            # Get all matching elements
            items = self.page.locator(base_locator).all()
            item_count = len(items)
            
            if item_count == 0:
                self.logger.error("No items found with the specified locator")
                return False
            
            # Select a random item (1-indexed for XPath)
            random_index = random.randint(1, item_count)
            
            self.logger.info(f"Found {item_count} items, selecting item #{random_index}")
            print(f"\n🎲 Found {item_count} items")
            print(f"👆 Randomly selecting item #{random_index}\n")
            
            # Create the indexed locator
            indexed_locator = f"({base_locator})[{random_index}]"
            
            # Click the random item
            self.logger.info(f"Clicking item with locator: {indexed_locator}")
            self.page.locator(indexed_locator).click()
            
            # Wait for navigation using load state instead of timeout
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(500)
            
            # Display the item page info
            item_url = self.get_current_url()
            item_title = self.page.title()
            
            print("\n" + "="*60)
            print("✓ ITEM PAGE LOADED")
            print("="*60)
            print(f"Title: {item_title}")
            print(f"URL: {item_url}")
            print("="*60 + "\n")
            
            self.logger.info(f"✓ Successfully navigated to item: {item_title}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"✗ Failed to click random item: {str(e)}")
            return False
    
    def add_to_cart(self) -> bool:
        """
        Click the 'Add to cart' button on the current item page.
        
        Returns:
            True if successfully added to cart, False otherwise
        """
        try:
            self.logger.info("Looking for 'Add to cart' button...")
            
            # Try multiple strategies quickly
            added = False
            
            # Strategy 1: Primary locator
            try:
                btn = self.page.locator("//span[text()='Add to cart']/../..")
                if btn.count() > 0:
                    btn.first.click()
                    self.page.wait_for_timeout(300)
                    added = True
            except:
                pass
            
            # Strategy 2: Direct text match
            if not added:
                try:
                    btn = self.page.locator("a:has-text('Add to cart')")
                    if btn.count() > 0:
                        btn.first.click()
                        self.page.wait_for_timeout(300)
                        added = True
                except:
                    pass
            
            # Strategy 3: Any link with 'cart' in href
            if not added:
                try:
                    btn = self.page.locator("a[href*='addToCart'], a[href*='cart']")
                    if btn.count() > 0:
                        btn.first.click()
                        self.page.wait_for_timeout(300)
                        added = True
                except:
                    pass
            
            if added:
                self.logger.info("✓ Item added to cart")
                print("✓ Added to cart\n")
                return True
            else:
                self.logger.warning("⚠ Could not find add to cart button, item may not be available")
                return False
            
        except Exception as e:
            self.logger.error(f"✗ Failed to add to cart: {str(e)}")
            return False
    
    def go_back(self) -> None:
        """
        Navigate back to the previous page.
        """
        self.logger.info("Going back to previous page...")
        self.page.go_back(wait_until="domcontentloaded")
        self.page.wait_for_timeout(300)
    
    def add_multiple_items_to_cart(self, count: int = 4) -> int:
        """
        Add multiple random items to cart.
        
        Args:
            count: Number of items to add (default 4)
            
        Returns:
            Number of items successfully added
        """
        added_count = 0
        
        for i in range(count):
            try:
                print(f"\n🛍️ Adding item {i+1}/{count} to cart...")
                
                # Click on a random item
                if self.click_random_search_result():
                    # Add to cart
                    if self.add_to_cart():
                        added_count += 1
                        print(f"✓ Item {i+1}/{count} added successfully")
                    
                    # Go back to search results
                    self.go_back()
                    self.page.wait_for_timeout(200)
                else:
                    self.logger.warning(f"Failed to select item {i+1}")
                    
            except Exception as e:
                self.logger.error(f"Error adding item {i+1}: {str(e)}")
                continue
        
        print(f"\n✓ Successfully added {added_count}/{count} additional items to cart\n")
        return added_count
    
    def open_shopping_cart(self) -> bool:
        """
        Click on the shopping cart icon to view cart.
        
        Returns:
            True if cart opened successfully, False otherwise
        """
        try:
            self.logger.info("Opening shopping cart...")
            print("\n🛒 Opening shopping cart...\n")
            
            self.click_element(
                locators=self.CART_ICON_LOCATORS,
                element_name="Shopping Cart Icon",
                timeout=10000
            )
            
            self.page.wait_for_timeout(1000)
            
            cart_url = self.get_current_url()
            cart_title = self.page.title()
            
            print("\n" + "="*60)
            print("🛒 SHOPPING CART")
            print("="*60)
            print(f"Title: {cart_title}")
            print(f"URL: {cart_url}")
            print("="*60 + "\n")
            
            self.logger.info("✓ Shopping cart opened")
            return True
            
        except Exception as e:
            self.logger.error(f"✗ Failed to open shopping cart: {str(e)}")
            return False
    
    def get_displayed_email(self) -> Optional[str]:
        """
        Get the email address displayed on the profile page after clicking Edit.
        
        Returns:
            Email address or None if not found
        """
        try:
            # Common locators for email display
            email_locators = [
                "input[type='email']",
                "input[name='email']",
                "//input[@type='email']",
                "//input[@name='email']",
                "//input[contains(@id, 'email')]",
            ]
            
            for locator in email_locators:
                try:
                    element = self.page.locator(locator)
                    if element.count() > 0:
                        email = element.first.input_value()
                        if email:
                            self.logger.info(f"Found email: {email}")
                            return email
                except:
                    continue
            
            self.logger.warning("Could not find email field on profile page")
            return None
        except Exception as e:
            self.logger.error(f"Error getting displayed email: {str(e)}")
            return None
    
    def validate_email(self, expected_email: str) -> bool:
        """
        Validate that the displayed email matches the expected email.
        
        Args:
            expected_email: The email from .env file
            
        Returns:
            True if emails match, False otherwise
        """
        try:
            self.navigate_to_profile()
            self.click_edit_button()
            displayed_email = self.get_displayed_email()
            
            if displayed_email:
                if displayed_email.lower() == expected_email.lower():
                    self.logger.info(f"✓ EMAIL VALIDATION SUCCESSFUL: {displayed_email}")
                    print("\n" + "="*60)
                    print("✓ EMAIL VALIDATION PASSED")
                    print(f"Expected: {expected_email}")
                    print(f"Found:    {displayed_email}")
                    print("="*60 + "\n")
                    
                    # Click Cancel to exit edit mode
                    self.click_cancel_button()
                    
                    # Navigate to main eBay page
                    self.navigate_to_main_ebay()
                    
                    return True
                else:
                    self.logger.error(f"✗ EMAIL MISMATCH: Expected '{expected_email}', Found '{displayed_email}'")
                    print("\n" + "="*60)
                    print("✗ EMAIL VALIDATION FAILED")
                    print(f"Expected: {expected_email}")
                    print(f"Found:    {displayed_email}")
                    print("="*60 + "\n")
                    
                    # Click Cancel to exit edit mode even on failure
                    self.click_cancel_button()
                    
                    # Navigate to main eBay page
                    self.navigate_to_main_ebay()
                    
                    return False
            else:
                self.logger.error("✗ Could not retrieve email for validation")
                return False
        except Exception as e:
            self.logger.error(f"✗ Email validation failed with exception: {str(e)}")
            return False
    
    def login(self, username: str, password: str) -> bool:
        """
        Complete login process for eBay.
        
        This is the main function that orchestrates the entire login flow:
        1. Navigate to login page
        2. Enter username
        3. Click continue (if two-step login)
        4. Enter password
        5. Click sign in
        6. Verify login success
        
        Args:
            username: eBay username or email
            password: eBay password
            
        Returns:
            True if login successful, False otherwise
            
        Raises:
            Exception: If login process fails critically
        """
        try:
            self.logger.info(f"Starting login process for user: {username}")
            
            # Step 1: Navigate to login page
            self.navigate()
            
            # Step 2: Enter username/email
            self.enter_username(username)
            
            # Step 2.5: Check for CAPTCHA after entering username
            if self.is_captcha_present():
                self.wait_for_captcha_solution(timeout=20000)
            
            # Step 3: Click Continue button (REQUIRED for eBay two-step login)
            # This makes the password field appear
            self.click_continue_button()
            
            # Step 3.5: Check for CAPTCHA after clicking continue
            if self.is_captcha_present():
                self.wait_for_captcha_solution(timeout=20000)
            
            # Step 4: Enter password (password field is now visible)
            self.enter_password(password)
            
            # Step 5: Click Sign In button
            self.click_signin_button()
            
            # Step 5.5: Check for and click 'Skip for now' link if present
            self.click_skip_for_now_if_present()
            
            # Step 6: Check for errors
            error_message = self.get_error_message()
            if error_message:
                self.logger.error(f"Login failed with error: {error_message}")
                self.take_screenshot("login_error")
                return False
            
            # Step 7: Verify login success
            if self.is_login_successful():
                self.logger.info("✓ Login completed successfully")
                return True
            else:
                self.logger.error("✗ Login failed - verification failed")
                self.take_screenshot("login_failed_verification")
                return False
                
        except Exception as e:
            self.logger.error(f"✗ Login process failed with exception: {str(e)}")
            self.take_screenshot("login_exception")
            raise Exception(f"Login failed: {str(e)}")
