"""
Visual comparison CLI for baseline images.
"""
import os
import sys
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add project root to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.web_utils import take_screenshot, wait_for_page_load_complete
from utils.image_utils import compare_images
from config.config import (
    BASELINE_DIR, 
    RESULTS_DIR, 
    DIFF_DIR, 
    SIMILARITY_THRESHOLD,
    HEADLESS
)

console = Console()

def parse_args():
    parser = argparse.ArgumentParser(description='Run visual comparison test')
    parser.add_argument('--url', type=str, required=True, help='URL to test')
    parser.add_argument('--name', type=str, required=True, help='Name of the baseline image (without extension)')
    return parser.parse_args()

def run_website_test(url, baseline_name):
    """
    Test a website by comparing its current state with a baseline.
    
    Args:
        url (str): URL of the website to test
        baseline_name (str): Name of the baseline image (without extension)
    Returns:
        tuple: (result, similarity_score, duration)
    """
    start_time = time.time()
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
                current_path = take_screenshot(driver, "current.png", folder=RESULTS_DIR)
            console.print("Screenshot captured")
            with console.status("Comparing screenshots", spinner="dots", spinner_style="white"):
                baseline_path = os.path.join(BASELINE_DIR, f"{baseline_name}_baseline.png")
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
        console.print(f"[bold red]Error testing website: {str(e)}")
        return "Error", None, duration

def main():
    args = parse_args()
    result, similarity_score, duration = run_website_test(args.url, args.name)
    table = Table(show_header=False, box=None)
    table.add_row("Result", result)
    table.add_row("Duration", f"{duration:.2f} seconds")
    if similarity_score is not None:
        table.add_row("Similarity Score", f"{similarity_score * 100:.2f}%")
    console.print()
    console.print(Panel(table, title="Baseline Comparison Summary", expand=False))

if __name__ == "__main__":
    main() 