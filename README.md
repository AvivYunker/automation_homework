# eBay Automation Testing Framework

## Project Overview
This is a comprehensive automation testing framework for eBay, implementing the Page Object Model (POM) design pattern with Playwright. The framework automates user login, profile validation, product search, and shopping cart operations.

## Features

### Core Functionality
- **User Authentication**: Automated login with email and password
- **CAPTCHA Handling**: Automatic detection and manual solving support (20-second wait)
- **Profile Validation**: Email verification on profile page
- **Product Search**: Search for items (e.g., chairs) with smart waiting
- **Shopping Cart**: Add multiple random items to cart
- **Smart Locators**: Multiple fallback locator strategies for reliability
- **Optimized Performance**: Fast execution with minimal wait times

### Key Capabilities
- ✅ Two-step login process (email → continue → password)
- ✅ "Skip for now" popup handling
- ✅ Random item selection from search results
- ✅ Add 5 items to shopping cart automatically
- ✅ Browser window maximization
- ✅ Screenshot capture on errors
- ✅ Comprehensive logging

## Project Structure

```
automation_homework/
├── pages/                  # Page Object Model classes
│   ├── base_page.py       # Base page with common methods
│   ├── login_page.py      # eBay login and shopping functionality
│   └── __init__.py
├── tests/                 # Test files
│   ├── test_smoke.py      # Smoke tests
│   └── __init__.py
├── config/                # Configuration files
├── data/                  # Test data
├── logs/                  # Execution logs
├── screenshots/           # Error screenshots
├── reports/               # Test reports
├── .env                   # Environment variables (credentials)
├── .gitignore            # Git ignore file
├── requirements.txt       # Python dependencies
├── demo_login.py         # Demo script for full flow
└── README.md             # This file
```

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd automation_homework
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

5. **Configure credentials**
   Create a `.env` file in the root directory:
   ```
   EBAY_USERNAME=your_email@example.com
   EBAY_PASSWORD=your_password
   ```

## Usage

### Run Demo Script
The main demo script performs the complete automation flow:

```bash
python demo_login.py
```

**What it does:**
1. Logs into eBay with credentials from `.env`
2. Handles CAPTCHA challenges (20-second wait for manual solving)
3. Clicks "Skip for now" if prompted
4. Searches for "chair" items
5. Randomly selects and adds 5 chairs to shopping cart
6. Opens shopping cart to display all items

### Run Tests
Execute the smoke test suite:

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_smoke.py -v
```

## Configuration

### Environment Variables (.env)
- `EBAY_USERNAME`: eBay account email
- `EBAY_PASSWORD`: eBay account password

### Browser Settings
- Default browser: Chromium (maximized window)
- Viewport: 1920x1080
- Headless mode: False (visible browser)
- Slow motion: 500ms (for demonstration)

## Design Patterns & Best Practices

### Page Object Model (POM)
The framework implements POM with:
- **BasePage**: Common functionality (navigation, element finding, screenshots)
- **LoginPage**: eBay-specific operations (login, search, cart)

### Smart Locator Strategy
Multiple locator strategies for each element:
1. Primary locator (most reliable)
2. Fallback locators (alternative methods)
3. Automatic retry on failure

### Error Handling
- Try-catch blocks for resilience
- Screenshot capture on failures
- Detailed logging for debugging
- Multiple fallback strategies

### Performance Optimization
- Smart waits using `wait_for_load_state`
- Minimal fixed timeouts (200-500ms)
- Parallel operations where possible
- Efficient page navigation

## Key Components

### BasePage (pages/base_page.py)
Core functionality:
- `find_element()`: Smart element finding with multiple locators
- `click_element()`: Click with retry logic
- `fill_element()`: Input field filling
- `navigate_to()`: Page navigation
- `take_screenshot()`: Error screenshots

### LoginPage (pages/login_page.py)
eBay-specific operations:
- `login()`: Complete login flow
- `search_for_item()`: Product search
- `click_random_search_result()`: Random item selection
- `add_to_cart()`: Add item to cart
- `add_multiple_items_to_cart()`: Bulk cart operations
- `open_shopping_cart()`: View cart
- `is_captcha_present()`: CAPTCHA detection
- `wait_for_captcha_solution()`: Manual CAPTCHA handling

## Troubleshooting

### Common Issues

**1. CAPTCHA Challenges**
- The automation detects CAPTCHA and waits 20 seconds
- Manually solve the CAPTCHA in the browser window
- The automation continues automatically

**2. Add to Cart Fails**
- Multiple fallback locators are tried automatically
- Some items may not have "Add to cart" (e.g., auctions)
- Check screenshots folder for error details

**3. Login Issues**
- Verify credentials in `.env` file
- Check for eBay account restrictions
- Ensure 2FA is not enabled

**4. Slow Execution**
- All waits are optimized (200-500ms)
- Using `wait_for_load_state` for smart waiting
- Network speed may affect performance

## Testing Strategy

### Test Coverage
- Login functionality
- Page object initialization
- Navigation between pages
- Element interaction
- Error handling

### Test Execution
```bash
# Run all tests
pytest tests/

# Run with HTML report
pytest tests/ --html=reports/report.html

# Run with parallel execution
pytest tests/ -n auto
```

## Dependencies

### Core
- `playwright` - Browser automation
- `pytest` - Testing framework
- `python-dotenv` - Environment variable management

### Additional
- `allure-pytest` - Advanced reporting
- `pytest-html` - HTML reports
- `colorlog` - Colored logging

See `requirements.txt` for complete list.

## Security Notes

- ⚠️ Never commit `.env` file with real credentials
- ⚠️ `.env` is in `.gitignore` by default
- ⚠️ Use test accounts for automation
- ⚠️ Be aware of eBay's Terms of Service regarding automation

## Future Enhancements

- [ ] Support for multiple browsers (Firefox, Safari)
- [ ] Parallel test execution with pytest-xdist
- [ ] API integration for data validation
- [ ] Advanced reporting with Allure
- [ ] CI/CD pipeline integration
- [ ] Database integration for test data
- [ ] Video recording of test execution

## Author

Automation Homework Project

## License

This project is for educational purposes only.
