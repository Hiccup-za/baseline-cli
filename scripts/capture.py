"""
Script to capture baseline screenshots and element templates.

This tool helps create initial reference images for visual regression testing.
"""
import os
import sys
import time
import argparse
from PIL import Image
from selenium.webdriver.common.by import By

# Add project root to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.web_utils import create_driver, take_screenshot
from config.config import TARGET_URL, BASELINE_DIR, HEADLESS


def capture_full_page_baseline(url, name, driver=None, should_quit=True):
    """
    Capture a full page screenshot as a baseline.
    
    Args:
        url (str): URL to navigate to
        name (str): Name to use for the baseline image
        driver (WebDriver, optional): Existing driver to use
        should_quit (bool): Whether to quit the driver when done
    
    Returns:
        str: Path to the saved baseline image
    """
    if driver is None:
        driver = create_driver(headless=HEADLESS)
    start_time = time.time()
    output_path = None
    try:
        print(f"🧭 Visiting {url}...")
        driver.get(url)
        time.sleep(3)
        print("🖼️  Capturing screenshot...")
        filename = f"{name}_baseline.png"
        baseline_path = take_screenshot(driver, filename=filename, folder=BASELINE_DIR)
        output_path = baseline_path
        print("🛠️  Compiling results...")
        duration = time.time() - start_time
        return "✅ Success", baseline_path, duration
    except KeyboardInterrupt:
        duration = time.time() - start_time
        print("\nCapture cancelled by user.")
        return "🚫 Cancelled", output_path, duration
    except Exception as e:
        duration = time.time() - start_time
        print(f"🚨 Error capturing baseline: {str(e)}")
        return "🚨 Error", output_path, duration
    finally:
        if should_quit:
            driver.quit()


def capture_element_template(url, element_selector, name, selector_type=By.CSS_SELECTOR, driver=None, should_quit=True):
    """
    Capture a screenshot of a specific element to use as a template.
    
    Args:
        url (str): URL to navigate to
        element_selector (str): Selector to locate the element
        name (str): Name to use for the template image
        selector_type (By): Type of selector to use
        driver (WebDriver, optional): Existing driver to use
        should_quit (bool): Whether to quit the driver when done
    
    Returns:
        str: Path to the saved template image
    """
    if driver is None:
        driver = create_driver(headless=HEADLESS)
    start_time = time.time()
    output_path = None
    try:
        print(f"🧭 Visiting {url}...")
        driver.get(url)
        time.sleep(3)
        print("🖼️  Capturing element screenshot...")
        element = driver.find_element(selector_type, element_selector)
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)
        location = element.location
        size = element.size
        temp_screenshot = os.path.join(BASELINE_DIR, "temp_screenshot.png")
        driver.save_screenshot(temp_screenshot)
        full_img = Image.open(temp_screenshot)
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        device_pixel_ratio = driver.execute_script("return window.devicePixelRatio;")
        if device_pixel_ratio and device_pixel_ratio > 1:
            left *= device_pixel_ratio
            top *= device_pixel_ratio
            right *= device_pixel_ratio
            bottom *= device_pixel_ratio
        elem_img = full_img.crop((left, top, right, bottom))
        template_path = os.path.join(BASELINE_DIR, f"{name}_template.png")
        elem_img.save(template_path)
        os.remove(temp_screenshot)
        output_path = template_path
        print("🛠️  Compiling results...")
        duration = time.time() - start_time
        return "✅ Success", template_path, duration
    except KeyboardInterrupt:
        duration = time.time() - start_time
        print("\nCapture cancelled by user.")
        return "🚫 Cancelled", output_path, duration
    except Exception as e:
        duration = time.time() - start_time
        print(f"🚨 Error capturing element template: {str(e)}")
        return "🚨 Error", output_path, duration
    finally:
        if should_quit:
            driver.quit()


def main():
    """Run the baseline capture tool."""
    parser = argparse.ArgumentParser(description="Capture baseline screenshots and templates")
    parser.add_argument("--url", type=str, default=TARGET_URL, help="URL to navigate to")
    parser.add_argument("--page", action="store_true", help="Capture full page screenshot")
    parser.add_argument("--element", action="store_true", help="Capture element template")
    parser.add_argument("--name", type=str, required=True, help="Name for the baseline/template")
    parser.add_argument("--selector", type=str, help="CSS selector for the element (required for --element)")
    args = parser.parse_args()
    os.makedirs(BASELINE_DIR, exist_ok=True)
    print("\n--- Baseline Capture ---\n")
    if args.page and args.element:
        print("Please choose either --page or --element, not both.")
        sys.exit(1)
    if args.element and not args.selector:
        print("--selector is required when using --element")
        sys.exit(1)
    driver = create_driver(headless=HEADLESS)
    try:
        if args.page:
            result, output_path, duration = capture_full_page_baseline(args.url, args.name, driver, should_quit=False)
        elif args.element:
            result, output_path, duration = capture_element_template(args.url, args.selector, args.name, driver=driver, should_quit=False)
        else:
            print("Please specify either --page or --element")
            sys.exit(1)
    finally:
        driver.quit()
    print("\n--- Capture Result ---\n")
    print(f"🚦 Result: {result}")
    print(f"⏱️  Duration: {duration:.2f} seconds")


if __name__ == "__main__":
    main() 