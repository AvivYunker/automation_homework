"""
Pytest configuration and fixtures
"""
import pytest
import json
import os
from utils.driver_factory import DriverFactory
from utils.logger import Logger


@pytest.fixture(scope="function")
def driver(request):
    """
    WebDriver fixture with setup and teardown
    
    Provides a WebDriver instance for each test
    Supports parallel execution (each test gets isolated driver)
    """
    logger = Logger.get_logger()
    logger.info("=" * 80)
    logger.info(f"Starting test: {request.node.name}")
    logger.info("=" * 80)
    
    # Create driver
    factory = DriverFactory()
    driver_instance = factory.create_driver()
    
    # Provide driver to test
    yield driver_instance
    
    # Teardown
    logger.info("=" * 80)
    logger.info(f"Finishing test: {request.node.name}")
    logger.info("=" * 80)
    
    try:
        driver_instance.quit()
        logger.info("Driver closed successfully")
    except Exception as e:
        logger.error(f"Error closing driver: {str(e)}")


@pytest.fixture(scope="session")
def test_data():
    """
    Test data fixture - loads data from JSON file
    
    Implements Data-Driven testing requirement from PDF
    """
    logger = Logger.get_logger()
    
    # Try to load test data from JSON file
    data_file = os.path.join("data", "test_data.json")
    
    if os.path.exists(data_file):
        logger.info(f"Loading test data from: {data_file}")
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Test data loaded: {data}")
        return data
    else:
        # Default test data if file doesn't exist
        logger.warning(f"Test data file not found: {data_file}. Using defaults.")
        default_data = {
            "base_url": "https://www.ebay.com",
            "search_query": "shoes",
            "max_price": 220,
            "item_limit": 5
        }
        return default_data


@pytest.fixture(scope="function")
def search_page(driver):
    """Search page fixture"""
    from pages.search_page import SearchPage
    return SearchPage(driver)


@pytest.fixture(scope="function")
def product_page(driver):
    """Product page fixture"""
    from pages.product_page import ProductPage
    return ProductPage(driver)


@pytest.fixture(scope="function")
def cart_page(driver):
    """Cart page fixture"""
    from pages.cart_page import CartPage
    return CartPage(driver)


@pytest.fixture(scope="function")
def login_page(driver):
    """Login page fixture"""
    from pages.login_page import LoginPage
    return LoginPage(driver)


def pytest_configure(config):
    """Pytest configuration hook"""
    # Create necessary directories
    os.makedirs("reports", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)


def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "eBay Automation Test Report"
