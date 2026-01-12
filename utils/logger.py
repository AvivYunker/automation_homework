"""
Logger utility for consistent logging across the framework
"""
import logging
import os
from datetime import datetime


class Logger:
    """Singleton logger class"""
    
    _logger = None
    
    @staticmethod
    def get_logger(name: str = "AutomationFramework"):
        """
        Get or create logger instance
        
        Args:
            name: Logger name
            
        Returns:
            Logger instance
        """
        if Logger._logger is None:
            Logger._logger = logging.getLogger(name)
            Logger._logger.setLevel(logging.DEBUG)
            
            # Create logs directory if it doesn't exist
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)
            
            # Create file handler with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = os.path.join(log_dir, f"test_run_{timestamp}.log")
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            
            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Add handlers
            Logger._logger.addHandler(file_handler)
            Logger._logger.addHandler(console_handler)
        
        return Logger._logger
