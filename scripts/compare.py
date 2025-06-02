"""
Script to compare screenshots against baseline images for visual regression testing.

This tool captures new screenshots and compares them with existing baselines.
"""
import os
import sys
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import cv2
import numpy as np
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from PIL import Image
from selenium.webdriver.common.by import By

# Add project root to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.web_utils import take_screenshot, wait_for_page_load_complete, create_driver
from utils.image_utils import compare_images
from config.config import (
    BASELINE_DIR, 
    RESULTS_DIR, 
    DIFF_DIR, 
    SIMILARITY_THRESHOLD,
    HEADLESS,
    TARGET_URL
)
from __version__ import __version__, __title__, __description__

console = Console()

def parse_args():
    parser = argparse.ArgumentParser(description='Run visual comparison test')
    parser.add_argument('--url', type=str, nargs='?', default=None, help='URL to test')
    parser.add_argument('--name', type=str, nargs='?', default=None, help='Name of the baseline image (without extension)')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--page', action='store_true', help='Compare full page screenshot (default)')
    group.add_argument('--element', action='store_true', help='Compare element screenshot')
    parser.add_argument('--class', dest='class_name', type=str, nargs='?', help='Class name for the element (used with --element)')
    parser.add_argument('--selector', dest='css_selector', type=str, nargs='?', help='CSS selector for the element (used with --element)')
    parser.add_argument("--version", action="store_true", help="Show version information")
    return parser.parse_args()

def compare_website_visuals(url, baseline_name, compare_element=False, class_name=None, css_selector=None):
    """
    Test a website by comparing its current state with a baseline or element image.
    Args:
        url (str): URL of the website to test
        baseline_name (str): Name of the baseline image (without extension)
        compare_element (bool): Whether to compare element image
        class_name (str): Class name for the element (if used)
        css_selector (str): CSS selector for the element (if used)
    Returns:
        tuple: (result, similarity_score, duration)
    """
    start_time = time.time()
    if compare_element:
        baseline_path = os.path.join(BASELINE_DIR, f"{baseline_name}_element.png")
    else:
        baseline_path = os.path.join(BASELINE_DIR, f"{baseline_name}_baseline.png")
    if not os.path.exists(baseline_path):
        duration = time.time() - start_time
        error_msg = f"Image not found"
        console.print(f"\n[bold red]{error_msg}")
        return "Failed", None, duration
    try:
        # Ensure the results and diff directories exist
        os.makedirs(RESULTS_DIR, exist_ok=True)
        os.makedirs(DIFF_DIR, exist_ok=True)
        chromedriver_path = ChromeDriverManager().install()
        if "THIRD_PARTY_NOTICES" in chromedriver_path:
            driver_dir = os.path.dirname(chromedriver_path)
            chromedriver_path = os.path.join(driver_dir, "chromedriver")
        os.chmod(chromedriver_path, 0o755)
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        service = ChromeService(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)
        try:
            console.print()
            with console.status(f"Visiting {url}", spinner="dots", spinner_style="white"):
                driver.get(url)
                wait_for_page_load_complete(driver)
            console.print("Visited URL")
            with console.status("Capturing screenshot", spinner="dots", spinner_style="white"):
                if compare_element:
                    # Find the element
                    if class_name:
                        element = driver.find_element(By.CLASS_NAME, class_name)
                    else:
                        element = driver.find_element(By.CSS_SELECTOR, css_selector)
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(1)
                    location = element.location
                    size = element.size
                    temp_screenshot = os.path.join(RESULTS_DIR, "temp_screenshot.png")
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
                    current_path = os.path.join(RESULTS_DIR, "current.png")
                    elem_img.save(current_path)
                    os.remove(temp_screenshot)
                else:
                    current_path = take_screenshot(driver, "current.png", folder=RESULTS_DIR)
            console.print("Screenshot captured")
            with console.status("Comparing screenshots", spinner="dots", spinner_style="white"):
                diff_path = os.path.join(DIFF_DIR, "diff.png")
                similarity_score, _ = compare_images(
                    current_path,
                    baseline_path,
                    output_path=diff_path
                )
            console.print("Screenshots compared")
            with console.status("Compiling results", spinner="dots", spinner_style="white"):
                duration = time.time() - start_time
            console.print("Results compiled")
            result = "Success" if similarity_score >= SIMILARITY_THRESHOLD else "Failed"
            return result, similarity_score, duration
        finally:
            driver.quit()
    except KeyboardInterrupt:
        duration = time.time() - start_time
        console.print("\n[bold yellow]Comparison cancelled by user.")
        return "Cancelled", None, duration
    except Exception as e:
        duration = time.time() - start_time
        console.print(f"\n[bold red]Error testing website: {str(e)}")
        return "Error", None, duration

def main():
    args = parse_args()
    
    # Handle version request first, before any other validation
    if args.version:
        console.print(f"[bold green]{__title__}[/bold green] v{__version__}")
        console.print(f"[dim]{__description__}[/dim]")
        sys.exit(0)
    
    # Check for --url provided but no value
    if '--url' in sys.argv:
        url_index = sys.argv.index('--url')
        # If --url is last or next value is another flag or missing
        if url_index == len(sys.argv) - 1 or (url_index + 1 < len(sys.argv) and sys.argv[url_index + 1].startswith('--')):
            error_msg = "URL not provided"
            duration = 0.0
            console.print(f"\n[bold red]{error_msg}")
            table = Table(show_header=False, box=None)
            table.add_row("Result", "Failed")
            table.add_row("Duration", f"{duration:.2f} seconds")
            console.print()
            console.print(Panel(table, title="Baseline Comparison Summary", expand=False))
            return

    # If neither --url nor --name are provided, show both errors
    if not args.url and not args.name:
        duration = 0.0
        console.print(f"\n[bold red]The --url arg was not provided")
        console.print(f"[bold red]The --name arg was not provided")
        table = Table(show_header=False, box=None)
        table.add_row("Result", "Failed")
        table.add_row("Duration", f"{duration:.2f} seconds")
        console.print()
        console.print(Panel(table, title="Baseline Comparison Summary", expand=False))
        return

    if not args.url:
        error_msg = "The --url arg was not provided"
        duration = 0.0
        console.print(f"\n[bold red]{error_msg}")
        table = Table(show_header=False, box=None)
        table.add_row("Result", "Failed")
        table.add_row("Duration", f"{duration:.2f} seconds")
        console.print()
        console.print(Panel(table, title="Baseline Comparison Summary", expand=False))
        return
    # Check for --name provided but no value
    if '--name' in sys.argv:
        name_index = sys.argv.index('--name')
        # If --name is last or next value is another flag or missing
        if name_index == len(sys.argv) - 1 or (name_index + 1 < len(sys.argv) and sys.argv[name_index + 1].startswith('--')):
            error_msg = "Image name not provided"
            duration = 0.0
            console.print(f"\n[bold red]{error_msg}")
            table = Table(show_header=False, box=None)
            table.add_row("Result", "Failed")
            table.add_row("Duration", f"{duration:.2f} seconds")
            console.print()
            console.print(Panel(table, title="Baseline Comparison Summary", expand=False))
            return

    if not args.name:
        error_msg = "The --name arg was not provided"
        duration = 0.0
        console.print(f"\n[bold red]{error_msg}")
        table = Table(show_header=False, box=None)
        table.add_row("Result", "Failed")
        table.add_row("Duration", f"{duration:.2f} seconds")
        console.print()
        console.print(Panel(table, title="Baseline Comparison Summary", expand=False))
        return

    # If --element is used, require --class or --selector
    if args.element:
        if not args.class_name and not args.css_selector:
            duration = 0.0
            console.print(f"\n[bold red]You must provide either --class or --selector for --element")
            table = Table(show_header=False, box=None)
            table.add_row("Result", "Failed")
            table.add_row("Duration", f"{duration:.2f} seconds")
            console.print()
            console.print(Panel(table, title="Baseline Comparison Summary", expand=False))
            return
        if args.class_name == 'class':
            duration = 0.0
            console.print(f"\n[bold red]No class name provided")
            table = Table(show_header=False, box=None)
            table.add_row("Result", "Failed")
            table.add_row("Duration", f"{duration:.2f} seconds")
            console.print()
            console.print(Panel(table, title="Baseline Comparison Summary", expand=False))
            return
        if args.css_selector == 'selector':
            duration = 0.0
            console.print(f"\n[bold red]No CSS selector provided")
            table = Table(show_header=False, box=None)
            table.add_row("Result", "Failed")
            table.add_row("Duration", f"{duration:.2f} seconds")
            console.print()
            console.print(Panel(table, title="Baseline Comparison Summary", expand=False))
            return
        result, similarity_score, duration = compare_website_visuals(args.url, args.name, compare_element=True, class_name=args.class_name, css_selector=args.css_selector)
    else:
        result, similarity_score, duration = compare_website_visuals(args.url, args.name, compare_element=False)
    table = Table(show_header=False, box=None)
    table.add_row("Result", result)
    table.add_row("Duration", f"{duration:.2f} seconds")
    if similarity_score is not None:
        table.add_row("Similarity Score", f"{similarity_score * 100:.2f}%")
    console.print()
    console.print(Panel(table, title="Baseline Comparison Summary", expand=False))

if __name__ == "__main__":
    main() 