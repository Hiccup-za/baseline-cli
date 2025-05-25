"""
Selenium utility functions for web automation and testing.
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def create_driver(browser_type="chrome", headless=False):
    """
    Create and configure a WebDriver instance.
    
    Args:
        browser_type (str): Type of browser ('chrome', 'firefox', or 'edge')
        headless (bool): Whether to run in headless mode
        
    Returns:
        WebDriver: Configured WebDriver instance
    """
    browser_type = browser_type.lower()
    
    if browser_type == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")  # Updated headless mode syntax
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        
        # Get ChromeDriver path and ensure it's executable
        chromedriver_path = ChromeDriverManager().install()
        if "THIRD_PARTY_NOTICES" in chromedriver_path:
            driver_dir = os.path.dirname(chromedriver_path)
            chromedriver_path = os.path.join(driver_dir, "chromedriver")
        
        # Ensure ChromeDriver is executable
        os.chmod(chromedriver_path, 0o755)
        
        service = ChromeService(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
    
    elif browser_type == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    
    elif browser_type == "edge":
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless")
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
    
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")
    
    # Set common timeouts
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)
    
    return driver


def wait_for_element(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    """
    Wait for an element to be present on the page.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
        selector (str): Element selector
        by (By): Selector type
        timeout (int): Maximum wait time in seconds
        
    Returns:
        WebElement: The found element
        
    Raises:
        TimeoutException: If element not found within timeout
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        return element
    except TimeoutException:
        raise TimeoutException(f"Element not found: {selector} (by {by})")


def take_screenshot(driver, filename, folder=None):
    """
    Take a screenshot and save it to the specified folder.
    
    Args:
        driver: Selenium WebDriver instance
        filename: Name of the screenshot file
        folder: Directory to save the screenshot
        
    Returns:
        str: Path to the saved screenshot
    """
    # Create folder if it doesn't exist
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    
    # Generate full path
    filepath = os.path.join(folder, filename) if folder else filename
    
    # Take screenshot
    driver.save_screenshot(filepath)
    
    return filepath


def scroll_to_element(driver, element):
    """
    Scroll to make an element visible.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
        element (WebElement): Element to scroll to
    """
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    # Add a small delay to allow the page to settle after scrolling
    time.sleep(0.5)


def fill_form(driver, field_mappings):
    """
    Fill in a form using field mappings.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
        field_mappings (dict): Dictionary mapping field selectors to values
    """
    for selector, value in field_mappings.items():
        try:
            field = driver.find_element(By.CSS_SELECTOR, selector)
            field.clear()
            field.send_keys(value)
        except NoSuchElementException:
            print(f"Warning: Field not found: {selector}")


def wait_for_page_load_complete(driver, timeout=30):
    """
    Wait for the page to be fully loaded and rendered.
    Uses multiple indicators to determine when a page is completely loaded.
    
    Args:
        driver: Selenium WebDriver instance
        timeout: Maximum time to wait in seconds
        
    Returns:
        bool: True if page is loaded successfully
        
    Raises:
        TimeoutException: If page doesn't load within timeout
    """
    wait = WebDriverWait(driver, timeout)
    
    # Wait for document ready state
    try:
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
    except TimeoutException:
        raise TimeoutException("Page document.readyState didn't reach 'complete'")
    
    # Wait for jQuery to be loaded and inactive (if present)
    try:
        wait.until(lambda d: d.execute_script(
            'return typeof jQuery !== "undefined" ? jQuery.active === 0 : true'))
    except Exception:
        pass  # jQuery might not be present, which is fine
    
    # Wait for any animations to complete (common libraries)
    try:
        wait.until(lambda d: d.execute_script(
            'return !document.querySelector(".loading, .animating, .spinner, [data-loading]")'))
    except Exception:
        pass  # No loading elements might be present, which is fine
    
    # Additional check for any network requests still in progress
    try:
        wait.until(lambda d: d.execute_script(
            'return window.performance && performance.getEntriesByType("resource").filter(r => !r.responseEnd).length === 0'
        ))
    except Exception:
        pass  # Performance API might not be supported
        
    # Wait a tiny bit for any final rendering
    time.sleep(0.5)
    
    return True 