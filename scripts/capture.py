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
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add project root to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.web_utils import create_driver, take_screenshot
from config.config import TARGET_URL, BASELINE_DIR, HEADLESS
from __version__ import __version__, __title__, __description__

console = Console()

def handle_error(message, title="Baseline Capture Summary"):
    """
    Handle errors consistently with standardized output format.
    
    Args:
        message (str): Error message to display
        title (str): Title for the summary panel
    """
    result = "Failed"
    duration = 0.00
    console.print()
    console.print(f"[bold red]{message}")
    table = Table(show_header=False, box=None)
    table.add_row("Result", result)
    table.add_row("Duration", f"{duration:.2f} seconds")
    console.print()
    console.print(Panel(table, title=title, expand=False))
    sys.exit(1)

def capture_full_page_baseline(url, name, driver=None, should_quit=True):
    """
    Capture a full page screenshot as a baseline.
    
    Args:
        url (str): URL to navigate to
        name (str): Name to use for the baseline image
        driver (WebDriver, optional): Existing driver to use
        should_quit (bool): Whether to quit the driver when done
    """
    if driver is None:
        driver = create_driver(headless=HEADLESS)
    start_time = time.time()
    output_path = None
    try:
        console.print()
        with console.status("Visiting {}".format(url), spinner="dots", spinner_style="white"):
            driver.get(url)
            time.sleep(3)
        console.print("Visited URL")
        with console.status("Capturing screenshot", spinner="dots", spinner_style="white"):
            filename = f"{name}_baseline.png"
            baseline_path = take_screenshot(driver, filename=filename, folder=BASELINE_DIR)
            output_path = baseline_path
        console.print("Screenshot captured")
        with console.status("Compiling results", spinner="dots", spinner_style="white"):
            duration = time.time() - start_time
            # No real work here, but keep for consistency
        console.print("Results compiled")
        return "Success", baseline_path, duration
    except KeyboardInterrupt:
        duration = time.time() - start_time
        console.print("\n[bold yellow]Capture cancelled by user.")
        return "Cancelled", output_path, duration
    except Exception as e:
        duration = time.time() - start_time
        console.print(f"[bold red]Error capturing baseline: {str(e)}")
        return "Error", output_path, duration
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
    """
    if driver is None:
        driver = create_driver(headless=HEADLESS)
    start_time = time.time()
    output_path = None
    try:
        console.print()
        with console.status(f"Visiting {url}", spinner="dots", spinner_style="white"):
            driver.get(url)
            time.sleep(3)
        console.print("Visited URL")
        with console.status("Capturing element screenshot", spinner="dots", spinner_style="white"):
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
            template_path = os.path.join(BASELINE_DIR, f"{name}_element.png")
            elem_img.save(template_path)
            os.remove(temp_screenshot)
            output_path = template_path
        console.print("Element screenshot captured")
        with console.status("Compiling results", spinner="dots", spinner_style="white"):
            duration = time.time() - start_time
        console.print("Results compiled")
        return "Success", template_path, duration
    except KeyboardInterrupt:
        duration = time.time() - start_time
        console.print("\n[bold yellow]Capture cancelled by user.")
        return "Cancelled", output_path, duration
    except Exception as e:
        duration = time.time() - start_time
        console.print(f"[bold red]Error capturing element template: {str(e)}")
        return "Error", output_path, duration
    finally:
        if should_quit:
            driver.quit()


def main():
    """Run the baseline capture tool."""
    parser = argparse.ArgumentParser(description="Capture baseline screenshots and templates")
    parser.add_argument("--url", type=str, nargs='?', help="URL to navigate to")
    parser.add_argument("--page", action="store_true", help="Capture full page screenshot")
    parser.add_argument("--element", action="store_true", help="Capture element template")
    parser.add_argument("--name", type=str, nargs='?', help="Name for the baseline/template")
    # Add mutually exclusive group for --class and --selector
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--class", dest="class_name", type=str, nargs='?', const='', help="Class name for the element (required for --element if not using --selector)")
    group.add_argument("--selector", dest="css_selector", type=str, nargs='?', const='', help="Generic CSS selector for the element (required for --element if not using --class)")
    parser.add_argument("--version", action="store_true", help="Show version information")
    args = parser.parse_args()
    
    # Handle version request first, before any other validation
    if args.version:
        console.print(f"[bold green]{__title__}[/bold green] v{__version__}")
        console.print(f"[dim]{__description__}[/dim]")
        sys.exit(0)
    
    os.makedirs(BASELINE_DIR, exist_ok=True)

    # Custom error handling for --name and --url
    if '--name' in sys.argv and args.name is None:
        handle_error("Baseline name not provided")
    if '--name' not in sys.argv:
        handle_error("The --name arg was not provided")
    if '--url' in sys.argv and (args.url is None or args.url.startswith('--')):
        handle_error("URL not provided")
    if '--url' not in sys.argv:
        handle_error("The --url arg was not provided")

    if args.page and args.element:
        console.print("[bold red]Please choose either --page or --element, not both.")
        sys.exit(1)
    driver = create_driver(headless=HEADLESS)
    try:
        if args.page:
            result, output_path, duration = capture_full_page_baseline(args.url, args.name, driver, should_quit=False)
        elif args.element:
            # Support --class or --selector for element selection
            if args.class_name == '':
                handle_error("Class not provided")
            if args.css_selector == '':
                handle_error("Selector not provided")
            if args.class_name is None and args.css_selector is None:
                handle_error("You must provide either --class or --selector for --element")
            if args.class_name:
                result, output_path, duration = capture_element_template(args.url, args.class_name, args.name, selector_type=By.CLASS_NAME, driver=driver, should_quit=False)
            elif args.css_selector:
                result, output_path, duration = capture_element_template(args.url, args.css_selector, args.name, selector_type=By.CSS_SELECTOR, driver=driver, should_quit=False)
        else:
            # Consistent error output for missing --page/--element
            handle_error("The --page or --element arg was not provided")
    finally:
        driver.quit()
    table = Table(show_header=False, box=None)
    table.add_row("Result", result)
    table.add_row("Duration", f"{duration:.2f} seconds")
    console.print()
    console.print(Panel(table, title="Baseline Capture Summary", expand=False))


if __name__ == "__main__":
    main() 