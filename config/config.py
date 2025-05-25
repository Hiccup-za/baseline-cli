"""
Configuration settings for the Selenium and OpenCV testing framework.
"""
import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Browser settings
DEFAULT_BROWSER = "chrome"  # Options: chrome, firefox, edge
HEADLESS = True  # Run browser in headless mode
WINDOW_SIZE = (1920, 1080)

# Timeouts (in seconds)
DEFAULT_TIMEOUT = 10
PAGE_LOAD_TIMEOUT = 30
IMPLICIT_WAIT = 5

# Screenshot settings
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
BASELINE_DIR = os.path.join(SCREENSHOT_DIR, "baseline")
RESULTS_DIR = os.path.join(SCREENSHOT_DIR, "results")
DIFF_DIR = os.path.join(SCREENSHOT_DIR, "diff")

# Image comparison settings
SIMILARITY_THRESHOLD = 0.95  # Threshold for image comparison (0.0 to 1.0)
TEMPLATE_MATCH_THRESHOLD = 0.8  # Threshold for template matching

# Ensure directories exist
for directory in [SCREENSHOT_DIR, BASELINE_DIR, RESULTS_DIR, DIFF_DIR]:
    os.makedirs(directory, exist_ok=True)


# Web app settings
TARGET_URL = "http://localhost:3000/"