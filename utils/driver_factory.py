"""
WebDriver Factory with support for local and remote (Grid/Moon) execution
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from utils.logger import Logger
from config.config_reader import ConfigReader


class DriverFactory:
    """Factory class for creating WebDriver instances"""
    
    def __init__(self):
        self.logger = Logger.get_logger()
        self.config = ConfigReader()
    
    def create_driver(self, browser: str = None, headless: bool = False):
        """
        Create a WebDriver instance
        
        Args:
            browser: Browser name (chrome, firefox, edge)
            headless: Run in headless mode
            
        Returns:
            WebDriver instance
        """
        if browser is None:
            browser = self.config.get("browser", "chrome")
        
        grid_url = self.config.get("grid_url")
        
        if grid_url:
            return self._create_remote_driver(browser, headless, grid_url)
        else:
            return self._create_local_driver(browser, headless)
    
    def _create_local_driver(self, browser: str, headless: bool):
        """Create local WebDriver"""
        self.logger.info(f"Creating local {browser} driver (headless={headless})")
        
        if browser.lower() == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--start-maximized")
            driver = webdriver.Chrome(options=options)
        
        elif browser.lower() == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
        
        elif browser.lower() == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--start-maximized")
            driver = webdriver.Edge(options=options)
        
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        driver.maximize_window()
        driver.implicitly_wait(10)
        
        return driver
    
    def _create_remote_driver(self, browser: str, headless: bool, grid_url: str):
        """Create remote WebDriver for Selenium Grid or Moon"""
        self.logger.info(f"Creating remote {browser} driver at {grid_url} (headless={headless})")
        
        if browser.lower() == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        
        elif browser.lower() == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
        
        elif browser.lower() == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless")
        
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        # Add capabilities for grid
        browser_version = self.config.get("browser_version", "latest")
        platform_name = self.config.get("platform", "ANY")
        
        options.set_capability("browserVersion", browser_version)
        options.set_capability("platformName", platform_name)
        
        driver = webdriver.Remote(
            command_executor=grid_url,
            options=options
        )
        
        driver.maximize_window()
        driver.implicitly_wait(10)
        
        return driver
