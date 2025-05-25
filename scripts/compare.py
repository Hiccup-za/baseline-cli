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
            print(f"🧭 Visiting {url}...")
            driver.get(url)
            wait_for_page_load_complete(driver)
            # Always write current screenshot to RESULTS_DIR/current.png
            current_path = take_screenshot(driver, "current.png", folder=RESULTS_DIR)
            baseline_path = os.path.join(BASELINE_DIR, f"{baseline_name}_baseline.png")
            diff_path = os.path.join(DIFF_DIR, "diff.png")
            print("🖼️  Comparing screenshots...")
            similarity_score, _ = compare_images(
                current_path,
                baseline_path,
                output_path=diff_path
            )
            print("🛠️  Compiling results...")
            duration = time.time() - start_time
            result = "✅ Pass" if similarity_score >= SIMILARITY_THRESHOLD else "❌ Failed"
            return result, similarity_score, duration
        finally:
            driver.quit()
    except KeyboardInterrupt:
        duration = time.time() - start_time
        print("\nComparison cancelled by user.")
        return "🚫 Cancelled", None, duration
    except Exception as e:
        duration = time.time() - start_time
        print(f"🚨 Error testing website: {str(e)}")
        return "🚨 Error", None, duration

if __name__ == "__main__":
    args = parse_args()
    print("\n--- Baseline Visual Comparison ---\n")
    result, similarity_score, duration = run_website_test(args.url, args.name)
    print("\n--- Comparison Result ---\n")
    print(f"🚦 Result: {result}")
    if similarity_score is not None:
        print(f"📊 Similarity Score: {similarity_score * 100:.2f}%")
    print(f"⏱️  Duration: {duration:.2f} seconds") 