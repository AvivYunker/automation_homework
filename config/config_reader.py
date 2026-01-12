"""
Configuration Reader - reads settings from config.yaml
"""
import yaml
import os
from typing import Any, Optional


class ConfigReader:
    """Singleton configuration reader"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigReader, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from YAML file"""
        config_file = os.path.join("config", "config.yaml")
        
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
        else:
            # Default configuration if file doesn't exist
            self._config = {
                "browser": "chrome",
                "headless": False,
                "base_url": "https://www.ebay.com",
                "implicit_wait": 10,
                "explicit_wait": 10,
                "grid_url": None,
                "browser_version": "latest",
                "platform": "ANY"
            }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        # Check environment variables first (for overrides)
        env_value = os.getenv(key.upper())
        if env_value is not None:
            return env_value
        
        # Then check config file
        return self._config.get(key, default)
    
    def get_browser_config(self) -> dict:
        """Get browser configuration"""
        return {
            "browser": self.get("browser", "chrome"),
            "headless": self.get("headless", False),
            "browser_version": self.get("browser_version", "latest"),
            "platform": self.get("platform", "ANY")
        }
    
    def get_grid_config(self) -> Optional[str]:
        """Get Selenium Grid / Moon URL"""
        return self.get("grid_url")
    
    def get_timeouts(self) -> dict:
        """Get timeout configurations"""
        return {
            "implicit_wait": self.get("implicit_wait", 10),
            "explicit_wait": self.get("explicit_wait", 10),
            "page_load_timeout": self.get("page_load_timeout", 30)
        }
    
    def reload(self):
        """Reload configuration from file"""
        self._load_config()
